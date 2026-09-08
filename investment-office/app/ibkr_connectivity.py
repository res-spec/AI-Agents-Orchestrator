import socket
from dataclasses import asdict, dataclass

from .config import Settings


@dataclass
class IBKRConnectivity:
    host: str
    port: int
    reachable: bool
    message: str

    def as_dict(self) -> dict:
        return asdict(self)


def probe_tws(settings: Settings, *, live: bool = False, timeout: float = 1.5) -> IBKRConnectivity:
    """Check whether TWS/IB Gateway is listening on the configured socket.

    This only proves that a TCP listener is reachable. It does not authenticate,
    request account data, or place an order. The official IBKR TWS API client is
    wired in a later step after the local API package is installed and paper
    connectivity is verified.
    """

    port = settings.ibkr_live_port if live else settings.ibkr_paper_port
    try:
        with socket.create_connection((settings.ibkr_host, port), timeout=timeout):
            return IBKRConnectivity(
                host=settings.ibkr_host,
                port=port,
                reachable=True,
                message="TWS socket is reachable.",
            )
    except OSError as exc:
        return IBKRConnectivity(
            host=settings.ibkr_host,
            port=port,
            reachable=False,
            message=f"TWS socket is not reachable: {exc}",
        )
