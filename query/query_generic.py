from abc import ABC, abstractmethod


class QueryGeneric(ABC):
    @abstractmethod
    def execute(self, **kwargs):
        pass
