import copy
import pathlib
from typing import Any, Dict, List, Optional, Union

from anyscale._private.anyscale_client import (
    AnyscaleClient,
    AnyscaleClientInterface,
    WORKSPACE_CLUSTER_NAME_PREFIX,
)
from anyscale.cli_logger import BlockLogger
from anyscale.client.openapi_client.models import (
    ComputeTemplateConfig,
    DecoratedComputeTemplateConfig,
)
from anyscale.utils.runtime_env import is_dir_remote_uri, parse_requirements_file


class WorkloadSDK:
    """Shared parent class for job and service SDKs."""

    def __init__(
        self,
        *,
        logger: Optional[BlockLogger] = None,
        client: Optional[AnyscaleClientInterface] = None,
    ):
        self._logger = logger or BlockLogger()
        self._client = client or AnyscaleClient()

    @property
    def logger(self) -> BlockLogger:
        return self._logger

    @property
    def client(self) -> AnyscaleClientInterface:
        return self._client

    def override_and_load_requirements_files(
        self,
        runtime_envs: List[Dict[str, Any]],
        *,
        requirements_override: Union[None, str, List[str]],
        autopopulate_in_workspace: bool = True,
    ) -> List[Dict[str, Any]]:
        """Replaces 'pip' fields in runtime_envs with their parsed file contents.

        The precedence for overrides is: explicit overrides passed in > fields in the existing
        runtime_envs > workspace defaults (if `autopopulate_in_workspace == True`).
        """
        new_runtime_envs = copy.deepcopy(runtime_envs)

        local_path_to_parsed_requirements: Dict[str, List[str]] = {}

        def _load_requirements_file_memoized(
            target: Union[str, List[str]]
        ) -> List[str]:
            if isinstance(target, list):
                return target
            elif target in local_path_to_parsed_requirements:
                return local_path_to_parsed_requirements[target]
            elif isinstance(target, str):
                parsed_requirements = parse_requirements_file(target)
                if parsed_requirements is None:
                    raise FileNotFoundError(
                        f"Requirements file {target} does not exist."
                    )
                local_path_to_parsed_requirements[target] = parsed_requirements
                return parsed_requirements
            else:
                raise TypeError("pip field in runtime_env must be a list or string.")

            return parsed_requirements

        for runtime_env in new_runtime_envs:
            if requirements_override is not None:
                # Explicitly-specified override from the user.
                runtime_env["pip"] = requirements_override
            elif (
                autopopulate_in_workspace
                and self._client.inside_workspace()
                and "pip" not in runtime_env
                and "conda" not in runtime_env
            ):
                # If no "pip" or "conda" field was specified, try filling it in from
                # the workspace-tracked requirements file.
                workspace_requirements_path = (
                    self._client.get_workspace_requirements_path()
                )
                if workspace_requirements_path is not None:
                    self.logger.info("Including workspace-managed pip dependencies.")
                    runtime_env["pip"] = workspace_requirements_path

            if runtime_env.get("pip", None) is not None:
                # Load requirements from the file if necessary.
                runtime_env["pip"] = _load_requirements_file_memoized(
                    runtime_env["pip"]
                )

        return new_runtime_envs

    def override_and_upload_local_dirs(
        self,
        runtime_envs: List[Dict[str, Any]],
        *,
        working_dir_override: Optional[str],
        excludes_override: Optional[List[str]],
        cloud_id: Optional[str] = None,
        autopopulate_in_workspace: bool = True,
    ) -> List[Dict[str, Any]]:
        """Returns modified runtime_envs with all local dirs converted to remote URIs.

        The precedence for overrides is: explicit overrides passed in > fields in the existing
        runtime_envs > workspace defaults (if `autopopulate_in_workspace == True`).

        Each unique local directory across these fields will be uploaded once to cloud storage,
        then all occurrences of it in the config will be replaced with the corresponding remote URI.
        """
        new_runtime_envs = copy.deepcopy(runtime_envs)

        local_path_to_uri: Dict[str, str] = {}

        def _upload_dir_memoized(target: str, *, excludes: Optional[List[str]]) -> str:
            if is_dir_remote_uri(target):
                return target
            if target in local_path_to_uri:
                return local_path_to_uri[target]

            self.logger.info(f"Uploading local dir '{target}' to cloud storage.")
            uri = self._client.upload_local_dir_to_cloud_storage(
                target, cloud_id=cloud_id, excludes=excludes,
            )
            local_path_to_uri[target] = uri
            return uri

        for runtime_env in new_runtime_envs:
            # Extend, don't overwrite, excludes if it's provided.
            if excludes_override is not None:
                existing_excludes = runtime_env.get("excludes", None) or []
                runtime_env["excludes"] = existing_excludes + excludes_override

            final_excludes = runtime_env.get("excludes", [])

            new_working_dir = None
            if working_dir_override is not None:
                new_working_dir = working_dir_override
            elif "working_dir" in runtime_env:
                new_working_dir = runtime_env["working_dir"]
            elif autopopulate_in_workspace and self._client.inside_workspace():
                new_working_dir = "."

            if new_working_dir is not None:
                runtime_env["working_dir"] = _upload_dir_memoized(
                    new_working_dir, excludes=final_excludes
                )

            py_modules = runtime_env.get("py_modules", None)
            if py_modules is not None:
                runtime_env["py_modules"] = [
                    _upload_dir_memoized(py_module, excludes=final_excludes)
                    for py_module in py_modules
                ]

        return new_runtime_envs

    def resolve_compute_config_to_id(
        self, compute_config: Optional[Union[str, Dict]]
    ) -> str:
        """Resolve the passed compute config to an ID that can be passed to the backend.

        Accepts either:
            - A string of the form: '<name>[:<version>]'.
            - A dictionary from which an anonymous compute config will be built.
        """
        if compute_config is None:
            compute_config_id = self._client.get_compute_config_id()
            assert compute_config_id is not None
        elif isinstance(compute_config, str):
            compute_config_id = self._client.get_compute_config_id(
                compute_config_name=compute_config,
            )
            if compute_config_id is None:
                raise ValueError(
                    f"The compute config '{compute_config}' does not exist."
                )
        else:
            try:
                compute_config_template = ComputeTemplateConfig(**compute_config)
            except (ValueError, TypeError) as e:
                raise RuntimeError(f"Invalid compute config: {e}.")

            compute_config_id = self._client.create_anonymous_compute_config(
                compute_config_template
            )

        return compute_config_id

    def get_current_workspace_name(self) -> Optional[str]:
        """Get the name of the curernt workspace if running inside one."""
        if not self._client.inside_workspace():
            return None

        name = self._client.get_current_workspace_cluster().name
        # Defensively default to the workspace cluster name as-is if it doesn't
        # start with the expected prefix.
        if name.startswith(WORKSPACE_CLUSTER_NAME_PREFIX):
            name = name[len(WORKSPACE_CLUSTER_NAME_PREFIX) :]

        return name

    def get_containerfile_contents(self, path: str) -> str:
        """Get the full content of the containerfile as a string."""
        containerfile_path = pathlib.Path(path)
        if not containerfile_path.exists():
            raise FileNotFoundError(
                f"Containerfile '{containerfile_path}' does not exist."
            )
        if not containerfile_path.is_file():
            raise ValueError(f"Containerfile '{containerfile_path}' must be a file.")

        return containerfile_path.read_text()

    def _strip_none_values_from_dict(self, d: Dict) -> Dict:
        """Return a copy of the dictionary without any keys whose values are None.

        Recursively calls into any dictionary values.
        """
        result = {}
        for k, v in d.items():
            if isinstance(v, dict):
                result[k] = self._strip_none_values_from_dict(v)
            elif v is not None:
                result[k] = v

        return result

    def get_user_facing_compute_config(
        self, compute_config_id: str,
    ) -> Union[str, Dict]:
        """Get the compute config in a format to be displayed in a user-facing status.

        If the compute config refers to an anonymous compute config, its config
        dictionary will be returned. Else the name of the compute config will be
        returned in the form: '<name>:<version>'.
        """
        compute_config = self._client.get_compute_config(compute_config_id)
        if compute_config is None:
            raise RuntimeError(
                f"Failed to get compute config for ID {compute_config_id}."
            )

        if not compute_config.anonymous:
            compute_config_name = compute_config.name
            if compute_config.version is not None:
                compute_config_name += f":{compute_config.version}"
            return compute_config_name

        config: DecoratedComputeTemplateConfig = compute_config.config
        config_dict = {
            # Strip some internal fields that we don't want to expose to the user.
            # TODO(edoakes): we should improve the compute config model and avoid this.
            k: v
            for k, v in config.to_dict().items()
            if k
            not in {
                "cloud",
                "cloud_id",
                "maximum_uptime_minutes",
                "idle_termination_minutes",
            }
        }
        return self._strip_none_values_from_dict(config_dict)
