# Original code from DanilZherebtsov, licensed under the MIT License.
# Modifications (2024-03-23) made by Daniel Porsmose.

from rapidgbm.metrics import supported_metrics
from typing import Any


class ArgValidationMixin:
    @staticmethod
    def _is_bool(val: Any) -> bool:
        """
        Check if a value is of boolean type.

        Args:
            val (Any): The value to be checked.

        Returns:
            bool: True if the value is of boolean type, False otherwise.
        """
        return type(val) == bool

    @staticmethod
    def _is_int(val: Any) -> bool:
        """
        Check if a value is of type int.

        Args:
            val (Any): The value to be checked.

        Returns:
            bool: True if the value is of type int, False otherwise.
        """
        return type(val) == int
    # -------------------------------------------------------------------------
    # metric
    @property
    def metric(self) -> str:
        return self._metric

    @metric.setter
    def metric(self, value: Any) -> None:
        if type(value) != str : raise TypeError('metric must be a string')
        if value not in supported_metrics: raise KeyError(f'LGBMTuner supports the following evaluation metrics: {supported_metrics}')
        self._metric = value
    # -------------------------------------------------------------------------
    # trials
    @property
    def trials(self) -> int:
        return self._trials

    @trials.setter
    def trials(self, value: Any) -> None:
        if not self._is_int(value) : raise TypeError('trials must be an integer')
        if value <= 0: raise ValueError('trials must be an integer > 0')
        self._trials = value
    # -------------------------------------------------------------------------
    # refit
    @property
    def refit(self) -> bool:
        return self._refit

    @refit.setter
    def refit(self, value: Any) -> None:
        if not self._is_bool(value) : raise TypeError('acceptable refit options are True/False')
        self._refit = value
    # -------------------------------------------------------------------------
    # verbosity
    @property
    def verbosity(self) -> int:
        return self._verbosity

    @verbosity.setter
    def verbosity(self, value: Any) -> None:
        if not self._is_int(value) : raise TypeError('verbosity must be an integer')
        if value not in range(0,6) : raise ValueError('acceptable verbosity options are [0,1,2,3,4,5]')
        self._verbosity = value
    # -------------------------------------------------------------------------
    # visualization
    @property
    def visualization(self) -> bool:
        return self._visualization

    @visualization.setter
    def visualization(self, value: Any) -> None:
        if not self._is_bool(value) : raise TypeError('acceptable visualization options are True/False')
        self._visualization = value
    # -------------------------------------------------------------------------
    # device_type
    @property
    def device_type(self) -> str:
        return self._device_type

    @device_type.setter
    def device_type(self, value: Any) -> None:
        if not value in ['cpu', 'gpu', 'cuda', 'cuda_exp'] : raise TypeError('acceptable device_type options are cpu/gpu/cuda/cuda_exp')
        self._device_type = value
    # -------------------------------------------------------------------------
    # n_jobs
    @property
    def n_jobs(self) -> int:
        return self._n_jobs

    @n_jobs.setter
    def n_jobs(self, value: Any) -> None:
        error_msg = 'n_jobs must be an integer; -1 for all available threads/cores or > 0 for a specific number of threads/cores'
        if not self._is_int(value) : raise TypeError(error_msg)
        if value < -1 : raise ValueError(error_msg)
        if value == 0 : raise ValueError(error_msg)
        self._n_jobs = value
    # -------------------------------------------------------------------------
    # seed
    @property
    def seed(self) -> int:
        return self._seed

    @seed.setter
    def seed(self, value: Any) -> None:
        if not self._is_int(value) : raise TypeError('seed must be an integer')
        self._seed = value
    # -------------------------------------------------------------------------
    # eval_results_callback
    @property
    def eval_results_callback(self) -> Any:
        return self._eval_results_callback

    @eval_results_callback.setter
    def eval_results_callback(self, value: Any) -> None:
        if not value is None:
            if not hasattr(value, '__call__') : raise TypeError('eval_results_callback must be a function')
        self._eval_results_callback = value