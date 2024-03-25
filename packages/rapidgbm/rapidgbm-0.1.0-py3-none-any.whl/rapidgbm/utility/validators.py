# Original code from DanilZherebtsov, licensed under the MIT License.
# Modifications (2024-03-23) made by Daniel Porsmose.

import pandas as pd
import numpy as np

class Validators:
    """
    A collection of static methods for validating arguments.

    Methods:
        validate_features_argument(value: pd.DataFrame) -> None:
            Validates the features argument.

        validate_target_argument(value: pd.Series) -> None:
            Validates the target argument.

        validate_threshold_argument(value: float) -> None:
            Validates the threshold argument.

        validate_plotting_legend_argument(value: bool) -> None:
            Validates the legend argument.

        validate_plot_importances_n_features_argument(value: int) -> None:
            Validates the n_features argument for plotting importances.

        validate_plot_importances_figsize_argument(value: tuple) -> None:
            Validates the figsize argument for plotting importances.

        validate_numpy_ndarray_arguments(value: np.ndarray) -> None:
            Validates the arguments for the fit_optimized() function.
    """

    @staticmethod
    def validate_features_argument(value: pd.DataFrame) -> None:
        """
        Validates the features argument.

        Args:
            value (pd.DataFrame): The features data.

        Raises:
            TypeError: If value is not a pandas DataFrame.
            Exception: If value is an empty DataFrame.
        """
        if not isinstance(value, pd.DataFrame): 
            raise TypeError('X (features) must be a pandas DataFrame')
        if len(value) == 0:
            raise Exception('X (features) must contain data')

    @staticmethod
    def validate_target_argument(value: pd.Series) -> None:
        """
        Validates the target argument.

        Args:
            value (pd.Series): The target variable.

        Raises:
            TypeError: If value is not a pandas Series.
            Exception: If value is an empty Series.
        """
        if not isinstance(value, pd.Series):
            raise TypeError('y (target variable) must be a pandas Series')
        if len(value) == 0:
            raise Exception('X (features) must contain data')

    @staticmethod
    def validate_threshold_argument(value: float) -> None:
        """
        Validates the threshold argument.

        Args:
            value (float): The threshold value.

        Raises:
            TypeError: If value is not a float.
            ValueError: If value is not within the range (0, 1).
        """
        if not isinstance(value, float):
            raise TypeError('threshold must be a float')
        if not 0 < value < 1:
            raise ValueError('threshold must can take values 0 < threshold < 1')

    @staticmethod
    def validate_plotting_legend_argument(value: bool) -> None:
        """
        Validates the legend argument.

        Args:
            value (bool): The legend argument.

        Raises:
            TypeError: If value is not a bool.
        """
        if not isinstance(value, bool):
            raise TypeError('legent argument can be True/False')

    @staticmethod
    def validate_plot_importances_n_features_argument(value: int) -> None:
        """
        Validates the n_features argument for plotting importances.

        Args:
            value (int): The n_features argument.

        Raises:
            TypeError: If value is not an int.
            ValueError: If value is not a positive integer.
        """
        if not isinstance(value, int):
            raise TypeError('n_features argument must be of type int')        
        if value <= 0:
            raise ValueError('n_features argument must be positive')
            
    @staticmethod
    def validate_plot_importances_figsize_argument(value: tuple) -> None:
        """
        Validates the figsize argument for plotting importances.

        Args:
            value (tuple): The figsize argument.

        Raises:
            TypeError: If value is not a tuple.
            ValueError: If value does not contain two values or if any value is not positive.
        """
        if not isinstance(value, tuple):
            raise TypeError('figsize argument must be a tuple. E.g. (15,10)')
        if len(value) != 2:
            raise ValueError('figsize must contain two values. E.g. (15,10)')
        if np.any([val <= 0 for val in value]):
            raise ValueError('figsize must contain two positive values. E.g. (15,10)')

    @staticmethod
    def validate_numpy_ndarray_arguments(value: np.ndarray) -> None:
        """
        Validates the arguments for the fit_optimized() function.

        Args:
            value (np.ndarray): The arguments.

        Raises:
            TypeError: If value is not a numpy array.
        """
        if not isinstance(value, np.ndarray):
            raise TypeError('Arguments to fit_optimized() must be of type numpy.array')