# Original code from DanilZherebtsov, licensed under the MIT License.
# Modifications (2024-03-23) made by Daniel Porsmose.

from rapidgbm.metrics.metric_funcs import regression_metrics, classification_metrics, ClassificationMetrics, RegressionMetrics
import numpy as np
from typing import Callable
from numpy.typing import ArrayLike
import pandas as pd

supported_lgb_metrics_dict: dict = {'mae':'l1',
                              'mse':'l2',
                              'rmse':'rmse',
                              'mape':'mape'}

class MetricHelpers:
    """
    A utility class for handling metrics in RapidGBM.

    This class provides various methods for defining optimization metrics,
    evaluation metrics, pruning metrics, and objective functions based on user input.

    Methods
    -------
    get_optimization_metric_func(eval_metric: str) -> Callable:
        Define optimization metric based on evaluation metric.

    get_evaluation_metric(eval_metric: str) -> Callable:
        Define evaluation metric based on user input.

    get_eval_score(labels: ArrayLike, pred: ArrayLike, eval_metric: str, objective: str) -> float:
        Evaluate model against the evaluation metric.

    get_pruning_metric(eval_metric: str, target_classes: list) -> str:
        Define optimization metric for pruning based on evaluation metric.

    define_objective(metric: str, y: pd.Series) -> str:
        Select an appropriate objective model based on metric and target variable.

    print_lower_greater_better(metric: str) -> str:
        Determine if a metric is lower-better or greater-better.
    """

    @staticmethod
    def get_optimization_metric_func(eval_metric: str) -> Callable:
        """
        Define optimization metric based on evaluation metric (passed by user at __init__).

        Args:
            eval_metric (str): Evaluation metric passed by the user.

        Returns:
            Callable: Optimization metric function.

        Notes:
            - Regression optimization metric is selected based on eval_metric (passed by user at __init__), except for r2.
            - If eval_metric == 'r2', then optimization metric is 'mean_squared_error'.
            - If eval_metric is not in regression_metrics, then optimization metric is 'log_loss'.
        """
        if eval_metric in regression_metrics:
            if eval_metric == 'r2':
                func = globals()["RegressionMetrics"].__dict__['mse']
            else:
                func = globals()["RegressionMetrics"].__dict__[eval_metric]
        else:
            func = globals()["ClassificationMetrics"].__dict__['log_loss']
        return func

    @staticmethod
    def get_evaluation_metric(eval_metric: str) -> Callable:
        """
        Define evaluation (not to be optimized) metric based on user input.

        Args:
            eval_metric (str): Evaluation metric name.

        Returns:
            func (function): Evaluation metric function.
        """
        if eval_metric in regression_metrics:
            func = globals()["RegressionMetrics"].__dict__[eval_metric]
        else:
            func = globals()["ClassificationMetrics"].__dict__[eval_metric]
        return func
    
    @classmethod
    def get_eval_score(cls, 
                       labels: ArrayLike, 
                       pred: ArrayLike, 
                       eval_metric: str, 
                       objective: str) -> float:
        """
        Evaluate model against the eval_metric passed by the user.

        Args:
            cls: The class object.
            labels (ArrayLike): True labels.
            pred (ArrayLike): Predicted labels.
            eval_metric (str): Evaluation metric name.
            objective (str): Training objective: regression/binary/multiclass.

        Returns:
            float: Evaluation score.
        """
        # TODO = tune threshold here
        pred = np.array(pred).astype('float')
        eval_func = cls.get_evaluation_metric(eval_metric)
        if objective == 'binary':
            if eval_metric not in ['auc', 'gini', 'log_loss']:
                pred = (pred > 0.5).astype('int')
        elif objective == 'multiclass':
            if eval_metric not in ['log_loss']:
                pred = np.argmax(pred, axis=1)
        return eval_func(labels, pred)

    @staticmethod
    def get_pruning_metric(eval_metric: str, target_classes: list) -> str:
        """
        Define optimization metric for pruning based on evaluation metric (passed by user)
        and LGBM supported metrics.

        Args:
            eval_metric (str): Evaluation metric passed by the user.
            target_classes (list): Target unique classes.

        Returns:
            str: The optimization metric function.
        """
        if eval_metric in supported_lgb_metrics_dict:
            func = supported_lgb_metrics_dict[eval_metric]
        else:
            if eval_metric in regression_metrics:
                func = 'l2'
            else:
                if len(target_classes) == 2:
                    func = 'binary_logloss'
                else:
                    func = 'multi_logloss'
        return func

    @staticmethod
    def define_objective(metric: str, y: pd.Series) -> str:
        """
        Selects an appropriate objective model based on the given metric and target variable.

        Args:
            metric (str): The name of the metric.
            y (pd.Series): The target variable series.

        Returns:
            str: The objective value for lgbm params.
        """
        if metric in regression_metrics:
            objective = 'regression'
        else:
            if len(set(y)) == 2:
                objective = 'binary'
            else:
                objective = 'multiclass'
        return objective

    @staticmethod
    def print_lower_greater_better(metric: str) -> str:
        """
        Determines whether a metric is lower-better or greater-better.

        Args:
            metric (str): The metric to be evaluated.

        Returns:
            str: 'lower-better' if the metric is in ['mae', 'mse', 'rmse', 'rmsle', 'mape', 'smape', 'rmspe', 'log_loss'],
                'greater-better' otherwise.
        """
        if metric in ['mae', 'mse', 'rmse', 'rmsle', 'mape', 'smape', 'rmspe', 'log_loss']:
            return 'lower-better'
        else:
            return 'greater-better'
