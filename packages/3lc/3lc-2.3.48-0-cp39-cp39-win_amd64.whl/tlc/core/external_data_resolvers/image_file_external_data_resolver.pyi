from tlc.core.external_data_resolver import ExternalDataResolver as ExternalDataResolver
from tlc.core.external_data_resolver_registry import ExternalDataResolverRegistry as ExternalDataResolverRegistry
from tlc.core.object import Object as Object
from tlc.core.schema import Schema as Schema

class ImageFileExternalDataResolver(ExternalDataResolver):
    """
    An external data resolver which will transform an image filename string
    into a 2D array of floating point (R, G, B) values.
    """
    def will_transform_object_property(self, tlc_object: Object, property_name: str) -> bool: ...
    def transform_object_property(self, tlc_object: Object, property_name: str) -> None: ...
    def transform_object_property_schema(self, schema: Schema, property_name: str) -> None: ...
