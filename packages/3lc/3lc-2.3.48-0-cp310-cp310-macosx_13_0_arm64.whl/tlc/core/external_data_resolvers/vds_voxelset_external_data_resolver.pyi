from tlc.core.external_data_resolver import ExternalDataResolver as ExternalDataResolver
from tlc.core.external_data_resolver_registry import ExternalDataResolverRegistry as ExternalDataResolverRegistry
from tlc.core.object import Object as Object
from tlc.core.schema import Schema as Schema

class VdsVoxelsetExternalDataResolver(ExternalDataResolver):
    """
    An external data resolver which will transform a field of this type...

        (VdsIndex, MinX, MinY, MinZ, MaxX, MaxY, MaxZ)

    ... into a 3D array of scalar floating point voxel values.

    MVP2TODO: How is the size of the resulting voxel set encoded?

    Note that the mapping from VdsIndex (a number) to Vds filename (a string) is
    defined in the schema for the relevant column.
    """
    def will_transform_object_property(self, tlc_object: Object, property_name: str) -> bool: ...
    def transform_object_property(self, tlc_object: Object, property_name: str) -> None: ...
    def transform_object_property_schema(self, schema: Schema, property_name: str) -> None: ...
