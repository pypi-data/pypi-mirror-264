from _typeshed import Incomplete
from tlc.core.objects.tables.from_table.filtered_table_criteria.filter_criterion import ColumnFilterCriterion as ColumnFilterCriterion, FilterCriterion as FilterCriterion
from tlc.core.schema import BoolValue as BoolValue, Schema as Schema
from typing import Any, Mapping

class BoolFilterCriterion(ColumnFilterCriterion):
    """A BoolFilterCriterion is a predicate that can be applied to an object's attribute to determine whether the
    object matches the criterion.

    Args:
        attribute (str): The name of the attribute to which the criterion applies.
        bool_value (bool): The boolean value to match.


    """
    bool_value: Incomplete
    def __init__(self, attribute: str | None = None, bool_value: bool | None = None, init_parameters: Any = None) -> None: ...
    @staticmethod
    def from_any(any_filter_criterion: Mapping | FilterCriterion) -> BoolFilterCriterion: ...
