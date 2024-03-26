import os
from typing import Generator, Optional
from unittest.mock import Mock, patch

import click
from click.testing import CliRunner
import pytest

from anyscale._private.sdk import _LAZY_SDK_SINGLETONS
from anyscale.commands.job_commands import submit
from anyscale.job.commands import _JOB_SDK_SINGLETON_KEY
from anyscale.job.models import JobConfig


def _get_test_file_path(subpath: str) -> str:
    return os.path.join(os.path.dirname(__file__), "test_files/", subpath,)


MINIMAL_CONFIG_PATH = _get_test_file_path("job_config_files/minimal.yaml")


class FakeJobSDK:
    DEFAULT_JOB_ID = "default-fake-job-id"

    def __init__(self):
        self._submitted_config: Optional[JobConfig] = None

    @property
    def submitted_config(self) -> Optional[JobConfig]:
        return self._submitted_config

    def submit(self, config: JobConfig):
        assert isinstance(config, JobConfig)
        self._submitted_config = config
        return self.DEFAULT_JOB_ID


@pytest.fixture()
def mock_job_controller() -> Generator[Mock, None, None]:
    mock_job_controller = Mock(submit=Mock(return_value=FakeJobSDK.DEFAULT_JOB_ID))
    mock_job_controller_cls = Mock(return_value=mock_job_controller)
    with patch(
        "anyscale.commands.job_commands.JobController", new=mock_job_controller_cls,
    ):
        yield mock_job_controller


@pytest.fixture()
def fake_job_sdk() -> Generator[FakeJobSDK, None, None]:
    fake_job_sdk = FakeJobSDK()
    _LAZY_SDK_SINGLETONS[_JOB_SDK_SINGLETON_KEY] = fake_job_sdk
    try:
        yield fake_job_sdk
    finally:
        del _LAZY_SDK_SINGLETONS[_JOB_SDK_SINGLETON_KEY]


def _assert_error_message(result: click.testing.Result, *, message: str):
    assert result.exit_code != 0
    assert message in result.stdout


