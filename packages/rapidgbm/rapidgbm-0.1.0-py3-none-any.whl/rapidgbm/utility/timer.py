# Created on Wed Apr 27 17:51:24 2022
# Original code from DanilZherebtsov, licensed under the MIT License.
# Modifications (2024-03-23) made by Daniel Porsmose.

import time
from functools import wraps
from typing import Any

from typing import Any
import time
from functools import wraps

from typing import Any
import time
from functools import wraps

def timer(func: Any) -> Any:
    '''
    Decorator to print func execution time

    Args:
        func: The function to decorate.

    Returns:
        The wrapped function.

    Examples:
        @timer
        def my_function():
            # code here
            pass

    '''
    
    @wraps(func)
    def wrapped(*args, **kwargs) -> Any:
        start = time.time()
        result = func(*args, **kwargs)
        elapsed = round(time.time() - start, 5)
        if elapsed < 60:
            print(f"\nTime elapsed for {func.__name__} execution: {elapsed} seconds")
        elif 60 < elapsed < 3600:
            minutes = int(elapsed/60)
            seconds = round(elapsed%60,3)
            print(f"\nTime elapsed for {func.__name__} execution: {minutes} min {seconds} sec")
        else:
            hours = int(elapsed // 60 // 60)
            minutes = int(elapsed // 60 % 60)
            seconds = int(elapsed % 60)
            print(f"\nTime elapsed for function {func.__name__} execution: {hours} hour(s) {minutes} min {seconds} sec")
        return result
    return wrapped