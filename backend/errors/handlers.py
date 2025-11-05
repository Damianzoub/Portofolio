from fastapi import Request

async def http_404_handler(request: Request, exc):
    return {"error": "Resource not fonud"}

async def http_500_handler(request: Request,exc):
    return {"error": "Internal server error"}

async def http_403_handler(rquest: Request,exc):
    return {"error": "Forbidden access"}