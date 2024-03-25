# Created on Wed Apr 27 17:51:24 2022
# Original code from DanilZherebtsov, licensed under the MIT License.
# Modifications (2024-03-23) made by Daniel Porsmose.

from functools import wraps
import traceback
from typing import Any, Union


class Printer: # mypy ignore
    __version__: str = '0.1.2'
    
    def __init__(self, verbose: bool = True) -> None:
        self.verbose: bool = verbose 

    def print(self, 
              message: Union[str, None] = None, 
              order: Union[None, int, str]  = 1, 
              breakline: Union[None, str] = None, 
              force_print: Union[None, bool] = None, 
              leading_blank_paragraph: bool = False, 
              trailing_blank_paragraph: bool = False) -> None:
        """Output messages to the console based on seniority level (order).

        Args:
            message (str, optional): The message to print. Default is None.
            order (int or str, optional): The order to tabulate the message print. Can take values between 1 and 4, or 'error'. The default is 1.
            breakline (str, optional): The string symbol to print a breakline. Default is None.
            force_print (bool, optional): If True, the message will be printed even if self.verbose == False. Applicable for non-error important messages that need to be printed. Default is None.
            leading_blank_paragraph (bool, optional): If True, a leading blank paragraph will be added before the message. Default is False.
            trailing_blank_paragraph (bool, optional): If True, a trailing blank paragraph will be added after the message. Default is False.

        Returns:
            None: This method does not return anything.

        Note:
            order=0 - program title print
            order=1 - major function title print
            order=2 - minor function title print
            order=3 - internal function first order results
            order=4 - internal function second order results
            order=5 - internal function third order results
            order='error' - error message print including traceback

        """
        leading_blank = '\n' if leading_blank_paragraph else ''
        trailing_blank = '\n' if trailing_blank_paragraph else ''

        message_prefix = {
            1       :"\n * ",
            2       :"\n   - ",
            3       :"     . ",
            4       :"     .. ",
            5       :"     ... ",
            'error' : f"{traceback.format_exc()}\n! "
        }
        
        if order!='error' and not self.verbose and not force_print:
            return None

        if not message:
            if breakline:
                print(f' {breakline*75}')
        else:
            if order == 0:
                print('\n')
                print('-'*75)
                print(f'{message}')
                print('-'*75)
            else:
                print(f'{leading_blank}{message_prefix[order]}{message}{trailing_blank}')
                if breakline: 
                    print(f' {breakline*75}')
