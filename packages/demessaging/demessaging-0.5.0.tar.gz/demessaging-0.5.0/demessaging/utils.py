"""Utilities for the demessaging module."""

# SPDX-FileCopyrightText: 2019-2024 Helmholtz Centre Potsdam GFZ German Research Centre for Geosciences
# SPDX-FileCopyrightText: 2020-2021 Helmholtz-Zentrum Geesthacht GmbH
# SPDX-FileCopyrightText: 2021-2024 Helmholtz-Zentrum hereon GmbH
#
# SPDX-License-Identifier: Apache-2.0

import inspect
import textwrap
from typing import Any, Type

from pydantic import BaseModel


def type_to_string(type_: Any):
    if inspect.isclass(type_):
        return object_to_string(type_)
    else:
        return str(type_)


def object_to_string(obj: Any):
    if obj.__module__ == "builtins":
        return obj.__name__
    return f"{obj.__module__}.{obj.__name__}"


def build_parameter_docs(model: Type[BaseModel]) -> str:
    """Build the docstring for the parameters of a model."""
    docstring = "\n\nParameters\n----------"
    for fieldname, field_info in model.model_fields.items():
        param_doc = textwrap.dedent(
            f"""
            {fieldname} : {type_to_string(field_info.annotation)}
                {field_info.description}
            """
        )
        docstring = docstring + param_doc.rstrip()
    return docstring


def append_parameter_docs(model: Type[BaseModel]) -> Type[BaseModel]:
    """Append the parameters section to the docstring of a model."""
    docstring = build_parameter_docs(model)
    model.__doc__ += docstring  # type: ignore
    return model
