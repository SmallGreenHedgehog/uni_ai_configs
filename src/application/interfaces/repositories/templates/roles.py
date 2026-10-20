from abc import ABC, abstractmethod

from entities import AgentConfigTemplate


class RolesTemplateRepository(ABC):
    @abstractmethod
    def get_role_templates(self) -> list[AgentConfigTemplate]: ...
