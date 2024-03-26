from _typeshed import Incomplete
from tlc.core.external_data_resolver import ExternalDataResolver as ExternalDataResolver
from tlc.core.external_data_resolver_registry import ExternalDataResolverRegistry as ExternalDataResolverRegistry
from tlc.core.object import Object as Object
from tlc.core.schema import Schema as Schema

class _VdsImageExternalDataSchema:
    vds_index_property_schema: Incomplete
    min_x_property_schema: Incomplete
    min_y_property_schema: Incomplete
    max_x_property_schema: Incomplete
    max_y_property_schema: Incomplete
    z_property_schema: Incomplete
    def __init__(self, vds_index_property_schema: Schema, min_x_property_schema: Schema, min_y_property_schema: Schema, max_x_property_schema: Schema, max_y_property_schema: Schema, z_property_schema: Schema) -> None: ...

class VdsImageExternalDataResolver(ExternalDataResolver):
    """
    An external data resolver which will transform a column of this type...

        (VdsIndex, MinX, MinY, MaxX, MaxY, Z)

    ... into a 2D array of floating point (R, G, B) values.

    Note that the mapping from VdsIndex (a number) to Vds filename (a string) is
    defined in the schema for the relevant column.
    """
    def will_transform_object_property(self, tlc_object: Object, property_name: str) -> bool: ...
    def transform_object_property(self, tlc_object: Object, property_name: str) -> None: ...
    def transform_object_property_schema(self, schema: Schema, property_name: str) -> None: ...
