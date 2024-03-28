import copy
from typing import Any, Dict, Optional

from anyscale._private.models.image_uri import ImageURI
from anyscale._private.sdk.workload_sdk import WorkloadSDK
from anyscale.cli_logger import BlockLogger
from anyscale.sdk.anyscale_client.models import (
    AccessConfig,
    ApplyServiceModel,
    ProductionServiceV2VersionModel,
    RayGCSExternalStorageConfig,
    ServiceConfig as ExternalAPIServiceConfig,
    ServiceEventCurrentState,
    ServiceModel,
)
from anyscale.service.models import (
    ServiceConfig,
    ServiceState,
    ServiceStatus,
    ServiceVersionStatus,
)
from anyscale.utils.workspace_notification import (
    WorkspaceNotification,
    WorkspaceNotificationAction,
)


logger = BlockLogger()


class ServiceSDK(WorkloadSDK):
    def _override_application_runtime_envs(
        self,
        config: ServiceConfig,
        *,
        autopopulate_in_workspace: bool = True,
        cloud_id: Optional[str] = None,
    ) -> ServiceConfig:
        """Overrides the runtime_env of each application in the config.

        Local directories specified in the 'working_dir' or 'py_modules' fields will be
        uploaded and replaced with the resulting remote URIs.

        Requirements files will be loaded and populated into the 'pip' field.

        If autopopulate_from_workspace is passed and this code is running inside a
        workspace, the following defaults will be applied:
            - 'working_dir' will be set to '.'.
            - 'pip' will be set to the workspace-managed requirements file.
        """
        new_applications = copy.deepcopy(config.applications)
        new_runtime_envs = [app.get("runtime_env", {}) for app in new_applications]

        new_runtime_envs = self.override_and_upload_local_dirs(
            new_runtime_envs,
            working_dir_override=config.working_dir,
            excludes_override=config.excludes,
            cloud_id=cloud_id,
            autopopulate_in_workspace=autopopulate_in_workspace,
        )
        new_runtime_envs = self.override_and_load_requirements_files(
            new_runtime_envs,
            requirements_override=config.requirements,
            autopopulate_in_workspace=autopopulate_in_workspace,
        )

        for app, new_runtime_env in zip(new_applications, new_runtime_envs):
            if new_runtime_env:
                app["runtime_env"] = new_runtime_env

        return config.options(
            applications=new_applications,
            requirements=None,
            working_dir=None,
            excludes=None,
        )

    def _get_default_name(self) -> str:
        """Get a default name for the service.

        A default is currently only generated when running inside a workspace
        (from the workspace cluster name), so this function errors if called outside
        a workspace.
        """
        name = self.get_current_workspace_name()
        if name is None:
            raise ValueError(
                "A service name must be provided when running outside of a workspace."
            )

        self.logger.info(f"No name was specified, using default: '{name}'.")
        return name

    def _log_deployed_service_info(
        self, service: ServiceModel, *, canary_percent: Optional[int]
    ):
        """Log user-facing information about a deployed service."""
        canary_percent_info = (
            ""
            if canary_percent is None
            else f" (target canary percent: {canary_percent})"
        )
        message = f"Service '{service.name}' deployed{canary_percent_info}."
        self.logger.info(message)
        if self.client.inside_workspace():
            self.client.send_workspace_notification(
                WorkspaceNotification(
                    body=message,
                    action=WorkspaceNotificationAction(
                        type="navigate-service", title="View Service", value=service.id,
                    ),
                ),
            )

        self.logger.info(
            f"View the service in the UI: '{self.client.get_service_ui_url(service.id)}'"
        )
        self.logger.info(
            "Query the service once it's running using the following curl command:"
        )
        auth_token_header = (
            ""
            if service.auth_token is None
            else f"-H 'Authorization: Bearer {service.auth_token}' "
        )
        self.logger.info(f"curl {auth_token_header}{service.base_url}/")

    def _build_apply_service_model_from_config(
        self,
        name: str,
        config: ServiceConfig,
        *,
        in_place: bool = False,
        canary_percent: Optional[int] = None,
        max_surge_percent: Optional[int] = None,
    ) -> ApplyServiceModel:
        if config.containerfile is not None:
            build_id = self.client.get_cluster_env_build_id_from_containerfile(
                cluster_env_name=f"image-for-{name}",
                containerfile=self.get_containerfile_contents(config.containerfile),
            )
        elif config.image_uri is not None:
            build_id = self.client.get_cluster_env_build_id_from_image_uri(
                image_uri=ImageURI.from_str(config.image_uri)
            )
        else:
            build_id = self.client.get_default_build_id()

        compute_config_id = self.resolve_compute_config_to_id(config.compute_config)

        # If a compute config was specified, we need to make sure to used the correct
        # cloud_id when uploading local directories.
        cloud_id = self.client.get_cloud_id(
            compute_config_id=None
            if config.compute_config is None
            else compute_config_id
        )
        config = self._override_application_runtime_envs(config, cloud_id=cloud_id)

        ray_serve_config: Dict[str, Any] = {"applications": config.applications}
        if config.http_options:
            ray_serve_config["http_options"] = config.http_options
        if config.grpc_options:
            ray_serve_config["grpc_options"] = config.grpc_options
        if config.logging_config:
            ray_serve_config["logging_config"] = config.logging_config

        ray_gcs_external_storage_config = None
        if config.ray_gcs_external_storage_config is not None:
            ray_gcs_external_storage_config = RayGCSExternalStorageConfig(
                **config.ray_gcs_external_storage_config
            )

        return ApplyServiceModel(
            name=name,
            project_id=self.client.get_project_id(),
            ray_serve_config=ray_serve_config,
            build_id=build_id,
            compute_config_id=compute_config_id,
            canary_percent=canary_percent,
            max_surge_percent=max_surge_percent,
            rollout_strategy="IN_PLACE" if in_place else "ROLLOUT",
            config=ExternalAPIServiceConfig(
                access=AccessConfig(use_bearer_token=config.query_auth_token_enabled),
            ),
            ray_gcs_external_storage_config=ray_gcs_external_storage_config,
        )

    def deploy(
        self,
        config: ServiceConfig,
        *,
        in_place: bool = False,
        canary_percent: Optional[int] = None,
        max_surge_percent: Optional[int] = None,
    ):
        if not isinstance(in_place, bool):
            raise TypeError("in_place must be a bool.")

        if canary_percent is not None:
            if not isinstance(canary_percent, int):
                raise TypeError("canary_percent must be an int.")
            if canary_percent < 0 or canary_percent > 100:
                raise ValueError("canary_percent must be between 0 and 100.")

        if max_surge_percent is not None:
            if not isinstance(max_surge_percent, int):
                raise TypeError("max_surge_percent must be an int.")

            if max_surge_percent < 0 or max_surge_percent > 100:
                raise ValueError("max_surge_percent must be between 0 and 100.")

        name = config.name or self._get_default_name()

        existing_service: Optional[ServiceModel] = self.client.get_service(name)
        if existing_service is None:
            self.logger.info(f"Starting new service '{name}'.")
        elif existing_service.current_state == ServiceEventCurrentState.TERMINATED:
            self.logger.info(f"Restarting existing service '{name}'.")
        else:
            self.logger.info(f"Updating existing service '{name}'.")

        service: ServiceModel = self.client.rollout_service(
            self._build_apply_service_model_from_config(
                name,
                config,
                in_place=in_place,
                canary_percent=canary_percent,
                max_surge_percent=max_surge_percent,
            )
        )

        self._log_deployed_service_info(service, canary_percent=canary_percent)

    def rollback(
        self, name: Optional[str] = None, *, max_surge_percent: Optional[int] = None,
    ):
        if name is None:
            name = self._get_default_name()

        model: Optional[ServiceModel] = self.client.get_service(name)
        if model is None:
            raise RuntimeError(f"Service with name '{name}' was not found.")

        return self.client.rollback_service(
            model.id, max_surge_percent=max_surge_percent,
        )

    def terminate(self, name: Optional[str] = None):
        if name is None:
            name = self._get_default_name()

        model: Optional[ServiceModel] = self.client.get_service(name)
        if model is None:
            raise RuntimeError(f"Service with name '{name}' was not found.")

        return self.client.terminate_service(model.id,)

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

    def _service_version_model_to_status(
        self,
        model: ProductionServiceV2VersionModel,
        *,
        service_name: str,
        query_auth_token_enabled: bool,
    ) -> ServiceVersionStatus:
        image_uri = self.client.get_cluster_env_build_image_uri(model.build_id)
        if image_uri is None:
            raise RuntimeError(f"Failed to get image URI for ID {model.build_id}.")

        ray_gcs_external_storage_config = None
        if model.ray_gcs_external_storage_config is not None:
            ray_gcs_external_storage_config = self._strip_none_values_from_dict(
                model.ray_gcs_external_storage_config.to_dict()
            )

        return ServiceVersionStatus(
            name=model.version,
            # NOTE(edoakes): there is also a "current_weight" field but it does not match the UI.
            weight=model.weight,
            config=ServiceConfig(
                name=service_name,
                applications=model.ray_serve_config["applications"],
                image_uri=str(image_uri),
                compute_config=self.get_user_facing_compute_config(
                    model.compute_config_id
                ),
                query_auth_token_enabled=query_auth_token_enabled,
                http_options=model.ray_serve_config.get("http_options", None),
                grpc_options=model.ray_serve_config.get("grpc_options", None),
                logging_config=model.ray_serve_config.get("logging_config", None),
                ray_gcs_external_storage_config=ray_gcs_external_storage_config,
            ),
        )

    def _service_model_to_status(self, model: ServiceModel) -> ServiceStatus:
        # TODO(edoakes): for some reason the primary_version is populated
        # when the service is terminated. This should be fixed in the backend.
        is_terminated = model.current_state == ServiceEventCurrentState.TERMINATED

        # TODO(edoakes): this is currently only exposed at the service level in the API,
        # which means that the per-version `query_auth_token_enabled` field will lie if
        # it's changed.
        query_auth_token_enabled = model.auth_token is not None

        primary_version = None
        if not is_terminated and model.primary_version is not None:
            primary_version = self._service_version_model_to_status(
                model.primary_version,
                service_name=model.name,
                query_auth_token_enabled=query_auth_token_enabled,
            )

        canary_version = None
        if not is_terminated and model.canary_version is not None:
            canary_version = self._service_version_model_to_status(
                model.canary_version,
                service_name=model.name,
                query_auth_token_enabled=query_auth_token_enabled,
            )

        # If we add a new state to the backend, old clients may not recognize it.
        # Rather than erroring out and causing old code to crash, return UNKNOWN.
        try:
            state = ServiceState(model.current_state)
        except ValueError:
            state = ServiceState.UNKNOWN
            self.logger.warning(
                f"Got unrecognized state: '{model.current_state}'. "
                "You likely need to update the 'anyscale' package. "
                "If you still see this message after upgrading, contact Anyscale support."
            )

        return ServiceStatus(
            id=model.id,
            name=model.name,
            state=state,
            query_url=model.base_url,
            query_auth_token=model.auth_token,
            primary_version=primary_version,
            canary_version=canary_version,
        )

    def status(self, name: Optional[str] = None) -> ServiceStatus:
        if name is None:
            name = self._get_default_name()

        model: Optional[ServiceModel] = self.client.get_service(name)
        if model is None:
            raise RuntimeError(f"Service with name '{name}' was not found.")

        return self._service_model_to_status(model)
