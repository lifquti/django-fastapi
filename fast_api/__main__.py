import uvicorn
from fastapi import Request
from starlette.responses import JSONResponse
from fast_api.misc import app


@app.exception_handler(FileNotFoundError)
async def unicorn_exception_handler(request: Request, exc: FileNotFoundError):
    return JSONResponse(
        status_code=404,
        content={"message": str(exc)},
    )

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=80)
