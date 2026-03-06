from typing import Tuple
from aiolimiter import AsyncLimiter

class RateLimiter:
    """
    Ensures that API calls do not exceed the Amazon Creators API rate limits.
    The default is 1 TPS (Transaction Per Second) for the initial 30 days.
    """
    def __init__(self, tps: float = 1.0):
        if tps <= 0:
            raise ValueError("tps must be greater than 0")

        # aiolimiter takes max_rate and time_period.
        # e.g., max_rate=1, time_period=1 => 1 request per 1 second
        self.tps = tps
        max_rate, time_period = limiter_config_from_tps(tps)
        self._limiter = AsyncLimiter(max_rate=max_rate, time_period=time_period)

    async def acquire(self):
        """
        Wait until we have capacity to make a request based on the allowed TPS.
        """
        await self._limiter.acquire()

def limiter_config_from_tps(tps: float) -> Tuple[int, float]:
    """
    Convert TPS to (max_rate, time_period) for aiolimiter.
    For TPS < 1, enforce one request every 1/tps seconds.
    For TPS >= 1, use max_rate requests per second.
    """
    if tps < 1.0:
        return 1, 1.0 / tps
    return int(tps), 1.0
