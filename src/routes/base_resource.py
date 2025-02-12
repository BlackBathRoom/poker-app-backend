from json import JSONDecodeError
from typing import Any, Mapping, NoReturn, Optional, Sequence, TypeGuard

from flask import Response, request
from flask.json import loads
from flask_restful import abort, output_json, Resource


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
    
    def request_loader(self) -> Any:
        try:
            data = request.data.decode("utf-8")
        except JSONDecodeError:
            self.error_response(400, "Invalid request data")
        return loads(data)

