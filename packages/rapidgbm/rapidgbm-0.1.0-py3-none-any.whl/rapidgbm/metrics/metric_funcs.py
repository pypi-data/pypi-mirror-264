# Created on Fri Mar 11 20:34:45 2022
# Original code from DanilZherebtsov, licensed under the MIT License.
# Modifications (2024-03-23) made by Daniel Porsmose.

import numpy as np
import pandas as pd
from typing import Any, Union
ArrayLike = Union[pd.DataFrame, pd.Series, np.ndarray, list, tuple]
from sklearn.metrics import mean_absolute_error as mae
from sklearn.metrics import mean_squared_error as mse
from sklearn.metrics import mean_squared_log_error as msle
from sklearn.metrics import r2_score as r2
from sklearn.metrics import roc_auc_score as auc
from sklearn.metrics import accuracy_score as accuracy
from sklearn.metrics import balanced_accuracy_score as balanced_accuracy
from sklearn.metrics import precision_score as precision
from sklearn.metrics import recall_score as recall
from sklearn.metrics import f1_score as f1
from sklearn.metrics import log_loss
# define mape manually for users without sklearn==1.0.1 (mape not included in prior versions)
try:
    from sklearn.metrics import mean_absolute_percentage_error as mape
except:
    def mape(y_true: ArrayLike, y_pred: ArrayLike) -> Union[float, ArrayLike]: 
        """
        Calculate the Mean Absolute Percentage Error (MAPE) between the true and predicted values.

        Parameters
            ----------
            y_true (ArrayLike): The true values.
            y_pred (ArrayLike): The predicted values.

        Returns
        _______
            Union[float, ArrayLike]: The MAPE value(s).
        """
        y_true, y_pred = np.array(y_true), np.array(y_pred)
        return np.mean(np.abs((y_true - y_pred) / y_true))
    

EPSILON: float = 1e-10

regression_metrics: list = ['mae', 'mse', 'rmse', 'rmsle', 'mape', 'smape', 'rmspe', 'r2']

classification_metrics: list = ['auc', 'gini', 'log_loss', 
                          'accuracy', 'balanced_accuracy',
                          'precision', 'precision_weighted', 'precision_macro',
                          'recall', 'recall_weighted', 'recall_macro',
                          'f1', 'f1_weighted', 'f1_macro']

supported_metrics: list = list(set(regression_metrics + classification_metrics))

