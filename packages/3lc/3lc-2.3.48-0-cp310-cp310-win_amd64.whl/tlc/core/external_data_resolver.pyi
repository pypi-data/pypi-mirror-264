import abc
from abc import ABC, abstractmethod
from tlc.core.object import Object as Object
from tlc.core.schema import Schema as Schema

class ExternalDataResolver(ABC, metaclass=abc.ABCMeta):
    """
    The base class for all external data resolvers.

    These are objects which can transform a table row (typically a training example)
    from its literal contents into its final form required for e.g. performing
    ML training.

    A typical sample would be an image filename (the literal contents) which is
    transformed into an actual image (the external data which is pulled in).
    """
    @abstractmethod
    def will_transform_object_property(self, tlc_object: Object, property_name: str) -> bool:
        """
        Indicates whether this external data resolver will want to transform a single,
        named property within an object.

        The decision is based solely on the schema of the object.
        """
    @abstractmethod
    def transform_object_property(self, tlc_object: Object, property_name: str) -> None:
        """
        Transforms a single property within an object from its literal value into
        the actual representation used by e.g. ML training
        """
    @abstractmethod
    def transform_object_property_schema(self, schema: Schema, property_name: str) -> None:
        """
        Transforms a single property within a schema from its literal description into
        a schema describing what the property will look like after a transform has
        taken place
        """
