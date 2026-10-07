import httpx
import logging
from typing import Any

logger = logging.getLogger(__name__)


class RequestMaker:
    @staticmethod
    async def request(method: str,url: str,headers: dict[str, str] | None = None,params: dict[str, Any] | None = None,json_body: dict[str, Any] | None = None,data: dict[str, Any] | None = None,timeout: float = 10.0):
        try:
            async with httpx.AsyncClient(timeout=timeout) as client:
                response = await client.request(
                    method=method,
                    url=url,
                    headers=headers,
                    params=params,
                    json=json_body,
                    data=data,
                )

            response.raise_for_status()
            return response.json()

        except httpx.HTTPStatusError as error:
            logger.error(
                "HTTP error occurred: %s - %s",
                error.response.status_code,
                error.response.text,
            )
            return None

        except httpx.RequestError as error:
            logger.error("Request error occurred: %s", error)
            return None