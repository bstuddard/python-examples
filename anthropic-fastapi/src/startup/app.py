from fastapi import FastAPI, Request, HTTPException, status
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware

# Start up app
app = FastAPI()

# Only only specific origins
app.add_middleware(
    CORSMiddleware,
    allow_origin_regex="https?://localhost(:\d+)?", # Could add other sites as needed |^https://dev--\.netlify\.app$
    allow_credentials=True,
    allow_methods=["GET","POST"],
    allow_headers=[
        "Content-Type",
        "Authorization",
        "Accept",
        "Origin",
        "X-Requested-With"
    ],
)


@app.middleware('http')
async def validate_referer(request: Request, call_next):

    # Check Referer
    approved_referers = ['http://localhost:8000/', 'http://localhost:8080/', 'http://localhost:5173/'] # Could later add 'https://xxx.netlify.app/', 'https://xxx.azurewebsites.net/'
    referer = request.headers.get('referer')
    if referer:
        if not any(referer.startswith(approved_referer) for approved_referer in approved_referers):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Not Authorized",
                headers={"WWW-Authenticate": "Bearer"}
            )
    
    response = await call_next(request)
    return response

""" # Enable if db is needed
from src.startup.database import create_pool, close_pool

@app.on_event("startup")
async def startup():
    await create_pool()


@app.on_event("shutdown")
async def shutdown():
    await close_pool()
"""