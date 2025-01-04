from abc import ABC, abstractmethod
from typing import Any, Mapping, NoReturn

from flask import Response
from flask_restful import abort, output_json, Resource

from response_header import response_header


class BaseResource(Resource, ABC):
    def __init__(self) -> None:
        super().__init__()

    @abstractmethod
    def get(self, *args, **kwargs) -> Response:
        pass

    @abstractmethod
    def post(self, *args, **kwargs) -> Response:
        pass

    @abstractmethod
    def put(self, *args, **kwargs) -> Response:
        pass

    @abstractmethod
    def delete(self, *args, **kwargs) -> Response:
        pass

    def error_response(self, code: int, message: str) -> NoReturn:
        abort(code, status=code, message=message, headers=response_header)
    
    def success_response(self, code: int, data: Mapping[str, Any] | None = None) -> Response:
        if data is None:
            return Response(status=code, headers=response_header)
        return output_json(data=data, code=code, headers=response_header)

