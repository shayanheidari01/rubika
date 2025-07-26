import asyncio
import time


async def tcping(host: str, port: int, timeout: float = 3.0) -> dict:
    """
    Performs an asynchronous TCP ping to the given host and port.
    Returns a dictionary with status and latency (in ms if up).
    """
    start = time.perf_counter()
    try:
        reader, writer = await asyncio.wait_for(
            asyncio.open_connection(host, port), timeout=timeout
        )
        latency = (time.perf_counter() - start) * 1000  # ms
        writer.close()
        await writer.wait_closed()
        return {"status": "up", "latency_ms": round(latency, 2)}
    except Exception:
        return {"status": "down", "latency_ms": None}