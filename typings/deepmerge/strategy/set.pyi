"""
This type stub file was generated by pyright.
"""

from .core import StrategyList

class SetStrategies(StrategyList):
    """
    Contains the strategies provided for sets.
    """
    NAME = ...
    @staticmethod
    def strategy_union(config, path, base, nxt):
        """
        use all values in either base or nxt.
        """
        ...
    
    @staticmethod
    def strategy_intersect(config, path, base, nxt):
        """
        use all values in both base and nxt.
        """
        ...
    
    @staticmethod
    def strategy_override(config, path, base, nxt):
        """
        use the set nxt.
        """
        ...
    


