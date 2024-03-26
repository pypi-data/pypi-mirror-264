import copy
from typing import Optional
import uuid

from anyscale._private.models.image_uri import ImageURI
from anyscale._private.sdk.workload_sdk import WorkloadSDK
from anyscale.cli_logger import BlockLogger
from anyscale.client.openapi_client.models import (
    CreateInternalProductionJob,
    InternalProductionJob,
    ProductionJobConfig,
)
from anyscale.job.models import JobConfig


logger = BlockLogger()


class JobSDK(WorkloadSDK):
    def _override_runtime_env(
        self,
        config: JobConfig,
        *,
        autopopulate_in_workspace: bool = True,
        cloud_id: Optional[str] = None,
    ) -> JobConfig:
        """Overrides the runtime_env in the config.

        Local directories specified in the 'working_dir' or 'py_modules' fields will be
        uploaded and replaced with the resulting remote URIs.

        Requirements files will be loaded and populated into the 'pip' field.

        If autopopulate_from_workspace is passed and this code is running inside a
        workspace, the following defaults will be applied:
            - 'working_dir' will be set to '.'.
            - 'pip' will be set to the workspace-managed requirements file.
        """
        new_runtime_env = (
            copy.deepcopy(config.runtime_env) if config.runtime_env else {}
        )
        [new_runtime_env] = self.override_and_upload_local_dirs(
            [new_runtime_env],
            working_dir_override=config.working_dir,
            excludes_override=config.excludes,
            cloud_id=cloud_id,
            autopopulate_in_workspace=autopopulate_in_workspace,
        )
        [new_runtime_env] = self.override_and_load_requirements_files(
            [new_runtime_env],
            requirements_override=config.requirements,
            autopopulate_in_workspace=autopopulate_in_workspace,
        )

        if new_runtime_env:
            # If `None` or `{}` was passed in and no overrides happened, leave it as-is.
            config = config.options(runtime_env=new_runtime_env)

        return config.options(requirements=None, working_dir=None, excludes=None,)

    def _get_default_name(self) -> str:
        """Get a default name for the job.

        If running inside a workspace, this is generated from the workspace name,
        else it generates a random name.
        """
        # TODO(edoakes): generate two random words instead of UUID here.
        name = f"job-{self.get_current_workspace_name() or str(uuid.uuid4())}"
        self.logger.info(f"No name was specified, using default: '{name}'.")
        return name

    def submit(self, config: JobConfig) -> str:
        name = config.name or self._get_default_name()
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
        config = self._override_runtime_env(config, cloud_id=cloud_id)

        job: InternalProductionJob = self.client.submit_job(
            CreateInternalProductionJob(
                name=name,
                # TODO(edoakes): should we support a description?
                description=None,
                project_id=self.client.get_project_id(),
                workspace_id=self.client.get_current_workspace_id(),
                config=ProductionJobConfig(
                    entrypoint=config.entrypoint,
                    runtime_env=config.runtime_env,
                    build_id=build_id,
                    compute_config_id=compute_config_id,
                    max_retries=config.max_retries,
                ),
                # TODO(edoakes): support job queue config.
                job_queue_config=None,
            )
        )

        self.logger.info(f"Job '{name}' submitted, ID: '{job.id}'.")
        self.logger.info(
            f"View the job in the UI: {self.client.get_job_ui_url(job.id)}"
        )
        return job.id
