from typing import List

from fastapi import APIRouter as FastAPIRouter
from fastapi.responses import JSONResponse

HTTP_GET = "GET"
HTTP_POST = "POST"
HTTP_PUT = "PUT"
HTTP_PATCH = "PATCH"
HTTP_DELETE = "DELETE"
HTTP_HEAD = "HEAD"
HTTP_OPTIONS = "OPTIONS"
HTTP_TRACE = "TRACE"
HTTP_CONNECT = "CONNECT"


class APIErrors:

    @staticmethod
    def _405():
        return JSONResponse(
            status_code=405,
            content={"message": "Method Not Allowed"},
        )


class AbstractPathStyle:
    PATHS = {
        HTTP_OPTIONS: "/{id}",
        HTTP_HEAD: "/{id}",
        HTTP_DELETE: "/{id}",
        HTTP_PATCH: "/{id}",
        HTTP_PUT: "/{id}",
        "POST": "/{id}",
        "GET": "/{id}",
    }


class DjangoPathStyle:
    PATHS = {
        HTTP_OPTIONS: "/{pk}",
        HTTP_HEAD: "/{pk}",
        HTTP_DELETE: "/{pk}",
        HTTP_PATCH: "/{pk}",
        HTTP_PUT: "/{pk}",
        "POST": "/{pk}",
        HTTP_GET: "/{pk}",
    }


class UserFrendlyPathStyle:
    PATHS = {
        HTTP_OPTIONS: "/{id}/options",
        HTTP_HEAD: "/{id}/head",
        HTTP_DELETE: "/{id}/delete",
        HTTP_PATCH: "/{id}/edit",
        HTTP_PUT: "/{id}/edit",
        HTTP_POST: "/create",
        HTTP_GET: "/list",
    }


class EndpointsRegister:

    def __init__(self, app, endpoints: List["BaseEndpoint"], generate_head: bool = True, generate_options: bool = True):
        for endpoint in endpoints:
            prefix = endpoint.PREFIX
            tags = endpoint.TAGS
            methods = endpoint.methods
            print(methods)
            router = FastAPIRouter(prefix=prefix, tags=tags)
            for http_method in methods:
                path = endpoint.paths[http_method]
                method = getattr(endpoint, http_method.lower())
                router.add_api_route(methods=[http_method], path=path, endpoint=method)
                if generate_head:
                    router.add_api_route(methods=[HTTP_HEAD], path=path, endpoint=method, include_in_schema=False)
                if generate_options:
                    router.add_api_route(methods=[HTTP_OPTIONS], path=path, endpoint=method, include_in_schema=False)
            app.include_router(router)


class AbstractEndpoint:
    PREFIX: str = None
    TAGS: List[str] = None

    def __init__(self, *args, **kwargs):
        self.methods = []
        self.paths = kwargs.get("paths", UserFrendlyPathStyle).PATHS

    def _get_http_method(self):
        raise NotImplementedError

    def _get_content_type(self):
        raise NotImplementedError

    def set_paths(self, paths_stype: "AbstractPathStyle"):
        self.paths = paths_stype.PATHS


class BaseEndpoint(AbstractEndpoint):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.methods.append(self._get_http_method())

    def _get_content_type(self):
        return JSONResponse.media_type


class GetEndpoint(BaseEndpoint):

    def _get_http_method(self):
        return HTTP_GET

    def _get(self, *args, **kwargs):
        raise NotImplementedError

    def get(self, *args, **kwargs):
        return self._get(*args, **kwargs)


class PostEndpoint(BaseEndpoint):

    def _get_http_method(self):
        return HTTP_POST

    def _post(self, *args, **kwargs):
        raise NotImplementedError

    def post(self, *args, **kwargs):
        return self._post(*args, **kwargs)


class PatchEndpoint(BaseEndpoint):

    def _get_http_method(self):
        return HTTP_PATCH

    def _patch(self, *args, **kwargs):
        raise NotImplementedError

    def patch(self, *args, **kwargs):
        return self.patch(*args, **kwargs)


class PutEndpoint(BaseEndpoint):

    def _get_http_method(self):
        return HTTP_PUT

    def _put(self, *args, **kwargs):
        raise NotImplementedError

    def put(self, *args, **kwargs):
        return self._put(*args, **kwargs)


class DeleteEndpoint(BaseEndpoint):

    def _get_http_method(self):
        return HTTP_DELETE

    def _delete(self, *args, **kwargs):
        raise NotImplementedError

    def delete(self, *args, **kwargs):
        return self._delete(*args, **kwargs)


class OptionsEndpoint(BaseEndpoint):

    def _get_http_method(self):
        return HTTP_OPTIONS

    def _options(self, *args, **kwargs):
        raise NotImplementedError

    def options(self, *args, **kwargs):
        return self._options(*args, **kwargs)


class HeadEndpoint(BaseEndpoint):

    def _get_http_method(self):
        return HTTP_HEAD

    def _head(self, *args, **kwargs):
        raise NotImplementedError

    def head(self, *args, **kwargs):
        return self._head(*args, **kwargs)


class TraceEndpoints(BaseEndpoint):

    def _get_http_method(self):
        return HTTP_TRACE

    def _trace(self, *args, **kwargs):
        raise NotImplementedError

    def trace(self, *args, **kwargs):
        return self._trace(*args, **kwargs)


class AbstractRouter(
    GetEndpoint,
    PostEndpoint,
    PutEndpoint,
    PatchEndpoint,
    DeleteEndpoint,
    HeadEndpoint,
    OptionsEndpoint,
):
    pass


class BaseWebhook(PostEndpoint, HeadEndpoint, OptionsEndpoint):
    pass
