from abc import ABC, abstractmethod

from entities import AgentConfigTemplate


class IgnoreTemplateRepository(ABC):
    @abstractmethod
    def get_ignore_templates(self) -> list[AgentConfigTemplate]: ...
