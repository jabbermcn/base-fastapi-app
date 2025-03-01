from pydantic import BaseModel, ConfigDict
from pydantic.alias_generators import to_camel


__all__ = ["DTO", "ImmutableDTO"]


def model_title_generator(dto: object) -> str:
    return dto.__name__.replace("DTO", "")


class DTO(BaseModel):
    model_config = ConfigDict(
        model_title_generator=model_title_generator,
        str_strip_whitespace=True,
        extra="forbid",
        populate_by_name=True,
        use_enum_values=True,
        from_attributes=True,
        alias_generator=to_camel,
        allow_inf_nan=False,
        ser_json_timedelta="float",
        ser_json_bytes="base64",
        val_json_bytes="base64",
        validate_default=True,
        validate_return=True,
        coerce_numbers_to_str=True,
        regex_engine="python-re",
        use_attribute_docstrings=True,
    )


class ImmutableDTO(DTO, frozen=True):
    pass