class RegressionMetrics:
    @staticmethod
    def mae(real: ArrayLike, pred: ArrayLike) -> Union[float, ArrayLike]:
        """
        Calculate the mean absolute error (MAE) between the real and predicted values.

        Args:
            real (ArrayLike): The real values.
            pred (ArrayLike): The predicted values.

        Returns:
            Union[float, ArrayLike]: The mean absolute error.

        Raises:
            None

        Examples:
            >>> mae([1, 2, 3], [2, 3, 4])
            1.0
        """
        return mae(real, pred)

    @staticmethod
    def mse(real: ArrayLike, pred: ArrayLike) -> Union[float, ArrayLike]:
        """
        Calculate the mean squared error (MSE) between the real and predicted values.

        Args:
            real (ArrayLike): The real values.
            pred (ArrayLike): The predicted values.

        Returns:
            Union[float, ArrayLike]: The mean squared error between the real and predicted values.
        """
        return mse(real, pred)
    
    @staticmethod
    def rmse(real: ArrayLike, pred: ArrayLike) -> Union[float, ArrayLike]:
        """
        Calculate the root mean squared error (RMSE) between the real and predicted values.

        Args:
            real (ArrayLike): The real values.
            pred (ArrayLike): The predicted values.

        Returns:
            Union[float, ArrayLike]: The root mean squared error between the real and predicted values.
        """
        return mse(real, pred, squared=False)

    @staticmethod
    def rmsle(cls, real: ArrayLike, pred: ArrayLike) -> Union[float, ArrayLike]:
        """
        Calculate the root mean squared log error (RMSLE) between the real and predicted values.
        Changes negative predictions to 0 for correct calculation of RMSLE
        
        Parameters:
            real (ArrayLike): The real values.
            pred (ArrayLike): The predicted values.
                    
        Returns:
            Union[float, ArrayLike]: The root mean squared log error between the real and predicted values.
        """
        try:
            return msle(real, pred, squared=False)
        except ValueError:
            pred_non_negative, real_non_negative = cls._remove_negatives(pred, real)
            return msle(real_non_negative, pred_non_negative, squared=False)
    
    @staticmethod
    def smape(real: ArrayLike, pred: ArrayLike) -> Union[float, ArrayLike]:
        """
        Calculates the Symmetric Mean Absolute Percentage Error (SMAPE) between the real and predicted values.

        Args:
            real (ArrayLike): The real values.
                The actual or ground truth values.
            pred (ArrayLike): The predicted values.
                The predicted values.

        Returns:
            Union[float, ArrayLike]: The SMAPE value(s).
                The calculated SMAPE value(s) between the real and predicted values.

        Notes:
            - The result is NOT multiplied by 100.
            - Rows with 0 values in the target are excluded as division by 0 is impossible and
              a small EPSILON will yield a huge percentage error when the relative error will be small.
        """
        ind = (real != 0)
        real = np.array(real[ind])
        pred = pred[ind]
        return np.mean(2.0 * np.abs(real - pred) / ((np.abs(real) + np.abs(pred)) + EPSILON))
    
    @staticmethod
    def rmspe(cls, real: ArrayLike, pred: ArrayLike) -> Union[float, ArrayLike]:
        """
        Calculates the root mean squared percentage error between the real and predicted values.

        Args:
            real (ArrayLike): The real values.
            pred (ArrayLike): The predicted values.

        Returns:
            Union[float, ArrayLike]: The root mean squared percentage error.

        Notes:
            - Result is NOT multiplied by 100.
            - Rows with 0 values in target are excluded as division by 0 is impossible and
              a small EPSILON will yield a huge percentage error when relative error will be small.
        """
        ind = (real != 0)
        real = np.array(real[ind])
        pred = pred[ind]
        return np.sqrt(np.mean(np.square(cls._percentage_error(real, pred))))
    
    @staticmethod
    def r2(real: ArrayLike, pred: ArrayLike) -> Union[float, ArrayLike]:
        """
        Calculate the R-squared (coefficient of determination) metric.

        Args:
            real (ArrayLike): The real values.
            pred (ArrayLike): The predicted values.

        Returns:
            Union[float, ArrayLike]: The R-squared value(s).
        """
        return r2(real, pred)
    
    # =============================================================================
    
    @staticmethod
    def _remove_negatives(pred: ArrayLike, real: ArrayLike) -> tuple:
        '''Remove identical indexes from pred / real if either of these arrays contain negative values
        
        Args:
            pred (ArrayLike): Array of predicted values
            real (ArrayLike): Array of real values
            
        Returns:
            tuple: A tuple containing the modified pred and real arrays with negative values removed
        '''
        pred = np.array(pred).astype(float)
        real = np.array(real).astype(float)
        neg_in_pred_idx = np.array(np.where(pred<0)).flatten()
        neg_in_true_idx = np.array(np.where(real<0)).flatten()
        
        neg_in_pred_and_true = list(set(np.concatenate((neg_in_pred_idx, neg_in_true_idx))))
        pred_non_negative = np.delete(pred, neg_in_pred_and_true) 
        real_non_negative = np.delete(real, neg_in_pred_and_true) 
        return pred_non_negative, real_non_negative
    
    @staticmethod
    def _error(real: ArrayLike, pred: ArrayLike) -> Union[float, ArrayLike]:
        """Calculates the simple error between the real and predicted values.

        Args:
            real (ArrayLike): The real values.
            pred (ArrayLike): The predicted values.

        Returns:
            Union[float, ArrayLike]: The difference between the real and predicted values.
        """
        real = np.array(real)
        return real - pred
    
    @staticmethod
    def _percentage_error(cls, real: ArrayLike, pred: ArrayLike) -> Union[float, ArrayLike]:
        """
        Calculates the percentage error between the real and predicted values.

        Args:
            real (ArrayLike): The real values.
            pred (ArrayLike): The predicted values.

        Returns:
            Union[float, ArrayLike]: The percentage error between the real and predicted values.

        Notes:
            - The result is NOT multiplied by 100.
            - Rows with 0 values in the target are excluded, as division by 0 is impossible.
              A small EPSILON will yield a huge percentage error when the relative error is small.
        """
        ind = real != 0
        real = np.array(real[ind])
        pred = pred[ind]
        return cls._error(real, pred) / (real + EPSILON)

    
