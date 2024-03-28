from dataclasses import dataclass, field
from enum import Enum
import re
from typing import Optional

import pytest

from anyscale._private.models import ModelBase


def test_invalid_subclass():
    """Validate that the subclass is a dataclass with frozen=True."""

    class NotADataclass(ModelBase):
        pass

    with pytest.raises(
        TypeError,
        match="Subclasses of `ModelBase` must be dataclasses with `frozen=True`.",
    ):
        NotADataclass()

    @dataclass
    class NotFrozen(ModelBase):
        pass

    with pytest.raises(
        TypeError,
        match="Subclasses of `ModelBase` must be dataclasses with `frozen=True`.",
    ):
        NotFrozen()


def test_missing_validator():
    @dataclass(frozen=True)
    class Subclass(ModelBase):
        some_field: str
        some_other_field: str

        def _validate_some_field(self, some_field: str):
            pass

    with pytest.raises(
        RuntimeError,
        match="Model 'Subclass' is missing validator method for field 'some_other_field'.",
    ):
        Subclass(some_field="hi", some_other_field="hi2")


def test_validators():
    @dataclass(frozen=True)
    class Subclass(ModelBase):
        some_field: str
        some_other_field: str

        def _validate_some_field(self, some_field: str):
            if not isinstance(some_field, str):
                raise TypeError("'some_field' must be a string.")

        def _validate_some_other_field(self, some_other_field: str):
            if not isinstance(some_other_field, str):
                raise TypeError("'some_other_field' must be a string.")

    Subclass(some_field="hi", some_other_field="hi2")
    with pytest.raises(TypeError, match="'some_other_field' must be a string."):
        Subclass(some_field="hi", some_other_field=123)


class TestToDict:
    def test_exclude_none(self):
        @dataclass(frozen=True)
        class SubModel(ModelBase):
            sub_field_1: Optional[str] = field(metadata={"detailed": True})
            sub_field_2: Optional[str]

            def _validate_sub_field_1(self, sub_field_1: Optional[str]):
                pass

            def _validate_sub_field_2(self, sub_field_2: Optional[str]):
                pass

        @dataclass(frozen=True)
        class Model(ModelBase):
            sub_model: Optional[SubModel]

            def _validate_sub_model(self, sub_model: Optional[SubModel]):
                pass

        assert Model(sub_model=None).to_dict() == {}
        assert Model(sub_model=None).to_dict(exclude_none=False) == {"sub_model": None}
        assert Model(
            sub_model=SubModel(sub_field_1=None, sub_field_2="hi")
        ).to_dict() == {"sub_model": {"sub_field_2": "hi"},}
        assert Model(sub_model=SubModel(sub_field_1=None, sub_field_2="hi")).to_dict(
            exclude_none=False
        ) == {"sub_model": {"sub_field_1": None, "sub_field_2": "hi"},}

    def test_convert_enum_to_str(self):
        class CustomEnum(Enum):
            VAL = "VAL"

        @dataclass(frozen=True)
        class Model(ModelBase):
            e: CustomEnum

            def _validate_e(self, e: CustomEnum):
                pass

        assert Model(e=CustomEnum.VAL).to_dict() == {"e": "VAL"}


def test_options():
    @dataclass(frozen=True)
    class Model(ModelBase):
        field_1: Optional[str]
        field_2: Optional[str]

        def _validate_field_1(self, field_1: Optional[str]):
            pass

        def _validate_field_2(self, field_2: Optional[str]):
            pass

    m0 = Model(field_1=None, field_2="hi2")
    assert m0.field_1 is None
    assert m0.field_2 == "hi2"

    # Check that only the passed value is overwritten.
    # m0 should be unmodified.
    m1 = m0.options(field_1="hi1")
    assert m1.field_1 == "hi1"
    assert m1.field_2 == "hi2"
    assert m0.field_1 is None
    assert m0.field_2 == "hi2"

    # Check that `None` can be passed to overwrite a value.
    m2 = m0.options(field_2=None)
    assert m2.field_1 is None
    assert m2.field_2 is None
    assert m0.field_1 is None
    assert m0.field_2 == "hi2"

    # Test passing an unknown field.
    with pytest.raises(
        ValueError,
        match=re.escape("Unexpected values passed to '.options': ['unknown']."),
    ):
        m0.options(unknown="oops")
