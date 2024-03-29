import platform

from automizor import version

OS_SYSTEM, OS_RELEASE, OS_VERSION = platform.system_alias(
    platform.system(), platform.release(), platform.version()
)


def get_headers(token: str) -> dict:
    return {
        "Authorization": f"Token {token}",
        "User-Agent": f"Automizor/{version} ({OS_SYSTEM} {OS_RELEASE}) {OS_VERSION}",
    }
