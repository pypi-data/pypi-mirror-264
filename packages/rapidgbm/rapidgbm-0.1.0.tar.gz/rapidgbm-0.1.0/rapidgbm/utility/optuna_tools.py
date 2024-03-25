# Original code from DanilZherebtsov, licensed under the MIT License.
# Modifications (2024-03-23) made by Daniel Porsmose.

from enum import Enum, unique
from typing import Union

# define optuna distribution pattern for params
@unique
class Distribution(int, Enum):
    CHOICE = 0
    UNIFORM = 1
    INTUNIFORM = 2
    QUNIFORM = 3
    LOGUNIFORM = 4
    DISCRETEUNIFORM = 5
    NORMAL = 6
    QNORMAL = 7
    LOGNORMAL = 8

OPTUNA_DISTRIBUTIONS_MAP : dict = {Distribution.CHOICE: "suggest_categorical",
                                   Distribution.UNIFORM: "suggest_uniform",
                                   Distribution.LOGUNIFORM: "suggest_loguniform",
                                   Distribution.INTUNIFORM: "suggest_int",
                                   Distribution.DISCRETEUNIFORM: "suggest_discrete_uniform"}

class SearchSpace:
    """
    Represents a search space for hyperparameter optimization using Optuna.

    Attributes:
        distribution_type (Union[Distribution, None]): The type of distribution to use for sampling.
        params (dict): Additional parameters for the search space.
    """

    distribution_type: Union[Distribution, None] = None
    params: dict = {}

    def __init__(self, distribution_type: Distribution, *args, **kwargs) -> None:
        """
        Initializes a new instance of the SearchSpace class.

        Args:
            distribution_type (Distribution): The type of distribution to use for sampling.
            *args: Additional positional arguments.
            **kwargs: Additional keyword arguments.
        """
        self.distribution_type = distribution_type
        self.params = kwargs