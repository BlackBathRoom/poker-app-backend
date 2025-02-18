from json import JSONDecodeError
from typing import Any, Mapping, NoReturn, Optional, Sequence, TypeGuard, TypeVar

from flask import Response, request
from flask.json import loads
from flask_restful import abort, output_json, Resource
from pydantic import BaseModel


T = TypeVar("T")

class BaseResource(Resource):
    def __init__(self) -> None:
        super().__init__()

    def error_response(self, code: int, message: str) -> NoReturn: # type: ignore
        abort(code, status=code, message=message)
    
    def success_response(
        self,
        code: int,
        data: Optional[Mapping[str, Any] | Sequence[Mapping[str, Any]]] = None
    ) -> Response:
        if data is None:
            return Response(status=code)
        return output_json(data=data, code=code)
    
    def request_data_checker(self, data: Any) -> TypeGuard[Mapping[str, Any]]:
        if isinstance(data, Mapping):
            return True
        return False
    
    def request_loader(self) -> Mapping[str, Any]:
        try:
            data = request.data.decode("utf-8")
        except JSONDecodeError:
            self.error_response(400, "Invalid request data")
        if self.request_data_checker(data):
            return data
        else:
            self.error_response(400, "Invalid request data")

    def request_formatter(self, data: Mapping[str, Any], into: type[T]) -> T:
        try:
            return into(**data)
        except Exception as e:
            self.error_response(400, f"Invalid request data: {e}")
