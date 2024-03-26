from anyscale._private.sdk import inject_sdk_singleton
from anyscale.job._private.job_sdk import JobSDK
from anyscale.job.models import JobConfig


_JOB_SDK_SINGLETON_KEY = "job_sdk"


@inject_sdk_singleton(_JOB_SDK_SINGLETON_KEY, JobSDK)
def submit(config: JobConfig, *, _sdk: JobSDK) -> str:
    return _sdk.submit(config)
