import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from friendlyeats.constants import FAST_API_APP
from friendlyeats.router import router
from friendlyeats.services.middlewares import CustomHTTPSRedirectMiddleware
from friendlyeats.services.sentry import init_sentry
from friendlyeats.settings import APP_ENV

# Sentry
init_sentry(app=FAST_API_APP)

app = FastAPI()

if APP_ENV != "LOCAL":
    app.add_middleware(CustomHTTPSRedirectMiddleware)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.include_router(router=router)


if __name__ == "__main__":
    uvicorn.run(
        "app:app",
        host="0.0.0.0",
        port=80,
        reload_dirs=["friendlyeats"],
        reload=True,
        workers=1,
    )
