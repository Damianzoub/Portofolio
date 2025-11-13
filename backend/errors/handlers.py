from fastapi import Request
from fastapi.responses import JSONResponse
from fastapi.exceptions import HTTPException

async def http_404_handler(request: Request, exc: HTTPException):
    return JSONResponse(
        status_code=404,
        content={"error": "Resource not found"}
    )

async def http_500_handler(request: Request,exc: Exception):
    return JSONResponse(
        status_code=500,
        content={"error":"Internal Server Error"}
    )

async def http_403_handler(request: Request, exc: HTTPException):
    return JSONResponse(
        status_code=403,
        content={"error":"Forbidden access"}
    )



