from fastapi import HTTPException, status
from typing import Any


class _HTTPAny(HTTPException):
    status_code = None
    def __init__(
        self,
        detail: Any = None,
        headers: dict[str, Any] | None = None,
    ) -> None:
        super().__init__(
            status_code=self.status_code,
            detail=detail,
            headers=headers
        )


class HTTP500(_HTTPAny):
    status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
    

class HTTP400(_HTTPAny):
    status_code = status.HTTP_400_BAD_REQUEST


class HTTP401(_HTTPAny):
    status_code = 401