class TestSubmit:
    def test_missing_arg(self, fake_job_sdk, mock_job_controller):
        runner = CliRunner()
        result = runner.invoke(submit)
        _assert_error_message(
            result,
            message="Either a config file or an inlined entrypoint must be provided.",
        )

    def test_config_file_not_found(self, fake_job_sdk, mock_job_controller):
        runner = CliRunner()
        result = runner.invoke(submit, ["missing_config.yaml"])
        _assert_error_message(
            result, message="Job config file 'missing_config.yaml' not found.",
        )

    @pytest.mark.parametrize("inlined_entrypoint", [False, True])
    def test_basic(self, fake_job_sdk, mock_job_controller, inlined_entrypoint: bool):
        runner = CliRunner()
        entrypoint_args = (
            ["--", "python", "main.py"] if inlined_entrypoint else [MINIMAL_CONFIG_PATH]
        )
        result = runner.invoke(submit, [*entrypoint_args])
        assert result.exit_code == 0

        if inlined_entrypoint:
            # Passing an inlined entrypoint should go through the new path.
            assert fake_job_sdk.submitted_config == JobConfig(
                entrypoint="python main.py"
            )
            mock_job_controller.submit.assert_not_called()
        else:
            # For now, passing a config file should go through the old path.
            assert fake_job_sdk.submitted_config is None
            mock_job_controller.submit.assert_called_once_with(
                MINIMAL_CONFIG_PATH, name=None, description=None
            )

    @pytest.mark.parametrize("inlined_entrypoint", [False, True])
    def test_override_name(
        self, fake_job_sdk, mock_job_controller, inlined_entrypoint: bool
    ):
        runner = CliRunner()
        entrypoint_args = (
            ["--", "python", "main.py"] if inlined_entrypoint else [MINIMAL_CONFIG_PATH]
        )
        result = runner.invoke(submit, ["--name", "test-name", *entrypoint_args])
        assert result.exit_code == 0

        if inlined_entrypoint:
            assert fake_job_sdk.submitted_config == JobConfig(
                entrypoint="python main.py", name="test-name"
            )
            mock_job_controller.submit.assert_not_called()
        else:
            assert fake_job_sdk.submitted_config is None
            mock_job_controller.submit.assert_called_once_with(
                MINIMAL_CONFIG_PATH, name="test-name", description=None
            )

    @pytest.mark.parametrize("inlined_entrypoint", [False, True])
    def test_override_description(
        self, fake_job_sdk, mock_job_controller, inlined_entrypoint: bool
    ):
        runner = CliRunner()

        entrypoint_args = (
            ["--", "python", "main.py"] if inlined_entrypoint else [MINIMAL_CONFIG_PATH]
        )
        result = runner.invoke(
            submit, ["--description", "test-description", *entrypoint_args]
        )
        assert result.exit_code == 0

        if inlined_entrypoint:
            # TODO(edoakes): support description in JobConfig.
            assert fake_job_sdk.submitted_config == JobConfig(
                entrypoint="python main.py"
            )
            mock_job_controller.submit.assert_not_called()
        else:
            assert fake_job_sdk.submitted_config is None
            mock_job_controller.submit.assert_called_once_with(
                MINIMAL_CONFIG_PATH, name=None, description="test-description"
            )

    @pytest.mark.parametrize("inlined_entrypoint", [False, True])
    def test_no_follow_by_default(
        self, fake_job_sdk, mock_job_controller, inlined_entrypoint: bool
    ):
        runner = CliRunner()

        entrypoint_args = (
            ["--", "python", "main.py"] if inlined_entrypoint else [MINIMAL_CONFIG_PATH]
        )
        result = runner.invoke(submit, [*entrypoint_args])
        assert result.exit_code == 0

        mock_job_controller.logs.assert_not_called()
        mock_job_controller.wait.assert_not_called()

    @pytest.mark.parametrize("inlined_entrypoint", [False, True])
    def test_follow(self, fake_job_sdk, mock_job_controller, inlined_entrypoint: bool):
        runner = CliRunner()

        entrypoint_args = (
            ["--", "python", "main.py"] if inlined_entrypoint else [MINIMAL_CONFIG_PATH]
        )
        result = runner.invoke(submit, ["--follow", *entrypoint_args])
        assert result.exit_code == 0
        print(result.stdout)

        mock_job_controller.logs.assert_called_once_with(
            fake_job_sdk.DEFAULT_JOB_ID, should_follow=True
        )
        mock_job_controller.wait.assert_not_called()

    @pytest.mark.parametrize("inlined_entrypoint", [False, True])
    def test_no_wait_by_default(
        self, fake_job_sdk, mock_job_controller, inlined_entrypoint: bool
    ):
        runner = CliRunner()

        entrypoint_args = (
            ["--", "python", "main.py"] if inlined_entrypoint else [MINIMAL_CONFIG_PATH]
        )
        result = runner.invoke(submit, [*entrypoint_args])
        assert result.exit_code == 0

        mock_job_controller.logs.assert_not_called()
        mock_job_controller.wait.assert_not_called()

    @pytest.mark.parametrize("inlined_entrypoint", [False, True])
    def test_wait(self, fake_job_sdk, mock_job_controller, inlined_entrypoint: bool):
        runner = CliRunner()

        entrypoint_args = (
            ["--", "python", "main.py"] if inlined_entrypoint else [MINIMAL_CONFIG_PATH]
        )
        result = runner.invoke(submit, ["--wait", *entrypoint_args])
        assert result.exit_code == 0
        print(result.stdout)

        mock_job_controller.logs.assert_not_called()
        mock_job_controller.wait.assert_called_once_with(
            job_id=fake_job_sdk.DEFAULT_JOB_ID,
        )
