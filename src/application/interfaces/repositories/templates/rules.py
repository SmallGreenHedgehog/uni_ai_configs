from abc import ABC, abstractmethod

from entities import AgentConfigTemplate


class RulesTemplateRepository(ABC):
    @abstractmethod
    def get_rule_templates(self) -> list[AgentConfigTemplate]: ...
