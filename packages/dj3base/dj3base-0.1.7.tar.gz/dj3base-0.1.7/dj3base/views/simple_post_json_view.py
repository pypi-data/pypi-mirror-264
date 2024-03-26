# -*- coding: utf-8 -*-
import abc
import json
from typing import Any, Type, Optional
import inspect

from django.views.generic import View
from django.http import FileResponse
from a3exception.errors import ServerKnownError, ValidationError
from dj3base.views.utils import build_success_response
from a3json_struct.struct import JsonStruct
from a3json_struct.errors import ValidationError as StructValidationError


class SimplePostJsonView(View):
    request_struct_cls: Type[JsonStruct] = None

    def _get_request_json_data(self) -> dict:
        try:
            return json.loads(self.request.body)
        except Exception as e:
            raise ValidationError(f"请求体不是合法的json", cause=str(e))

    def validate_request_permission(self):
        pass

    def validate_request_struct(self) -> Optional[JsonStruct]:
        request_struct = None

        if self.request_struct_cls is not None and inspect.isclass(self.request_struct_cls):
            data = self._get_request_json_data()
            request_struct = self.request_struct_cls(**data)
            try:
                request_struct.full_clean()
            except StructValidationError as e:
                raise ValidationError(str(e))

        return request_struct

    def post(self, *_, **__):
        self.validate_request_permission()
        request_struct = self.validate_request_struct()
        custom_params = self.custom_validate(request_struct)

        result = self.handle_post(request_struct, custom_params)
        if result is None:
            return build_success_response()
        elif isinstance(result, dict):
            return build_success_response(result)
        elif isinstance(result, FileResponse):
            return result
        else:
            raise ServerKnownError(cause=f"handle_post返回值类型未知: {type(result).__name__}")

    def custom_validate(self, request_struct) -> Any:
        pass

    @abc.abstractmethod
    def handle_post(self, request_struct, custom_params: dict):
        raise NotImplementedError()
