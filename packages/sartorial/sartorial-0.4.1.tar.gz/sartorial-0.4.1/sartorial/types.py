from datetime import date, datetime, time, timedelta
from decimal import Decimal
from enum import Enum
from ipaddress import (
    IPv4Address,
    IPv4Interface,
    IPv4Network,
    IPv6Address,
    IPv6Interface,
    IPv6Network,
)
from pathlib import Path
from typing import Any as AnyType
from typing import ClassVar, Type
from uuid import UUID

from foundational.nulls import DoesNotExist, Omitted
from pydantic import GetCoreSchemaHandler
from pydantic.json_schema import GetJsonSchemaHandler, JsonSchemaValue
from pydantic_core import CoreSchema, core_schema

JSON_SCHEMA_DEFAULT_TYPES = {
    "string": str,
    "number": float,
    "integer": int,
    "boolean": bool,
    "object": dict,
    "array": list,
    "null": type(None),
}


class JSONSchemaFormatted:
    __type_format_strings__ = {
        Decimal: ("number", "decimal"),
        datetime: ("string", "date-time"),
        date: ("string", "date"),
        time: ("string", "time"),
        timedelta: ("string", "duration"),
        Enum: ("string", "enum"),
        UUID: ("string", "uuid"),
        IPv4Address: ("string", "ipv4"),
        IPv4Interface: ("string", "ipv4-interface"),
        IPv4Network: ("string", "ipv4-network"),
        IPv6Address: ("string", "ipv6"),
        IPv6Interface: ("string", "ipv6-interface"),
        IPv6Network: ("string", "ipv6-network"),
        Path: ("string", "path"),
    }
    __string_type_formats__ = {}
    for k, (t, f) in __type_format_strings__.items():
        __string_type_formats__.setdefault(t, {})
        __string_type_formats__[t][f] = k

    python_type: ClassVar[Type] = Omitted
    schema_type: ClassVar[str] = "string"
    schema_format: ClassVar[str] = Omitted

    @classmethod
    def register(cls, python_type: Type, schema_type: str, schema_format: str):
        if (
            schema_type in cls.__string_type_formats__
            and schema_format in cls.__string_type_formats__[schema_type]
        ):
            raise ValueError(
                f"schema_format {schema_format} for type {schema_type} is already registered to {cls.__string_type_formats__[schema_type][schema_format]}"
            )
        cls.__string_type_formats__.setdefault(schema_type, {})
        cls.__string_type_formats__[schema_type][schema_format] = python_type
        if python_type not in cls.__type_format_strings__:
            cls.__type_format_strings__[python_type] = (schema_type, schema_format)

    @classmethod
    def __init_subclass__(cls, **kwargs):
        super().__init_subclass__(**kwargs)
        if cls.python_type is Omitted:
            cls.python_type = cls
        if not cls.schema_format:
            raise ValueError("schema_format is required")
        cls.register(cls.python_type, cls.schema_type, cls.schema_format)

    @classmethod
    def get_type(
        cls, schema_type: str, schema_format: str, default: AnyType = DoesNotExist
    ) -> Type:
        return cls.__string_type_formats__.get(schema_type, {}).get(
            schema_format, default
        )

    @classmethod
    def __get_pydantic_json_schema__(
        cls, core_schema: core_schema.JsonSchema, handler: GetJsonSchemaHandler
    ) -> JsonSchemaValue:
        json_schema = handler(core_schema)
        json_schema = handler.resolve_ref_schema(json_schema)
        cls.add_to_field_json_schema(json_schema)
        return json_schema

    @classmethod
    def add_to_field_json_schema(cls, json_schema: JsonSchemaValue):
        json_schema.update(type=cls.schema_type, format=cls.schema_format)

    @classmethod
    def validate(cls, value: AnyType) -> AnyType:
        return cls.python_type(value)

    @classmethod
    def __get_pydantic_core_schema__(
        cls, source_type: AnyType, handler: GetCoreSchemaHandler
    ) -> CoreSchema:
        return core_schema.no_info_after_validator_function(
            cls.validate, core_schema.any_schema()
        )
