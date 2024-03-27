import os
from typing import Any, Literal, Optional, List
import datetime as dt
from langfuse import Langfuse
from dataclasses import dataclass
from dotenv import load_dotenv

load_dotenv()


@dataclass
class DtaLogConfig:
    url: str
    public_key: str
    secret_key: str


class DtaLog:
    """
    DtaTrace powered by Langfuse
    """

    _config: DtaLogConfig = None

    @classmethod
    def set_keys(cls, *, public_key: str, secret_key: str, url: Optional[str] = None):
        if not cls._config:
            cls._config = DtaLogConfig(
                url=url,
                public_key=public_key,
                secret_key=secret_key,
            )
            return

        if url:
            cls._config.url = url

        if public_key:
            cls._config.public_key = public_key

        if secret_key:
            cls._config.secret_key = secret_key

    @classmethod
    def get_keys(cls, *, config: Optional[DtaLogConfig] = None) -> DtaLogConfig:
        return (
            DtaLogConfig(
                url=config.url if config and config.url else cls._config.url,
                public_key=(
                    config.public_key
                    if config and config.public_key
                    else cls._config.public_key
                ),
                secret_key=(
                    config.secret_key
                    if config and config.secret_key
                    else cls._config.secret_key
                ),
            )
            if config
            else cls._config
        )

    @classmethod
    def _create(cls, *, config: Optional[DtaLogConfig] = None) -> Langfuse:
        use_config = cls.get_keys(config=config)

        return Langfuse(
            host=use_config.url,
            public_key=use_config.public_key,
            secret_key=use_config.secret_key,
        )

    @classmethod
    def score(
        cls,
        *,
        trace_id: str,
        name: str,
        value: float,
        comment: Optional[str] = None,
        config: Optional[DtaLogConfig] = None,
        **kwargs,
    ):
        if not trace_id:
            raise Exception("Score requires trace_id")

        return cls._create(config=config).score(
            **cls._props_not_none(
                name=name, value=value, trace_id=trace_id, comment=comment, **kwargs
            ),
        )

    @classmethod
    def trace(
        cls,
        *,
        config: Optional[DtaLogConfig] = None,
        id: Optional[str] = None,
        session_id: Optional[str] = None,
        name: Optional[str] = None,
        user_id: Optional[str] = None,
        version: Optional[str] = None,
        input: Optional[Any] = None,
        output: Optional[Any] = None,
        metadata: Optional[Any] = None,
        tags: Optional[List[str]] = None,
        **kwargs,
    ):
        return cls._create(config=config).trace(
            **cls._props_not_none(
                id=id,
                session_id=session_id,
                name=name,
                user_id=user_id,
                version=version,
                input=input,
                output=output,
                metadata=metadata,
                tags=cls._process_tags(tags),
                **kwargs,
            ),
        )

    @classmethod
    def event(
        cls,
        *,
        config: Optional[DtaLogConfig] = None,
        id: Optional[str] = None,
        trace_id: Optional[str] = None,
        name: Optional[str] = None,
        start_time: Optional[dt.datetime] = None,
        metadata: Optional[Any] = None,
        input: Optional[Any] = None,
        output: Optional[Any] = None,
        level: Optional[Literal["DEBUG", "DEFAULT", "WARNING", "ERROR"]] = None,
        status_message: Optional[str] = None,
        version: Optional[str] = None,
        **kwargs,
    ):
        return cls._create(config=config).event(
            **cls._props_not_none(
                id=id,
                trace_id=trace_id,
                name=name,
                start_time=start_time,
                metadata=metadata,
                input=input,
                output=output,
                level=level,
                status_message=status_message,
                version=version,
                **kwargs,
            ),
        )

    @classmethod
    def openai(
        cls,
        *,
        config: Optional[DtaLogConfig] = None,
    ):
        from langfuse.openai import openai as lf_openai

        use_config = cls.get_keys(config=config)

        lf_openai.langfuse_public_key = use_config.public_key
        lf_openai.langfuse_secret_key = use_config.secret_key
        lf_openai.langfuse_host = use_config.url

        return lf_openai

    @classmethod
    def openai_flush(cls, dta_openai: Any):
        if dta_openai and hasattr(dta_openai, "flush_langfuse"):
            dta_openai.flush_langfuse()

    @classmethod
    def langchain_handler(cls, config: Optional[DtaLogConfig] = None, **kwargs):
        from langfuse.callback import CallbackHandler

        use_config = cls.get_keys(config=config)

        return CallbackHandler(
            host=use_config.url,
            public_key=use_config.public_key,
            secret_key=use_config.secret_key,
            **kwargs,
        )

    @classmethod
    def _props_not_none(
        cls, *, init_props: dict[str, Any] = {}, **kwargs
    ) -> dict[str, Any]:
        return {
            **{key: value for key, value in init_props.items() if value is not None},
            **{key: value for key, value in kwargs.items() if value is not None},
        }

    @classmethod
    def _process_tags(
        cls,
        tags: List[str] = [],
        init_props: List[str] = [],
    ):
        return list(set((init_props or []) + (tags or []) + ["dta-trace"]))


