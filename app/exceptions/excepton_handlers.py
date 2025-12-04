from fastapi import Request, status
from fastapi.responses import JSONResponse
from fastapi import APIRouter
import logging

from app.exceptions.errors import NoLongUrlFoundError, SlugAlreadyExistsError 

exception_router = APIRouter()
logging.basicConfig(level=logging.INFO)


@exception_router.exception_handler(NoLongUrlFoundError)
async def not_found_handler(request: Request, exc: NoLongUrlFoundError):
    return JSONResponse(
        status_code=status.HTTP_404_NOT_FOUND,
        content={"detail": "Link not found", "error_code": "NOT_FOUND"}
    )

@exception_router.exception_handler(SlugAlreadyExistsError)
async def conflict_handler(request: Request, exc: SlugAlreadyExistsError):
    return JSONResponse(
        status_code=status.HTTP_409_CONFLICT,
        content={"detail": "Could not generate unique link. Try again.", "error_code": "SLUG_CONFLICT"}
    )

@exception_router.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    logging.error(f"Unhandled error occurred: {exc}", exc_info=True)
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={"detail": "Internal server error. Server administrator has been notified."}
    )