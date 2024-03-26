import pathlib
from subprocess import list2cmdline
from typing import Optional, Tuple

import click

import anyscale
from anyscale.cli_logger import BlockLogger
from anyscale.client.openapi_client import HaJobStates
from anyscale.controllers.job_controller import JobController
from anyscale.job.models import JobConfig
from anyscale.util import validate_non_negative_arg


log = BlockLogger()  # CLI Logger


@click.group("job", help="Interact with production jobs running on Anyscale.")
def job_cli() -> None:
    pass


@job_cli.command(
    name="submit", short_help="Submit a job.",
)
@click.option("--name", "-n", required=False, default=None, help="Name of the job.")
@click.option(
    "--description", required=False, default=None, help="Description of the job."
)
@click.option(
    "--follow",
    "-f",
    required=False,
    default=False,
    type=bool,
    is_flag=True,
    help="Whether to follow the log of the created job",
)
@click.option(
    "--wait",
    "-w",
    required=False,
    default=False,
    type=bool,
    is_flag=True,
    help="Whether to block this CLI command until the job succeeds (or reaches another terminal state)",
)
@click.argument("entrypoint", required=False, nargs=-1, type=click.UNPROCESSED)
def submit(
    entrypoint: Tuple[str],
    name: Optional[str],
    description: Optional[str],
    follow: Optional[bool],
    wait: Optional[bool],
):
    """Submit a job.

    The job config can be specified from a file or inlined in this command:

    $ anyscale job submit config.yaml # Submit from a config file.

    $ anyscale job submit -- python main.py # Submit from an inlined entrypoint.

    By default, this command submits the job asynchronously and exits. To wait for the job to complete, use the `--wait` flag.
    """

    if len(entrypoint) == 0:
        raise click.ClickException(
            "Either a config file or an inlined entrypoint must be provided."
        )

    config_path: Optional[str] = None
    if len(entrypoint) == 1:
        maybe_config_path = entrypoint[0]
        if pathlib.Path(maybe_config_path).is_file():
            config_path = entrypoint[0]
            log.info(f"Submitting job from config file: '{config_path}'.")
        elif maybe_config_path.endswith(".yaml"):
            raise click.ClickException(
                f"Job config file '{maybe_config_path}' not found."
            )

    job_controller = JobController()
    if config_path is not None:
        job_id = job_controller.submit(config_path, name=name, description=description,)
    else:
        job_id = anyscale.job.submit(
            JobConfig(name=name, entrypoint=list2cmdline(entrypoint))
        )

    if follow or wait:
        job_controller.log.info(
            "Waiting for the job to run. Interrupting this command will not cancel the job."
        )
    else:
        job_controller.log.info(
            "Use `--wait` to wait for the job to run and stream logs."
        )

    if follow:
        job_controller.logs(job_id, should_follow=follow)
    if wait:
        job_controller.wait(job_id=job_id)


@job_cli.command(name="list", help="Display information about existing jobs.")
@click.option("--name", "-n", required=False, default=None, help="Filter by job name.")
@click.option(
    "--job-id", "--id", required=False, default=None, help="Filter by job id."
)
@click.option(
    "--project-id", required=False, default=None, help="Filter by project id."
)
@click.option(
    "--include-all-users",
    is_flag=True,
    default=False,
    help="Include jobs not created by current user.",
)
@click.option(
    "--include-archived",
    is_flag=True,
    default=False,
    help=(
        "List archived jobs as well as unarchived jobs."
        "If not provided, defaults to listing only unarchived jobs."
    ),
)
@click.option(
    "--max-items",
    required=False,
    default=10,
    type=int,
    help="Max items to show in list.",
    callback=validate_non_negative_arg,
)
def list(  # noqa: A001
    name: Optional[str],
    job_id: Optional[str],
    project_id: Optional[str],
    include_all_users: bool,
    include_archived: bool,
    max_items: int,
) -> None:
    job_controller = JobController()
    job_controller.list(
        name=name,
        job_id=job_id,
        project_id=project_id,
        include_all_users=include_all_users,
        include_archived=include_archived,
        max_items=max_items,
    )


@job_cli.command(name="archive", help="Archive a job.")
@click.option("--job-id", "--id", required=False, help="Unique ID of the job.")
@click.option("--name", "-n", required=False, help="Name of the job.")
def archive(job_id: Optional[str], name: Optional[str]) -> None:
    job_controller = JobController()
    job_controller.archive(job_id=job_id, job_name=name)


@job_cli.command(name="terminate", help="Attempt to terminate a job asynchronously.")
@click.option("--job-id", "--id", required=False, help="Unique ID of the job.")
@click.option("--name", "-n", required=False, help="Name of the job.")
def terminate(job_id: Optional[str], name: Optional[str]) -> None:
    job_controller = JobController()
    job_controller.terminate(job_id=job_id, job_name=name)


@job_cli.command(name="logs")
@click.option("--job-id", "--id", required=False, help="Unique ID of the job.")
@click.option("--name", "-n", required=False, help="Name of the job.")
@click.option(
    "--follow",
    "-f",
    required=False,
    default=False,
    type=bool,
    is_flag=True,
    help="Whether to follow the log.",
)
@click.option(
    "--all-attempts",
    is_flag=True,
    default=False,
    help="Show logs for all job attempts.",
)
def logs(
    job_id: Optional[str],
    name: Optional[str],
    follow: bool = False,
    all_attempts: bool = False,
) -> None:
    """Print the logs of a job.

    By default from the latest job attempt.

    Example usage:

        anyscale job logs --id prodjob_123

        anyscale job logs --id prodjob_123 -f

        anyscale job logs -n my-job --all-attempts"""
    job_controller = JobController(raise_structured_exception=True)
    job_controller.logs(
        job_id=job_id, job_name=name, should_follow=follow, all_attempts=all_attempts,
    )


@job_cli.command(name="wait")
@click.option("--job-id", "--id", required=False, help="Unique ID of the job.")
@click.option("--name", "-n", required=False, help="Name of the job.")
@click.option(
    "--state",
    "-s",
    required=False,
    default=HaJobStates.SUCCESS,
    help="The state to wait for this Job to enter",
)
@click.option(
    "--timeout",
    "-t",
    required=False,
    default=None,
    type=float,
    help="The timeout in seconds after which this command will exit.",
)
def wait(
    job_id: Optional[str],
    name: Optional[str],
    state: str = HaJobStates.SUCCESS,
    timeout=None,
) -> None:
    """Wait for a Job to enter a specific state (default: SUCCESS).

    To specify the Job by name, use the --name flag. To specify the Job by id, use the --job-id flag.

    If the Job reaches the target state, the command will exit successfully.

    If the Job reaches a terminal state other than the target state, the command will exit with an error.

    If the command reaches the timeout, the command will exit with an error.
    """
    state = state.upper()
    job_controller = JobController()
    job_id = job_controller.wait(
        job_id=job_id, job_name=name, target_state=state, timeout_secs=timeout,
    )
