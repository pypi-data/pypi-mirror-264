# Original code from DanilZherebtsov, licensed under the MIT License.
# Modifications made by Daniel Porsmose.

import os
import matplotlib.pyplot as plt
from rapidgbm.utility.validators import Validators
from optuna.visualization.matplotlib import plot_optimization_history, plot_param_importances, plot_intermediate_values
from typing import final
import pandas as pd
import optuna

class PlottingMixin:
    def __configure_matplotlib_style(self, dark: bool = True) -> None:
        '''Configure matplotlib style for plots.

        Args:
            dark (bool): Flag indicating whether to use a dark style. Default is True.

        Returns:
            None
        '''
        try:
            styles = plt.style.available
            if dark:
                styles_to_set = ['dark_background']
                for style in styles:
                    if 'deep' in style:
                        styles_to_set.append(style)
            else:
                styles_to_set = []
                for style in styles:
                    if 'pastel' in style:
                        styles_to_set.append(style)
            for style in styles_to_set:
                plt.style.use(style)
        except Exception as e:
            print(f'Error while configuring matplotlib style: {e}')
            print('Default style will be used')
            pass
    # ------------------------------------------------------------------------------------------
    def _plot_static_fim(self,
                        feat_imp: pd.Series, 
                        figsize: tuple = (10,6), 
                        dark: bool = True,
                        save: bool = False,
                        display: bool = True) -> None:
        """
        Plot feature importance as a horizontal bar chart.

        Args:
            feat_imp (pd.Series): Feature importance values.
            figsize (tuple, optional): Figure size. Defaults to (10,6).
            dark (bool, optional): Dark theme. Defaults to True.
            save (bool, optional): Save figure. Defaults to False.
            display (bool, optional): Display figure. Defaults to True.
        
        Returns:
            None.
        """
        fig, ax = plt.subplots(figsize=figsize)
        plt.tight_layout()
        ax.spines['top'].set_visible(False)
        ax.spines['right'].set_visible(False)
        ax.spines['left'].set_visible(False)
        ax.spines['bottom'].set_visible(False)
        self.__configure_matplotlib_style(dark)

        if dark:
            name = 'FIM_DARK'
            ax.barh(feat_imp.index, feat_imp, alpha=0.8, color='#F99245')
            fig.set_facecolor('#20253c')
            ax.set_facecolor('#20253c')
            ax.tick_params(axis='x', colors='white')
            ax.tick_params(axis='y', colors='white')
            ax.set_title('Feature importances (sum up to 1)', color='white')
        else:
            name = 'FIM_LIGHT'
            ax.barh(feat_imp.index, feat_imp, alpha=0.8, color='#007bff')
            fig.set_facecolor('#dee0eb')
            ax.set_facecolor('#dee0eb')
            ax.tick_params(axis='x', colors='#212529')
            ax.tick_params(axis='y', colors='#212529')
            ax.set_title('Feature importances (sum up to 1)', color='#212529')
        if save:
            plt.savefig(f'{name}.png', dpi=300, facecolor=fig.get_facecolor(),
                        edgecolor='none', bbox_inches='tight')
            print(f'Feature Importance Plot is saved to {os.path.join(os.getcwd(), f"{name}.png")}')
        if display:
            plt.show()
    # ------------------------------------------------------------------------------------------
    def plot_importances(self,
                         feature_importances: pd.Series, 
                         n_features: int = 15, 
                         figsize: tuple = (10,6), 
                         display: bool = True, 
                         dark: bool = True,
                         save: bool = True) -> None:
        '''
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
        '''
        Validators.validate_plot_importances_n_features_argument(n_features)
        Validators.validate_plot_importances_figsize_argument(figsize)

        importances_for_png_plot = feature_importances.nlargest(n_features).sort_values()           
        self._plot_static_fim(importances_for_png_plot, 
                                figsize = figsize, 
                                dark = dark, 
                                save = save,
                                display = display)
    # ------------------------------------------------------------------------------------------
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

        plot_optimization_history(study)
        
        if save:
            name = "optimization_history"
            plt.savefig(f'{name}.png', dpi=300,
                        edgecolor='none', bbox_inches='tight')
            print(f"Optimization History Plot is saved to {os.path.join(os.getcwd(), f'{name}.png')}")
        if display:
            plt.show()
    # ------------------------------------------------------------------------------------------
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

        plot_param_importances(study)
        
        if save:
            name = "param_importances"
            plt.savefig(f'{name}.png', dpi=300,
                        edgecolor='none', bbox_inches='tight')
            print(f"Parameter Importance Plot is saved to {os.path.join(os.getcwd(), f'{name}.png')}")
        if display:
            plt.show()
     
    # ------------------------------------------------------------------------------------------
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
        Validators.validate_plotting_legend_argument(legend)

        fig = plot_intermediate_values(study)
        if not legend:
            fig.get_legend().remove()
        
        if save:
            name = "intermediate_values"
            plt.savefig(f'{name}.png', dpi=300,
                        edgecolor='none', bbox_inches='tight')
            print(f"Intermediate Values Plot is saved to {os.path.join(os.getcwd(), f'{name}.png')}")
        if display:
            plt.show()