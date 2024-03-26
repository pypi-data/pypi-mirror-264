from typing import Optional

from anyscale._private.sdk import inject_sdk_singleton
from anyscale.service._private.service_sdk import ServiceSDK
from anyscale.service.models import ServiceConfig, ServiceStatus


_SERVICE_SDK_SINGLETON_KEY = "service_sdk"


@inject_sdk_singleton(_SERVICE_SDK_SINGLETON_KEY, ServiceSDK)
def deploy(
    config: ServiceConfig,
    *,
    in_place: bool = False,
    canary_percent: Optional[int] = None,
    max_surge_percent: Optional[int] = None,
    _sdk: ServiceSDK,
):
    return _sdk.deploy(
        config,
        in_place=in_place,
        canary_percent=canary_percent,
        max_surge_percent=max_surge_percent,
    )


@inject_sdk_singleton(_SERVICE_SDK_SINGLETON_KEY, ServiceSDK)
def rollback(
    name: Optional[str], *, max_surge_percent: Optional[int] = None, _sdk: ServiceSDK,
):
    return _sdk.rollback(name=name, max_surge_percent=max_surge_percent)


@inject_sdk_singleton(_SERVICE_SDK_SINGLETON_KEY, ServiceSDK)
def terminate(name: Optional[str], *, _sdk: ServiceSDK):
    return _sdk.terminate(name=name)


@inject_sdk_singleton(_SERVICE_SDK_SINGLETON_KEY, ServiceSDK)
def status(name: Optional[str], *, _sdk: ServiceSDK) -> ServiceStatus:
    return _sdk.status(name=name)