class ClassificationMetrics:
    @staticmethod
    def auc(real: ArrayLike, pred: ArrayLike) -> Union[float, ArrayLike]:
        """
        Computes the Area Under the Curve (AUC) for binary classification.

        Args:
            real (ArrayLike): The true labels of the binary classification.
            pred (ArrayLike): The predicted probabilities or scores for the positive class.

        Returns:
            Union[float, ArrayLike]: The AUC value or an array of AUC values if `real` and `pred` are arrays.
        """
        return auc(real, pred)
    
    @staticmethod
    def gini(real: ArrayLike, pred: ArrayLike) -> Union[float, ArrayLike]:
        """
        Calculate the Gini coefficient.

        Args:
            real (ArrayLike): The real values.
            pred (ArrayLike): The predicted values.

        Returns:
            Union[float, ArrayLike]: The Gini coefficient.

        """
        roc_auc = auc(real, pred)
        return 2*roc_auc - 1
    
    @staticmethod
    def log_loss(real: ArrayLike, pred: ArrayLike) -> Union[float, ArrayLike]:
        """
        Calculates the logarithmic loss between the true labels and predicted probabilities.

        Args:
            real (ArrayLike): The true labels.
            pred (ArrayLike): The predicted probabilities.

        Returns:
            Union[float, ArrayLike]: The logarithmic loss.

        """
        return log_loss(real, pred)
    
    @staticmethod
    def accuracy(real: ArrayLike, pred: ArrayLike) -> Union[float, ArrayLike]:
        """
        Calculates the accuracy of predicted values compared to the real values.

        Args:
            real (ArrayLike): The real values.
            pred (ArrayLike): The predicted values.

        Returns:
            Union[float, ArrayLike]: The accuracy score(s).

        """
        return accuracy(real, pred)
    
    @staticmethod
    def balanced_accuracy(real: ArrayLike, pred: ArrayLike) -> Union[float, ArrayLike]:
        """
        Calculate the balanced accuracy score.

        Args:
            real (ArrayLike): The true labels.
            pred (ArrayLike): The predicted labels.

        Returns:
            Union[float, ArrayLike]: The balanced accuracy score.

        """
        return balanced_accuracy(real, pred)
    
    @staticmethod
    def precision_weighted(real: ArrayLike, pred: ArrayLike) -> Union[float, ArrayLike]:
        """
        Calculates the weighted precision score.

        Args:
            real (ArrayLike): The true labels.
            pred (ArrayLike): The predicted labels.

        Returns:
            Union[float, ArrayLike]: The weighted precision score.

        """
        score = precision(real, pred, average='weighted')
        return score
    
    @staticmethod
    def precision_macro(real: ArrayLike, pred: ArrayLike) -> Union[float, ArrayLike]:
        """
        Calculate the macro-averaged precision score.

        Args:
            real (ArrayLike): The true labels.
            pred (ArrayLike): The predicted labels.

        Returns:
            Union[float, ArrayLike]: The macro-averaged precision score.

        """
        score = precision(real, pred, average='macro')
        return score
    
    @staticmethod
    def recall(real: ArrayLike, pred: ArrayLike) -> Union[float, ArrayLike]:
        """
        Calculates the recall score.

        Args:
            real (ArrayLike): The true labels.
            pred (ArrayLike): The predicted labels.

        Returns:
            Union[float, ArrayLike]: The recall score(s).
        """
        return recall(real, pred)
    
    @staticmethod
    def recall_weighted(real: ArrayLike, pred: ArrayLike) -> Union[float, ArrayLike]:
        """
        Calculates the weighted recall score.

        Args:
            real (ArrayLike): The true labels.
            pred (ArrayLike): The predicted labels.

        Returns:
            Union[float, ArrayLike]: The weighted recall score.

        """
        score = recall(real, pred, average='weighted')
        return score

    @staticmethod
    def recall_macro(real: ArrayLike, pred: ArrayLike) -> Union[float, ArrayLike]:
        """
        Calculates the macro-averaged recall score.

        Args:
            real (ArrayLike): The true labels.
            pred (ArrayLike): The predicted labels.

        Returns:
            Union[float, ArrayLike]: The macro-averaged recall score.

        """
        score = recall(real, pred, average='macro')
        return score
    
    @staticmethod
    def f1(real: ArrayLike, pred: ArrayLike) -> Union[float, ArrayLike]:
        """
        Calculates the F1 score.

        Args:
            real (ArrayLike): The true labels.
            pred (ArrayLike): The predicted labels.

        Returns:
            Union[float, ArrayLike]: The F1 score.

        """
        return f1(real, pred)
    
    @staticmethod
    def f1_weighted(real: ArrayLike, pred: ArrayLike) -> Union[float, ArrayLike]:
        """
        Calculates the weighted F1 score.

        Args:
            real (ArrayLike): The true labels.
            pred (ArrayLike): The predicted labels.

        Returns:
            Union[float, ArrayLike]: The weighted F1 score.

        """
        score = f1(real, pred, average='weighted')
        return score

    @staticmethod
    def f1_macro(real: ArrayLike, pred: ArrayLike) -> Union[float, ArrayLike]:
        """
        Calculates the F1 score using the macro averaging method.

        Args:
            real (ArrayLike): The true labels.
            pred (ArrayLike): The predicted labels.

        Returns:
            Union[float, ArrayLike]: The F1 score.

        """
        score = f1(real, pred, average='macro')
        return score
        
    

