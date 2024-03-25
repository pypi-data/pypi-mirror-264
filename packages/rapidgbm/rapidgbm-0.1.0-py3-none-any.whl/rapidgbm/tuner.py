import numpy as np
import pandas as pd
import os
import lightgbm as lgb
import optuna
from sklearn.model_selection import train_test_split
from copy import copy
from functools import partial
from typing import final, Callable, Any, Union, Iterable
import matplotlib.pyplot as plt

import warnings
warnings.filterwarnings("ignore")
import matplotlib.pyplot as plt
from rapidgbm.utility import timer, Printer, Validators
from rapidgbm.utility import Distribution, OPTUNA_DISTRIBUTIONS_MAP, SearchSpace
from rapidgbm.utility import ArgValidationMixin, PlottingMixin
from rapidgbm.metrics import MetricHelpers, regression_metrics, classification_metrics


supported_gridsearch_params: list = [
    'boosting_type', 'num_iterations', 'learning_rate', 'num_leaves', 'max_depth', 
    'min_data_in_leaf', 'min_sum_hessian_in_leaf', 'bagging_fraction', 'feature_fraction',
    'max_delta_step', 'lambda_l1', 'lambda_l2', 'linear_lambda', 'min_gain_to_split',
    'drop_rate', 'top_rate', 'min_data_per_group', 'max_cat_threshold'
    ]

