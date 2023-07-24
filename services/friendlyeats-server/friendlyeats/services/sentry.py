import sentry_sdk
from sentry_sdk.integrations.fastapi import FastApiIntegration

from friendlyeats.constants import  FAST_API_APP
from friendlyeats.settings import APP_ENV, SENTRY_DSN

integrations_dict: dict = {FAST_API_APP: FastApiIntegration}


def init_sentry(app: str) -> None:
    if APP_ENV == "LOCAL":
        return
    sentry_sdk.init(
        dsn=SENTRY_DSN,
        integrations=[integrations_dict[app]()],
        before_send=lambda x, y: x if APP_ENV == "PRODUCTION" else None,
        attach_stacktrace=True,
        send_default_pii=True,
    )
