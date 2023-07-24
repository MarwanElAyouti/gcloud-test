from starlette.datastructures import URL
from starlette.responses import RedirectResponse
from starlette.types import ASGIApp, Receive, Scope, Send


class CustomHTTPSRedirectMiddleware:
    # Source: fastapi.middleware.httpsredirect
    def __init__(self, app: ASGIApp) -> None:
        self.app = app
        self.redirect_scheme = {"http": "https"}
        self.excepted_paths = ["/health"]

    async def __call__(self, scope: Scope, receive: Receive, send: Send) -> None:
        path = scope.get("path", None)

        if (
            path is not None
            and path not in self.excepted_paths
            and scope["type"] == "http"
            and scope["scheme"] == "http"
        ):
            url = URL(scope=scope)
            netloc = url.hostname if url.port in (80, 443) else url.netloc
            url = url.replace(scheme=self.redirect_scheme[url.scheme], netloc=netloc)
            response = RedirectResponse(url, status_code=307)
            await response(scope, receive, send)
        else:
            await self.app(scope, receive, send)
