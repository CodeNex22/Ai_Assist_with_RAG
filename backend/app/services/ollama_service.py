import httpx

from app.core.config import settings
from app.core.logging import get_logger

logger = get_logger(__name__)


class OllamaService:
    def __init__(self, timeout: float = 300.0) -> None:
        self.base_url = settings.ollama_url.rstrip("/")

        timeout_config = httpx.Timeout(
            connect=30.0,
            read=300.0,
            write=300.0,
            pool=300.0,
        )

        self.client = httpx.AsyncClient(timeout=timeout_config)

    async def generate(self, prompt: str, *, model: str | None = None) -> str:
        payload = {
            "model": model or settings.ollama_model,
            "prompt": prompt,
            "stream": False,
            "keep_alive": "30m",
            "options": {
                "temperature": settings.temperature,
                "num_predict": settings.max_tokens,
            },
        }

        try:
            response = await self.client.post(
                f"{self.base_url}/api/generate",
                json=payload,
            )

            response.raise_for_status()

            data = response.json()

            return data.get("response", "")

        except httpx.TimeoutException as exc:
            logger.error("Ollama request timed out", error=str(exc))
            raise RuntimeError(
                "Ollama timed out while generating a response."
            ) from exc

        except httpx.HTTPStatusError as exc:
            logger.error(
                "Ollama returned an HTTP error",
                status=exc.response.status_code,
                body=exc.response.text,
            )
            raise RuntimeError(
                f"Ollama returned HTTP {exc.response.status_code}"
            ) from exc

        except httpx.HTTPError as exc:
            logger.error("Ollama request failed", error=str(exc))
            raise RuntimeError("Ollama is unavailable") from exc

    async def embed(self, text: str, *, model: str | None = None) -> list[float]:
        payload = {
            "model": model or settings.embedding_model,
            "input": text,
            "keep_alive": "30m",
        }

        try:
            response = await self.client.post(
                f"{self.base_url}/api/embeddings",
                json=payload,
            )

            response.raise_for_status()

            data = response.json()

            return data.get("embedding", [])

        except httpx.TimeoutException as exc:
            logger.error("Embedding request timed out", error=str(exc))
            raise RuntimeError(
                "Embedding request timed out."
            ) from exc

        except httpx.HTTPStatusError as exc:
            logger.error(
                "Embedding endpoint returned an HTTP error",
                status=exc.response.status_code,
                body=exc.response.text,
            )
            raise RuntimeError(
                f"Embedding endpoint returned HTTP {exc.response.status_code}"
            ) from exc

        except httpx.HTTPError as exc:
            logger.error("Embedding request failed", error=str(exc))
            raise RuntimeError(
                "Embedding service is unavailable"
            ) from exc

    async def close(self) -> None:
        await self.client.aclose()