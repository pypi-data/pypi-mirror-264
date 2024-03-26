import os
from dotenv import load_dotenv
from typing import Any, Optional
from dataclasses import dataclass

load_dotenv()


@dataclass
class DtaProxyConfig:
    url: str
    key: str


class DtaProxy:

    _config: DtaProxyConfig = None

    @classmethod
    def set_keys(cls, *, key: str, url: Optional[str] = None):
        if not cls._config:
            cls._config = DtaProxyConfig(
                url=url,
                key=key,
            )
            return

        if url:
            cls._config.url = url

        if key:
            cls._config.key = key

    @classmethod
    def get_keys(cls, *, config: Optional[DtaProxyConfig] = None) -> DtaProxyConfig:
        return (
            DtaProxyConfig(
                url=config.url if config and config.url else cls._config.url,
                key=(config.key if config and config.key else cls._config.key),
            )
            if config
            else cls._config
        )

    @classmethod
    def url(cls) -> str:
        return cls._config.url

    @classmethod
    def key(cls) -> str:
        value = cls._config.key

        if not value:
            raise Exception("Environment var DTA_PROXY_KEY not found")

        return value

    @classmethod
    def openai_client(
        cls, *, openai: Optional[Any] = None, config: Optional[DtaProxyConfig] = None
    ):
        if not openai:
            import openai

        use_config = cls.get_keys(config=config)

        return openai.OpenAI(
            api_key=use_config.key,
            base_url=use_config.url,
        )


DTA_PROXY_URL = "https://proxy.dta.totvs.ai"

DtaProxy.set_keys(
    url=os.environ.get("DTA_PROXY_URL", DTA_PROXY_URL),
    key=os.environ.get("DTA_PROXY_KEY"),
)
