from memento.sql.synchronous.schemas.models import Assistant, Conversation, Message, User
from memento.sql.synchronous.src.repository import Repository
from sqlalchemy.orm import sessionmaker
from typing import Literal, Any


class Manager(Repository):
    def __init__(self, sessionmaker: sessionmaker):
        super().__init__(sessionmaker)

    def register_user(self, name: str) -> int:
        return self.create(User(name=name))

    def register_assistant(
        self,
        name: str,
        system: str,
        model: str | None = None,
        tokens: int | None = None,
    ) -> int:
        return self.create(
            Assistant(
                name=name,
                system=system,
                model=model,
                tokens=tokens,
            )
        )

    def register_conversation(self, user: str, assistant: str) -> int:
        user_instance = self.read(User, name=user)
        assistant_instance = self.read(Assistant, name=assistant)
        if user_instance and assistant_instance:
            return self.create(
                Conversation(user=user_instance.id, assistant=assistant_instance.id)
            )
        else:
            raise ValueError(
                "Could not register conversation because either user or assistant do not exist."
            )

    def commit_message(self, role: str, content: str, conversation: int, augment: str | None = None) -> int:
        return self.create(
            Message(
                role=role,
                content=content,
                augment=augment,
                conversation=conversation,
                prompt={"role": role, "content": content},
            )
        )

    def pull_messages(self, conversation: int) -> list[dict]:
        conversation_instance = self.read(Conversation, id=conversation)
        if conversation_instance is not None:
            messages = [message.prompt for message in conversation_instance.messages]
            return messages
        else:
            raise ValueError(
                "Could not pull messages because conversation does not exist."
            )

    def pull_conversations(
        self, user: str = "user", assistant: str = "assistant"
    ) -> list[int] | None:
        user_instance = self.read(User, name=user)
        assistant_instance = self.read(Assistant, name=assistant)
        if user_instance is not None and assistant_instance is not None:
            conversations = self.read(Conversation, all=True, user=user_instance.id, assistant=assistant_instance.id)
            if conversations:
                return [conversation.id for conversation in conversations]
            else:
                return None
        else:
            raise ValueError(
                "Could not pull conversations because either user or assistant do not exist."
            )

    def delete_user(self, name: str):
        return self.delete(User, name=name)

    def delete_assistant(self, name: str):
        return self.delete(Assistant, name=name)

    def delete_conversation(self, id: int):
        return self.delete(Conversation, id=id)

    def query(
        self,
        model: Literal["Assistant", "Conversation"],
        all: bool = False,
        **kwargs
    ):
        if model == "Assistant":
            return self.read(Assistant, all, **kwargs)
        elif model == "Conversation":
            return self.read(Conversation, all, **kwargs)
        else:
            raise ValueError("Invalid model, only 'Assistant', 'Conversation', 'Message' allowed.")