class RapidGBMTuner(ArgValidationMixin, PlottingMixin):

    __version__ = '0.0.1'

    def __init__(self,*,
                 metric: str = "None",
                 trials: int = 200,
                 device_type: str = 'cpu',
                 refit: bool = True,
                 seed: int = 42,
                 n_jobs: int = -1,
                 verbosity: int = 1,
                 visualization: bool = True,
                 custom_lgbm_params: dict = {},
                 eval_results_callback: Union[Callable, None] = None,
                 ) -> None:
        """
        Class to automatically tune LGBM model with optuna.
        
        Model type (regressor/classifier) is inferred based on target variable & metric.
        Init parameters and search space are inferred by built in logic.

        Args:
            metric (str, optional): evaluation metric. The default is "None".
            trials (int, optional): number of hyperparameter search trials. The default is 200.
            refit (bool, optional): Flag to refit the model with optimized parameters on whole dataset.
            verbosity (int, optional): console verbosity level: 0 - no output except for optuna CRITICAL errors and builtin exceptions;
                (1-5) based on optuna.logging options. The default is 1. 
            visualization (bool, optional): flag to print optimization & feature importance plots. The default is True.
            seed (int): random_state. The default is 42.
            n_jobs (int): number of parallel jobs to run. The default is -1 which is all cores available minus 2 for safeguard.
            device_type (str): cpu/gpu/cuda/cuda_exp. The default is 'cpu'.
            custom_lgbm_params (dict): custom lgbm parameters to be passed to the model, please refer to LGBM documentation for available parameters.
            eval_results_callback (func): callback function to be applied on the eval_results dictionary that is being populated
                with evaluation metric score upon completion of each training trial.
        Returns:
            None

        """
        
        self.metric: str = metric
        self.trials: int = trials
        self.verbosity: int = verbosity
        self.device_type: str = device_type
        self.refit: bool = refit
        self.n_jobs: int = n_jobs
        self.visualization: bool = visualization
        self.seed: int = seed
        self.custom_lgbm_params: dict = custom_lgbm_params
        self.eval_results_callback: Union[Callable, None] = eval_results_callback

        self.target_minimum: float
        self._fitted_model: lgb.Booster
        self._feature_importances: pd.Series
        self._study: optuna.Study # save optuna study for plotting
        self.target_classes: list
        self._init_params: dict
        self._best_params: dict
        self.eval_results: dict = {} # evaluation metric results per each trial storage

        # __post__init__()
        self.printer: Printer = Printer(verbose=True if self.verbosity > 0 else False)
        self.search_space: dict = self._get_default_search_space()
        self.grid: dict = self._get_all_available_and_defined_grids()
        self.early_stopping_results: dict = {} # stores early_stopping results per each trial
        self._set_optuna_verbosity(self.verbosity)
    # -------------------------------------------------------------------------
    # -------------------------------------------------------------------------
     # init_params
    @property
    def init_params(self) -> dict:
        """ Initial LGBM parameters inferred based on data statistics and built-in logic.

        Returns:
            dict: Initial LGBM parameters
        """
        return self._init_params
    # -------------------------------------------------------------------------    
    # best_params
    @property
    def best_params(self) -> dict:
        """ Best LGBM parameters found during the optimization process.
        
        Returns:
            dict: Best LGBM parameters
        """
        return self._best_params
    # -------------------------------------------------------------------------    
    # feature_importances
    @property
    def feature_importances(self) -> pd.Series:
        """ Feature importances of the fitted model.

        Returns:
            pd.Series: Feature importances
        """
        if not self._fitted_model:
            raise AttributeError('LGBMTuner.fit(refit = True) must be applied before feature_importances can be displayed')
        return self._feature_importances
    # -------------------------------------------------------------------------    
    # fitted_model
    @property
    def fitted_model(self) -> lgb.Booster:
        """ Fitted LGBM model object.

        Returns:
            lgb.Booster: Fitted LGBM model
        """
        return self._fitted_model
    # -------------------------------------------------------------------------    
    # study
    @property
    def study(self) -> optuna.Study:
        """ Optuna study object.

        Returns:
            optuna.Study: Optuna study
        """
        return self._study
    # -------------------------------------------------------------------------
    # -------------------------------------------------------------------------
    @final
    def update_grid(self, lgb_key: str, params: Union[list, tuple, dict]) -> None:
        """
        Change the grid for a specific LightGBM parameter.

        Args:
            lgb_key (str): The key of the LightGBM parameter.
            params (Union[list, tuple, dict]): The new grid for the parameter. It can be passed as a list, tuple, or dict.

        Raises:
            ValueError: If params is not a list, tuple, or dict.

        Returns:
            None

        Notes:
            - list (will be used for a random search)
            - tuple (will be used to define the uniform grid range between the min(tuple), max(tuple))
            - dict with keywords 'choice'/'low'/'high'

        Example:
            ``` Python
            tuner = Tuner()
            tuner.update_grid('boosting_type', ['gbdt', 'rf'])  # random search
            tuner.update_grid('learning_rate', (0.001, 0.1))  # uniform grid range between the min(tuple), max(tuple))
            tuner.update_grid('num_leaves', {'low': 0.1, 'high': 5})  # uniform grid range between the low and high values
            tuner.update_grid('max_data_in_leaf', {'choice' : [40, 50, 70]})  # random search
            ```
        """
        if not isinstance(params, (list, tuple, dict)):
            raise ValueError('params must be a list, tuple or dict')
        
        self.grid[lgb_key] = params
    # -------------------------------------------------------------------------
    @final
    def fit_optimized(self, X: np.ndarray, y: np.ndarray) -> None:
        """
        Train model with tuned params on whole train data

        Args:
            X (np.ndarray): Train features.
            y (np.ndarray): Train target.

        Returns:
            None
        
        Example:
            ``` Python
            from rapidgbm import RapidGBMTuner
            tuner = RapidGBMTuner(metric='log_loss', trials=100, refit=False, verbosity=1)
            tuner.fit(X_train, y_train)
            tuner.fit_optimized(np.array(X_train), np.array(y_train))
            ```
        """
        if not self._best_params:
            raise ModuleNotFoundError(f'LGBMTuner.fit() must be applied before fit_optimized execution to populate best_params property.')

        Validators.validate_numpy_ndarray_arguments(X)
        Validators.validate_numpy_ndarray_arguments(y)
        
        self.printer.print('Fitting optimized model with the following params:', order=2)
        for key, value in self._best_params.items():
            print(f'{key:<33}: {value}')
        self._fitted_model = lgb.train(self._best_params, lgb.Dataset(X,y))
    # -----------------------------------------------------------------------------
    @final
    @timer
    def fit(self, X: pd.DataFrame, y: pd.Series, optuna_study_params: Union[None, dict] = None) -> None:
        """
        Fits the LightGBM model by finding optimized parameters based on the training data and metric.

        Args:
            X (pd.DataFrame): The training features.
            y (pd.Series): The training labels.
            optuna_study_params (dict, optional): Parameters for the Optuna study. Defaults to None.

        Returns:
            None

        Raises:
            ValueError: If the features or target arguments are invalid.

        Example:
            ``` Python
            from rapidgbm import RapidGBMTuner
            tuner = RapidGBMTuner(metric='log_loss', trials=100, refit=True, verbosity=1)
            tuner.fit(X_train, y_train)
            ```

        Notes:
            - The optimization metric is determined based on the metric specified during initialization.
            - For regression, the optimization metric is selected based on the `eval_metric` parameter, except for 'r2'.
                If `eval_metric` is 'r2', then the optimization metric is 'mean_squared_error'.
            - For classification, the optimization metric is always 'log_loss'.
            - The LGB Classifier/Regressor is inferred based on the metric and target variable statistics.
            - Initial LGBM parameters are inferred based on data statistics and built-in logic, and can be accessed
                using `self._init_params`.
            - The parameter grid for hyperparameter search is inferred based on data statistics and built-in logic.
            - The `optuna_study_params` parameter allows for customization of the Optuna study. Refer to the
                documentation for `optuna.study.create_study` for more details.

        """
        Validators.validate_features_argument(X)
        Validators.validate_target_argument(y)

        optimization_metric_func: Callable = MetricHelpers.get_optimization_metric_func(self.metric)
        
        self.printer.print('Initiating LGBMTuner.fit', order=1)
        self.printer.print('Settings:', order=3)
        self.printer.print(f'Trying {self.trials} trials', order=4)
        self.printer.print(f'Evaluation metric: {self.metric} ', order=4)
        self.printer.print(f'Study direction: minimize {optimization_metric_func.__name__}', order=4)
        print()
            
        self.target_classes = y.unique().tolist()
        self._get_target_minimum(y)
        self._init_params_on_input(len(X), y)
        # update the predefined params with custom params passed by user
        self._init_params.update(self.custom_lgbm_params)
        self._align_grid_and_search_space()
        
        sampler: optuna.samplers.TPESampler = optuna.samplers.TPESampler(seed=self.seed)
        
        optuna_params: dict = {'pruner':optuna.pruners.MedianPruner(n_warmup_steps=5),
                            'sampler':sampler,
                            'direction':'minimize'}
        # incorporate user defined params if passed
        if optuna_study_params is not None:
            optuna_params.update(optuna_study_params)

        study: optuna.Study = optuna.create_study(**optuna_params)#get_study_direction(metric))

        optimization_function: Callable = partial(self._objective, X = X.values, y = y.values)

        study.optimize(optimization_function, n_trials = self.trials)

        # populate the learned params into the suggested params
        temp_params: dict = self._populate_best_params_to_init_params(study.best_params)
        # extract early stopping results from best trial
        
        if not 'is_unbalance' in self._init_params or not 'scale_pos_weight' in self._init_params:
            best_trial_number = study.best_trial.number
            num_iterations_in_best_trial = self.early_stopping_results[best_trial_number]
            temp_params['num_iterations'] = num_iterations_in_best_trial
        # tune num_iterations    
        # iteration, best_score = self.optimize_num_iterations(X.values, y.values, temp_params)
        # temp_params['num_iterations'] = iteration
        self._best_params = temp_params

        if self.refit:
            self.fit_optimized(X.values, y.values)
            self._save_feature_importances(X.columns)

        self._study = study

        if self.visualization:
            self._check_refit_status('plot_optimization_history()')
            self.plot_optimization_history(study=self._study)
            self._check_refit_status('plot_param_importance()')
            self.plot_param_importances(study=self._study)
            self._check_refit_status('plot_intermediate_values()')
            self.plot_intermediate_values(study=self._study)
            if self.refit:
                self._check_refit_status('plot_importances()')
                self.plot_importances(feature_importances=self._feature_importances, dark=False, save=False)
        # clean up
        self.eval_results_callback = None
        # --------------------------------
        break_symbol = '|'
        print()
        self.printer.print(f"Optuna hyperparameters optimization finished", order=3)
        self.printer.print(f"Best trial number:{study.best_trial.number:>2}{break_symbol:>5}     {optimization_metric_func.__name__}:{study.best_trial.value:>29}", order=4, breakline='-')
    # -------------------------------------------------------------------------
    @final
    def predict(self, test: pd.DataFrame, threshold: float = 0.5) -> np.ndarray:
        """
        Predicts the target variable for the given test set using the fitted model.

        Args:
            test (pd.DataFrame): The test features.
            threshold (float, optional): The binary classification probability threshold. Defaults to 0.5.

        Returns:
            np.ndarray: The predicted values.

        Raises:
            ValueError: If the model has not been fitted yet.
            TypeError: If the test features are not a pandas DataFrame.
            ValueError: If the threshold is not a float.

        Example:
            ``` Python
            from rapidgbm import RapidGBMTuner
            tuner = RapidGBMTuner(metric='log_loss', trials=100, refit=True, verbosity=1)
            tuner.fit(X_train, y_train)
            predictions = tuner.predict(X_test, threshold=0.5)
            ```
        """
        self._check_refit_status('predict()')
        Validators.validate_features_argument(test)
        Validators.validate_threshold_argument(threshold)

        pred = self._fitted_model.predict(test.values, num_threads=self._init_params['num_threads'])
        pred = np.array(pred).astype('float')

        # regression predict
        if self.metric in regression_metrics:
            if self.target_minimum >= 0:
                pred = np.where(pred < 0, self.target_minimum, pred)
            return pred
        else:
            # binary classification predict
            if self._fitted_model.params['objective'] == 'binary':
                pred = (pred > threshold).astype('int')
            # multiclass classification predict
            # TODO: SAVE CLASSES NAMES TO APPLY THEM BACK
            else:
                pred = np.argmax(pred, axis=1)
            return pred
    # -------------------------------------------------------------------------
    @final
    def predict_proba(self, test: pd.DataFrame) -> np.ndarray:
        """
        Predict probabilities for classification problems.

        Args:
            test (pd.DataFrame): The test features.

        Raises:
            TypeError: If self._fitted_model.params['objective'] == 'regression',
                indicating that predict_proba() is only applicable for classification objectives.

        Returns:
            np.ndarray: The predicted probabilities.

        Example:
            ``` Python
            from rapidgbm import RapidGBMTuner
            tuner = RapidGBMTuner(metric='log_loss', trials=100, refit=True, verbosity=1)
            tuner.fit(X_train, y_train)
            predictions = tuner.predict_proba(X_test)
            ```

        """
        self._check_refit_status('predict_proba()')
        Validators.validate_features_argument(test)

        if self.metric in regression_metrics:
            raise TypeError('predict_proba() is applicable for classification problems only')
        pred = self._fitted_model.predict(test.values, num_threads=self._init_params['num_threads'])
        pred = np.array(pred).astype('float')
        return pred
    # -------------------------------------------------------------------------
    # -------------------------------------------------------------------------
    # get user defined grid
    def _get_all_available_and_defined_grids(self) -> dict:
        """
        Returns a dictionary containing all available and defined grid search parameters and their corresponding values.

        Returns:
            dict: A dictionary with grid search parameters as keys and their corresponding values as values.
                  If a parameter is not defined in the search space, its value will be None.
        """
        all_grids: dict = {}
        for param in supported_gridsearch_params:
            if param in self.search_space:
                all_grids[param] = self.search_space[param].params
            else:
                all_grids[param] = None
        return all_grids
        
    # -------------------------------------------------------------------------
    # print init parameters when calling the class instance
    def __repr__(self) -> str:
        return f'RapidGBMTuner(Evaluation metric: {self._metric}\
            \n          trials: {self.trials}\
            \n          refit: {self.refit}\
            \n          verbosity: {self.verbosity}\
            \n          visualization: {self.visualization})\
            \n          device_type: {self.device_type})\
            \n          grid: {self.grid})'
    
    # -------------------------------------------------------------------------    
    def _init_params_on_input(self, rows_num: int, y: pd.Series) -> None:
        """
        Get model parameters depending on dataset parameters.

        Args:
            rows_num (int): Number of rows in the training data.
            y (pd.Series): Train labels.

        Returns:
            None
        """
        # TODO: use number of features
        
        # default lgbm parameters - basis for minor changes based on dataset length
        default_params_classification: dict = {
            "task": "train",
            "learning_rate": 0.05,
            "num_leaves": 128,
            "feature_fraction": 0.7,
            "bagging_fraction": 0.7,
            "bagging_freq": 1,
            "max_depth": -1,
            "verbosity": -1,
            "lambda_l1": 1,
            "lambda_l2": 0.0,
            "min_split_gain": 0.0,
            "zero_as_missing": False,
            "max_bin": 255,
            "min_data_in_bin": 3,
            "num_iterations": 10000,
            "early_stopping_rounds": 100,
            "random_state": 42,
            "device_type": self.device_type
        }

        default_params_regression: dict = {
            "learning_rate": 0.05,
            "num_leaves": 32,
            "feature_fraction": 0.9,
            "bagging_fraction": 0.9,
            "verbosity": -1,
            "num_iterations": 10000,
            "early_stopping_rounds": 100,
            "random_state": 42,
            "device_type": self.device_type
        }

        task: str = MetricHelpers.define_objective(self.metric, y)
        
        if task == 'regression':
            self._init_params = copy(default_params_regression)
        else:
            self._init_params = copy(default_params_classification)

        # define additional params based on task type
        if task == 'binary':
            self._init_params['num_classes'] = 1 
        elif task == 'multiclass':
            self._init_params['num_classes'] = y.nunique()
        # -------------------------------------------------------------------------
        # populate objective and metric based
        self._init_params['objective'] = MetricHelpers.define_objective(self.metric, self.target_classes)
        self._init_params['metric'] = MetricHelpers.get_pruning_metric(self.metric, self.target_classes)
        # -------------------------------------------------------------------------
        # do not use all available threads and make sure cpu_count is not negative
        if self.n_jobs == -1:
            os_cpu_count = os.cpu_count()
            os_cpu_count = int(os_cpu_count) if os_cpu_count else 1 
            cpu_count = int(np.where(os_cpu_count-2 < 0, 1, os_cpu_count-2))
            self._init_params['num_threads'] = cpu_count
        else:
            self._init_params['num_threads'] = self.n_jobs

        self._init_params['num_threads'] = cpu_count

        if rows_num <= 10000:
            init_lr = 0.01
            ntrees = 3000
            es = 200
        elif rows_num <= 20000:
            init_lr = 0.02
            ntrees = 3000
            es = 200
        elif rows_num <= 100000:
            init_lr = 0.03
            ntrees = 1200
            es = 200
        elif rows_num <= 300000:
            init_lr = 0.04
            ntrees = 2000
            es = 100
        else:
            init_lr = 0.05
            ntrees = 2000
            es = 100

        if rows_num > 300000:
            self._init_params["num_leaves"] = 128 if task == "regression" else 244
        elif rows_num > 100000:
            self._init_params["num_leaves"] = 64 if task == "regression" else 128
        elif rows_num > 50000:
            self._init_params["num_leaves"] = 32 if task == "regression" else 64
            # params['lambda_l1'] = 1 if task == 'reg' else 0.5
        elif rows_num > 20000:
            self._init_params["num_leaves"] = 32 if task == "regression" else 32
            self._init_params["lambda_l1"] = 0.5 if task == "regression" else 0.0
        elif rows_num > 10000:
            self._init_params["num_leaves"] = 32 if task == "regression" else 64
            self._init_params["lambda_l1"] = 0.5 if task == "regression" else 0.2
        elif rows_num > 5000:
            self._init_params["num_leaves"] = 24 if task == "regression" else 32
            self._init_params["lambda_l1"] = 0.5 if task == "regression" else 0.5
        else:
            self._init_params["num_leaves"] = 16 if task == "regression" else 16
            self._init_params["lambda_l1"] = 1 if task == "regression" else 1

        self._init_params["learning_rate"] = init_lr
        self._init_params["num_iterations"] = ntrees

        # disable early stopping if 'scale_pos_weight' or 'is_unbalance' is used, because 
        # in such case with severe disbalance it always stops at first iteration and underfits
        if 'scale_pos_weight' in self._init_params or 'is_unbalance' in self._init_params:
            del self._init_params["early_stopping_rounds"]
        else:
            self._init_params["early_stopping_rounds"] = es
    # -----------------------------------------------------------------------------
    def _get_default_search_space(self) -> dict:
        """Returns the default search space for hyperparameter optimization.

        This method generates a default search space grid and type of distribution for each parameter
        used in hyperparameter optimization.

        Returns
        -------
        dict
            The optimization search space grid and type of distribution for each parameter.

        """
        # TODO: create additional options based on bigger estimated_n_trials
        search_space: dict = {}

        search_space["feature_fraction"] = SearchSpace(Distribution.UNIFORM, low=0.5, high=1.0) 
        search_space["num_leaves"] = SearchSpace(Distribution.INTUNIFORM, low=16, high=255)

        if self.trials > 30:
            search_space["bagging_fraction"] = SearchSpace(Distribution.UNIFORM, low=0.5, high=1.0) 
            search_space["min_sum_hessian_in_leaf"] = SearchSpace(Distribution.LOGUNIFORM, low=1e-3, high=10.0)

        if self.trials > 100:
            search_space["lambda_l1"] = SearchSpace(Distribution.LOGUNIFORM, low=1e-8, high=10.0)
            search_space["lambda_l2"] = SearchSpace(Distribution.LOGUNIFORM, low=1e-8, high=10.0)

        return search_space
    # -----------------------------------------------------------------------------
    def _sample_from_search_space(self, trial: optuna.Trial) -> dict:
        """
        Get params for a trial.

        Args:
            trial (optuna.Trial): The trial object.

        Raises:
            ValueError: If Optuna distribution error occurs.

        Returns:
            dict: The trial parameters consisting of suggested_params modified by grid.
        """
        trial_values = copy(self._init_params)
        for parameter, SearchSpace in self.search_space.items():
            if SearchSpace.distribution_type in OPTUNA_DISTRIBUTIONS_MAP:
                trial_values[parameter] = getattr(trial, OPTUNA_DISTRIBUTIONS_MAP[SearchSpace.distribution_type])(
                    name=parameter, **SearchSpace.params)
            else:
                for key, value in self.search_space.items():
                    print(key)
                    print(value.distribution_type)
                raise ValueError(f"Optuna does not support distribution {SearchSpace.distribution_type}")
        return trial_values
    # -----------------------------------------------------------------------------
    def _get_dtrain_dvalid_objects(self, 
                                   X: pd.DataFrame, 
                                   y: pd.Series, 
                                   metric: str, 
                                   seed: Union[None, int] = None, 
                                   return_raw_valid: bool = False) -> tuple:
        """
        Create lgbm.Datasets for training and validation.
        
        By default splits without defined random_state in order to replicate CV (sort of).
        Seed is used for optimize_num_iterations.

        Args:
            X (pd.DataFrame): Train features.
            y (pd.Series): Train labels.
            metric (str): Evaluation metric name.
            seed (int/None): Random state for split.
            return_raw_valid (bool): Flag to return valid_x, valid_y in addition to dvalid (for get_validation_score())

        Returns:
            tuple: A tuple containing:
                - dtrain (lgbm.Dataset): Train data.
                - dvalid (lgbm.Dataset): Valid data.
                - (optional) valid_x (pd.DataFrame): Validation features (only returned if `return_raw_valid` is True).
                - (optional) valid_y (pd.Series): Validation labels (only returned if `return_raw_valid` is True).
        """
        if metric in classification_metrics:
            train_x, valid_x, train_y, valid_y = train_test_split(X, y, test_size=0.25, stratify=y)
        else:
            train_x, valid_x, train_y, valid_y = train_test_split(X, y, random_state=seed, test_size=0.25)
        dtrain = lgb.Dataset(train_x, label=train_y)
        dvalid = lgb.Dataset(valid_x, label=valid_y)
        if return_raw_valid:
            return dtrain, dvalid, valid_x, valid_y
        else:
            return dtrain, dvalid
    # ------------------------------------------------------------------------------------------
    def _get_target_minimum(self, y: pd.Series) -> None:
        '''Record target minimum value for replacing negative predictions in regression.

        Args:
            y (pd.Series): The target variable.

        Returns:
            None
        '''
        if self.metric in regression_metrics:    
            self.target_minimum = min(y)
    # ------------------------------------------------------------------------------------------
    def _get_validation_score(self, 
                              trial: optuna.Trial, 
                              dtrain: lgb.Dataset, 
                              dvalid: lgb.Dataset, 
                              valid_x: pd.DataFrame, 
                              valid_y: pd.DataFrame, 
                              optimization_metric_func: Callable, 
                              params: dict, 
                              pruning_callback: Callable) -> float:
        '''
        Train model with trial params and validate on valid set against the defined metric.
        Print optimization result every iteration.
        If evaluation metric != optimization metric, print evaluation metric.

        Args:
            trial (optuna.Trial): Parameters tuning iteration.
            dtrain (lgb.Dataset): Train data.
            dvalid (lgb.Dataset): Valid data.
            valid_x (pd.DataFrame): Valid features.
            valid_y (pd.Series): Valid target.
            optimization_metric_func (Callable): Scorer function.
            params (dict): Model parameters.
            pruning_callback (Callable): Callback function.

        Returns:
            float: Validation result.
        '''

        gbm = lgb.train(params, dtrain, valid_sets=[dvalid], callbacks=[pruning_callback])
        pred = gbm.predict(valid_x)

        result = optimization_metric_func(valid_y, pred)

        optimization_direction: str = 'lower-better'

        self.printer.print(f'Trial number: {trial.number} finished', order=3)
        self.printer.print(f'Optimization score ({optimization_direction:<4}): {optimization_metric_func.__name__}: {result}', order=4)
        # save early stopping results per each trial for further use in best_params
        self.early_stopping_results[trial.number] = gbm.best_iteration
        # save evaluation metric results per each trial
        self.eval_results[f'train_trial_{trial.number}'] = result
        # calculate & print eval_metric only if eval_metric != optimization_metric
        if self.metric != optimization_metric_func.__name__:
            eval_score = MetricHelpers.get_eval_score(valid_y, pred, self.metric, params['objective'])
            self.printer.print(f'Evaluation score ({MetricHelpers.print_lower_greater_better(self.metric):<4}): {self.metric}: {eval_score}', order=4)
            # save evaluation metric results per each trial
            self.eval_results[f'train_trial_{trial.number}'] = eval_score
        self.printer.print(breakline='.')

        if self.eval_results_callback:
            self.eval_results_callback(self.eval_results)

        return result
    # ------------------------------------------------------------------------------------------
    def _objective(self, trial: optuna.Trial, X: pd.DataFrame, y: pd.Series) -> float:
        """
        Define objective for optuna trial training.

        This method defines the objective function for the Optuna trial training. It performs the following steps:
        - Creates an optimization metric based on the evaluation metric passed by the user.
        - Creates train/valid splits.
        - Defines suggested initial parameters for the LightGBM model based on the data and evaluation metric.
        - Defines the search space for some parameters within the suggested parameters.
        - Creates the final parameter dictionary based on the suggested initial parameters and a step in the optimization search space grid.
        - Defines a pruning callback to stop training of unpromising trials.
        - Trains a given trial and validates it using the optimization_metric_func.

        Parameters:
            trial (optuna.Trial): The Optuna trial object representing a single execution of the optimization process.
            X (pd.DataFrame): The training features.
            y (pd.Series): The training labels.

        Returns:
            float: The optimization metric validation result.
        """
        optimization_metric_func = MetricHelpers.get_optimization_metric_func(self.metric)
        dtrain, dvalid, valid_x, valid_y = self._get_dtrain_dvalid_objects(X, y, self.metric, return_raw_valid=True)
        params: dict = self._sample_from_search_space(trial)
        # Add a callback for pruning.
        pruning_callback = optuna.integration.LightGBMPruningCallback(trial, MetricHelpers.get_pruning_metric(self.metric, self.target_classes))
        result = self._get_validation_score(trial, dtrain, dvalid, valid_x, valid_y, optimization_metric_func, params, pruning_callback)

        return result
    # ------------------------------------------------------------------------------------------
    def _check_refit_status(self, method: str) -> None:
            """
            Checks if refit is enabled before executing a method.

            Args:
                method (str): The name of the method being executed.

            Raises:
                ModuleNotFoundError: If refit is not enabled before executing the method.
            """
            if not self.refit:
                raise ModuleNotFoundError(f'LGBMTuner.fit(refit = True) must be applied before {method} execution')
    # ------------------------------------------------------------------------------------------
    def _populate_best_params_to_init_params(self, best_params: dict) -> dict:
        """Populate the learned params into the suggested params.

        Args:
            best_params (dict): The dictionary containing the best parameters.

        Returns:
            dict: The updated dictionary of parameters with the best parameters included.
        """
        # output params are temporary, because num_iterations tuning will follow
        temp_params = copy(self._init_params)
        for key, val in best_params.items():
            temp_params[key] = val
        # remove early_stopping & num_iterations from params (used during optuna optimization).
        # final early stopping will be trained during final_estimators_tuning
        if 'early_stopping_rounds' in temp_params:
            del temp_params['early_stopping_rounds']
        if 'num_iterations' in temp_params:
            del temp_params['num_iterations']
        return temp_params
    # ------------------------------------------------------------------------------------------

    def _save_feature_importances(self, train_features: pd.Index) -> None:
            """Save feature importances in class instance as a pd.Series.

            Args:
                train_features (pd.Index): The index of the training features.

            Returns:
                None
            """
            feat_importances: pd.Series = pd.Series(self._fitted_model.feature_importance(), index=train_features)
            normalized_importances = np.round((lambda x: x / sum(x))(feat_importances), 5)
            self._feature_importances = normalized_importances
    # ------------------------------------------------------------------------------------------

    @staticmethod
    def _set_optuna_verbosity(value: int) -> None:
        """Set optimization console output verbosity based on optuna.logging options.

        Args:
            value (int): The verbosity level to set.

        Returns:
            None
        """
        value_to_optuna_verbosity_dict: dict = {0 : 'CRITICAL',
                                          1 : 'CRITICAL',
                                          2 : 'ERROR',
                                          3 : 'WARNING',
                                          4 : 'INFO',
                                          5 : 'DEBUG'}
        optuna.logging.set_verbosity(getattr(optuna.logging, value_to_optuna_verbosity_dict[value]))
    # ------------------------------------------------------------------------------------------
    @staticmethod
    def _contains_float(iterable: Iterable) -> bool:
        """Check if any floats are present in the iterable.

        Args:
            iterable (Iterable): The iterable to check for floats.

        Returns:
            bool: True if any floats are present, False otherwise.
        """
        return float in [type(x) for x in iterable]

    @staticmethod
    def _all_ints(iterable: Iterable) -> bool:
        """
        Check if iterable contains only integers.

        Args:
            iterable (Iterable): The iterable to be checked.

        Returns:
            bool: True if all elements in the iterable are integers, False otherwise.
        """
        return bool(np.all([type(x)==int for x in iterable]))

    def _align_grid_and_search_space(self) -> None:
        """Redefine self.search_space for optuna based on self.grid which could be amended by user.

        This method aligns the grid and search space parameters for the tuner. It checks each parameter in the grid
        and determines the corresponding search space distribution based on the type and values of the grid parameter.

        Unsupported parameters are excluded from the search space and a warning is printed.

        Returns:
            None
        """
        unsupported_params: list = []
        for param_name, param_grid in self.grid.items():
            if param_name not in supported_gridsearch_params:
                unsupported_params.append(param_name)
                continue
            if isinstance(param_grid, list):
                self.search_space[param_name] = SearchSpace(Distribution.CHOICE, choices = param_grid)
            elif isinstance(param_grid, tuple):
                if self._contains_float(param_grid):
                    self.search_space[param_name] = SearchSpace(Distribution.UNIFORM, low = min(param_grid), high = max(param_grid))
                elif self._all_ints(param_grid):
                    self.search_space[param_name] = SearchSpace(Distribution.INTUNIFORM, low = min(param_grid), high = max(param_grid))
            elif isinstance(param_grid, dict):
                if 'choices' in param_grid:
                    self.search_space[param_name] = SearchSpace(Distribution.CHOICE, choices = param_grid['choices'])
                elif 'low' in param_grid:
                    if self._contains_float(param_grid.values()):
                        self.search_space[param_name] = SearchSpace(Distribution.UNIFORM, low = param_grid['low'], high = param_grid['high'])
                    elif self._all_ints(param_grid.values()):
                        self.search_space[param_name] = SearchSpace(Distribution.INTUNIFORM, low = param_grid['low'], high = param_grid['high'])
        if unsupported_params:
            self.printer.print(f'Following changed parameters are not supported for tuning: {unsupported_params}', order = 'error', trailing_blank_paragraph=True)
        self.grid = {key: value for key, value in self.grid.items() if key not in unsupported_params}