class DtaTracer(DtaLog):
    _init_props: dict[str, Any]
    _tracer: Any = None
    _instance_config: DtaLogConfig = None

    def __init__(
        self,
        **kwargs,
    ) -> None:
        super().__init__()
        self._init_props = kwargs or {}

    def trace(
        self,
        *,
        id: Optional[str] = None,
        session_id: Optional[str] = None,
        name: Optional[str] = None,
        user_id: Optional[str] = None,
        version: Optional[str] = None,
        input: Optional[Any] = None,
        output: Optional[Any] = None,
        metadata: Optional[Any] = None,
        tags: Optional[List[str]] = None,
        **kwargs,
    ):
        if not self._tracer or (tags and len(tags)):
            self._init_props["tags"] = super()._process_tags(
                tags=tags,
                init_props=(
                    self._init_props["tags"] if "tags" in self._init_props else []
                ),
            )

        if self._tracer:
            return self._tracer.update(
                **super()._props_not_none(
                    init_props=self._init_props,
                    name=name,
                    user_id=user_id,
                    version=version,
                    input=input,
                    output=output,
                    metadata=metadata,
                    **kwargs,
                ),
            )

        self._tracer = super().trace(
            config=self._instance_config,
            **super()._props_not_none(
                init_props=self._init_props,
                id=id,
                session_id=session_id,
                name=name,
                user_id=user_id,
                version=version,
                input=input,
                output=output,
                metadata=metadata,
            ),
        )

        return self._tracer

    def event(
        self,
        *,
        id: Optional[str] = None,
        trace_id: Optional[str] = None,
        name: Optional[str] = None,
        start_time: Optional[dt.datetime] = None,
        metadata: Optional[Any] = None,
        input: Optional[Any] = None,
        output: Optional[Any] = None,
        level: Optional[Literal["DEBUG", "DEFAULT", "WARNING", "ERROR"]] = None,
        status_message: Optional[str] = None,
        version: Optional[str] = None,
        **kwargs,
    ):
        props = super()._props_not_none(
            init_props=self._init_props,
            id=id,
            trace_id=trace_id,
            name=name,
            start_time=start_time,
            metadata=metadata,
            input=input,
            output=output,
            level=level,
            status_message=status_message,
            version=version,
            **kwargs,
        )

        if not self._tracer:
            return super().event(config=self._instance_config, **props)

        return self._tracer.event(**props)

    def score(
        self,
        *,
        name: str,
        value: float,
        trace_id: Optional[str] = None,
        comment: Optional[str] = None,
        **kwargs,
    ):
        props = super()._props_not_none(
            init_props=self._init_props,
            name=name,
            value=value,
            trace_id=trace_id,
            comment=comment,
            **kwargs,
        )
        props.pop("tags", None)

        if not self._tracer:
            return super().score(config=self._instance_config, **props)

        return self._tracer.score(**props)

    def langchain_handler(self, **kwargs):
        """
        Usage example:

        from langchain_openai import ChatOpenAI

        def get_llm (tracer: DtaTracer) -> ChatOpenAI:
            handler = tracer.thread_langchain_handler()

            model = ChatOpenAI(
                temperature=0,
                model=model,
                callbacks=[handler],
            )

            return model
        """

        if not self._tracer:
            raise Exception("Tracer not created")

        return super().langchain_handler(
            config=self._instance_config,
            stateful_client=self._tracer,
            **kwargs,
        )

    def set_keys(self, *, public_key: str, secret_key: str, url: Optional[str] = None):
        if not self._instance_config:
            self._instance_config = DtaLogConfig(
                url=url,
                public_key=public_key,
                secret_key=secret_key,
            )
            return

        if url:
            self._instance_config.url = url

        if public_key:
            self._instance_config.public_key = public_key

        if secret_key:
            self._instance_config.secret_key = secret_key


DTA_LOGS_URL = "https://logs.dta.totvs.ai"

DtaLog.set_keys(
    url=os.environ.get("DTA_LOGS_URL", DTA_LOGS_URL),
    public_key=os.environ.get("DTA_LOGS_PUBLIC_KEY"),
    secret_key=os.environ.get("DTA_LOGS_SECRET_KEY"),
)
