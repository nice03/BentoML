"""
This type stub file was generated by pyright.
"""

from typing import List, Literal, Tuple, Union

from .merger import Merger

DEFAULT_TYPE_SPECIFIC_MERGE_STRATEGIES: List[Tuple[type, Union[Literal["append"], Literal["merge"], Literal["union"]]]] = ...
always_merger: Merger = ...
merge_or_raise: Merger = ...
conservative_merger: Merger = ...
