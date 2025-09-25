from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from fastapi import Request, status
from fastapi.responses import JSONResponse
from fastapi import Request


async def validation_exception_handler(request: Request, exc: RequestValidationError):
    """
    Validation Exception Handler
    """
    first_error = exc.errors()[0] if exc.errors() else None
    details = f"{first_error['loc'][-1]}: {first_error['msg']}" if first_error else "Datos inválidos"

    return JSONResponse(
        status_code=422,
        content={
            "status": "error",
            "error": {
                "code": "INVALID_FORMAT",
                "message": "Formato de mensaje inválido",
                "details": details
            }
        }
    )

class CustomAPIException(Exception):
    def __init__(self, code: str, message: str, details: str = None, http_status: int = status.HTTP_400_BAD_REQUEST):
        self.code = code
        self.message = message
        self.details = details
        self.http_status = http_status

class InvalidFormatException(CustomAPIException):
    def __init__(self, details: str = None):
        super().__init__(
            code="INVALID_FORMAT",
            message="Formato de mensaje inválido",
            details=details,
            http_status=status.HTTP_422_UNPROCESSABLE_ENTITY
        )

class MissingFieldException(CustomAPIException):
    def __init__(self, field_name: str):
        super().__init__(
            code="MISSING_FIELD",
            message="Campo requerido faltante",
            details=f"El campo '{field_name}' es obligatorio",
            http_status=status.HTTP_400_BAD_REQUEST
        )

class InternalServerError(CustomAPIException):
    def __init__(self, details: str = None):
        super().__init__(
            code="SERVER_ERROR",
            message="Error interno del servidor",
            details=details or "Ocurrió un error inesperado",
            http_status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )

async def custom_exception_handler(request: Request,exc: CustomAPIException):
    print(f"CustomAPIException capturada: {exc.code} - {exc.details}")
    return JSONResponse(
        status_code=exc.http_status,
        content={
            "status": "error",
            "error": {
                "code": exc.code,
                "message": exc.message,
                "details": exc.details
            }
        }
    )