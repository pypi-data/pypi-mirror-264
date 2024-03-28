from dataclasses import dataclass, field
from typing import Any, Dict, Optional

from anyscale._private.models import WorkloadConfig


@dataclass(frozen=True)
class JobConfig(WorkloadConfig):
    entrypoint: str = field(default="", repr=False)

    def _validate_entrypoint(self, entrypoint: str):
        if not isinstance(entrypoint, str):
            raise TypeError("'entrypoint' must be a string.")

        if not entrypoint:
            raise ValueError("'entrypoint' cannot be empty.")

    max_retries: int = field(default=1, repr=False)

    def _validate_max_retries(self, max_retries: int):
        if not isinstance(max_retries, int):
            raise TypeError("'max_retries' must be an int.")

        if max_retries < 0:
            raise ValueError("'max_retries' must be >= 0.")

    runtime_env: Optional[Dict[str, Any]] = field(default=None, repr=False)

    def _validate_runtime_env(self, runtime_env: Optional[Dict[str, Any]]):
        if runtime_env is None:
            return

        if not isinstance(runtime_env, dict):
            raise TypeError("'runtime_env' must be a dictionary.")