'''    
    # ------------------------------------------------------------------------------------------
    # Plotting methods
    # ------------------------------------------------------------------------------------------
    @final
    def plot_param_importances(self, 
                               study: optuna.Study,
                               save: bool = False,
                               display: bool = True) -> None:
        """
        Plots the parameter importances in the given Optuna study.

        Args:
            study (optuna.Study): The Optuna study containing the parameter importances.
            save (bool, optional): Whether to save the plot as an image file. Defaults to False.
            display (bool, optional): Whether to display the plot. Defaults to True.
        
        Returns:
            None        
        """
        self._plot_param_importances(study, save, display)
    # ------------------------------------------------------------------------------------------
    @final
    def plot_intermediate_values(self, 
                                 study: optuna.Study,
                                 legend: bool = False,
                                 save: bool = False,
                                 display: bool = True) -> None:
        """
        Plots the intermediate values of the study.

        Args:
            study (optuna.Study): The Optuna study containing the intermediate values.
            legend (bool, optional): Display the legend. Defaults to False.
            save (bool, optional): Save the plot as an image. Defaults to False.
            display (bool, optional): Display the plot. Defaults to True.

        Returns:
            None
        """
        self._plot_intermediate_values(study, legend, save, display)
    # ------------------------------------------------------------------------------------------
    @final
    def plot_optimization_history(self, study: optuna.Study, 
                                  save: bool = False,
                                  display: bool = True) -> None:
        """
        Plots the optimization history of the parameters in the given Optuna study.

        Args:
            study (optuna.Study): The Optuna study containing the optimization history.
            save (bool, optional): Whether to save the plot as a PNG file. Defaults to False.
            display (bool, optional): Whether to display the plot. Defaults to True.

        Returns:
            None
        """
        self._plot_optimization_history(study, save, display)
    # ------------------------------------------------------------------------------------------
    @final
    def plot_importances(self,
                        feature_importances: pd.Series, 
                        n_features: int = 15, 
                        figsize: tuple = (10,6), 
                        display: bool = True, 
                        dark: bool = True,
                        save: bool = True) -> None:
        """
        Plots the feature importances.

        Args:
            feature_importances (pd.Series): The feature importances.
            n_features (int, optional): Number of features to plot. Defaults to 15.
            figsize (tuple, optional): Figure size. Defaults to (10,6).
            display (bool, optional): Display the plot in a browser. If False, the plot will be saved in the current working directory. Defaults to True.
            dark (bool, optional): Display the dark or light version of the plot. Defaults to True.
            save (bool, optional): Save the plot to the current working directory. Defaults to True.

        Returns:
            None
        """
        self._plot_importances(feature_importances, n_features, figsize, display, dark, save)


'''