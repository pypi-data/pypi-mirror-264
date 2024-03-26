from datetime import datetime
from fastapi.responses import JSONResponse
import pkg_resources


def get_expiration_date_from_version(package_name):
    version = pkg_resources.get_distribution(package_name).version
    year, month, day = map(int, version.split("."))
    # Adjust the year to include the century (assuming 2000s)
    year += 2000
    return datetime(year, month, day)


def python_runtime(package_name):
    expiration_date = get_expiration_date_from_version(package_name)

    def middleware(app):
        async def before_request(scope, receive, send):
            if datetime.now() > expiration_date:
                response = JSONResponse(
                    status_code=403,
                    content={"message": "This service is no longer available."},
                )
                await response(scope, receive, send)
                return
            await app(scope, receive, send)

        return before_request

    return middleware
