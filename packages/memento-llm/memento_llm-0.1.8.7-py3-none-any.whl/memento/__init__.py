from memento.nosql import NoSQLMemory, AsyncNoSQLMemory
from memento.sql import SQLMemory, AsyncSQLMemory
from typing import Any, Callable


class Memento(SQLMemory):
    def __init__(self, connection: str = "sqlite:///:memory:", **kwargs):
        super().__init__(connection, **kwargs)

    @staticmethod
    def nosql(connection: str) -> NoSQLMemory:
        return NoSQLMemory.create(connection)

    @classmethod
    def patch(
        cls,
        connection: str,
        nosql: bool = False,
        stream: bool = False,
        openai: Any | None = None,
        function: Callable | None = None,
        template_factory: Callable | None = None,
    ):
        memento = Memento.nosql(connection) if nosql else Memento(connection)

        if openai:
            func = openai.chat.completions.create
            openai.chat.completions.create = memento(
                    func, stream=stream, template_factory=template_factory
                )
            return openai, memento
        elif function:
            function = memento(
                function, stream=stream, template_factory=template_factory
            )
            return function, memento
        else:
            raise ValueError("Either OpenAI client or generation function required.")


class AsyncMemento(AsyncSQLMemory):
    def __init__(self, connection: str = "sqlite:///:memory:", **kwargs):
        super().__init__(connection, **kwargs)

    @staticmethod
    def nosql(connection: str) -> AsyncNoSQLMemory:
        return AsyncNoSQLMemory.create(connection)

    @classmethod
    def patch(
        cls,
        connection: str,
        nosql: bool = False,
        stream: bool = False,
        openai: Any | None = None,
        function: Callable | None = None,
        template_factory: Callable | None = None,
    ):
        memento = AsyncMemento.nosql(connection) if nosql else AsyncMemento(connection)

        if openai:
            func = openai.chat.completions.create
            openai.chat.completions.create = memento(
                    func, stream=stream, template_factory=template_factory
                )
            return openai, memento
        elif function:
            function = memento(
                function, stream=stream, template_factory=template_factory
            )
            return function, memento
        else:
            raise ValueError("Either OpenAI client or generation function required.")
