from sentry_sdk.utils import ContextVar

request_id_contextvar: ContextVar[str] = ContextVar("request_id", default="1")