import asyncio
from typing import Optional
from aiolimiter import AsyncLimiter

class RateLimiter:
    """
    Ensures that API calls do not exceed the Amazon Creators API rate limits.
    The default is 1 TPS (Transaction Per Second) for the initial 30 days.
    """
    def __init__(self, tps: float = 1.0):
        # aiolimiter takes max_rate and time_period.
        # e.g., max_rate=1, time_period=1 => 1 request per 1 second
        self.tps = tps
        self._limiter = AsyncLimiter(max_rate=max_rate_from_tps(tps), time_period=1.0)

    async def acquire(self):
        """
        Wait until we have capacity to make a request based on the allowed TPS.
        """
        await self._limiter.acquire()

def max_rate_from_tps(tps: float) -> int:
    """
    Helper to convert float TPS to a valid max_rate for aiolimiter.
    If tps < 1 (e.g. 0.5), we could do 1 request every 2 seconds.
    But aiolimiter works best with max_rate requests per time_period.
    For simplicity, if tps is 1.0, max_rate is 1.
    If tps is 10.0, max_rate is 10.
    """
    return max(1, int(tps))
