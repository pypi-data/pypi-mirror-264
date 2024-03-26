from dataclasses import asdict, fields
from enum import Enum
from typing import Any, Dict, Iterable, Tuple, TypeVar

import yaml


# In Python 3.11 there is a 'Self' introduced, but this is the
# workaround before that: https://peps.python.org/pep-0673/.
TModelBase = TypeVar("TModelBase", bound="ModelBase")


class ModelBase:
    def __new__(cls, *args, **kwargs):  # noqa: ARG003
        """Validate that the subclass is a conforming dataclass."""
        if (
            not hasattr(cls, "__dataclass_params__")
            or not cls.__dataclass_params__.frozen
        ):
            raise TypeError(
                "Subclasses of `ModelBase` must be dataclasses with `frozen=True`."
            )

        return super().__new__(cls)

    def _run_validators(self):
        """Run magic validator methods.

        Looks for methods with the name: `_validate_{field}`. The method will be called
        with the field value as its sole argument.
        """
        for field in fields(self):
            validator = getattr(self, f"_validate_{field.name}", None)
            if validator is None:
                raise RuntimeError(
                    f"Model '{type(self).__name__}' is missing validator method for field '{field.name}'."
                )

            validator(getattr(self, field.name))

    def __post_init__(self):
        self._run_validators()

    @classmethod
    def from_yaml(cls, path: str):
        with open(path) as f:
            return cls(**yaml.safe_load(f))

    def to_dict(self, *, exclude_none: bool = True) -> Dict[str, Any]:
        """Convert the model to a dictionary representation.

        If `exclude_none` is `True`, keys whose values are `None` will be excluded.
        """

        def maybe_exclude_nones(i: Iterable[Tuple[str, Any]]):
            d = {}
            for k, v in i:
                # Exclude none values if specified.
                if exclude_none and v is None:
                    continue

                # Convert enums to their string representation.
                if isinstance(v, Enum):
                    v = v.value

                d[k] = v

            return d

        return asdict(self, dict_factory=maybe_exclude_nones)

    def options(self: TModelBase, **kwargs) -> TModelBase:
        """Return a copy of the model with the provided fields updated.

        All fields in the constructor are supported. Those not provided will be unchanged.
        """
        self_dict = self.to_dict(exclude_none=False)
        new_instance_kwargs = {
            field: kwargs.pop(field) if field in kwargs else self_dict[field]
            for field in self_dict
        }
        if len(kwargs) > 0:
            raise ValueError(
                f"Unexpected values passed to '.options': {list(kwargs.keys())}."
            )

        return type(self)(**new_instance_kwargs)
