from abc import ABC
from tlc.core.external_data_resolver import ExternalDataResolver as ExternalDataResolver
from typing import Type

class ExternalDataResolverRegistry(ABC):
    """Maintains a list of currently registered ExternalDataResolvers."""
    @staticmethod
    def register_external_data_resolver(external_data_resolver_type: Type[ExternalDataResolver]) -> None:
        """
        Register an external data resolver in the global registry
        """
    @staticmethod
    def print_external_data_resolvers(line_prefix: str = '') -> None:
        """
        Print all external data resolvers.
        """
