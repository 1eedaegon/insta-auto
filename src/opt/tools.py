import os
import sys
import time
import logging

logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")


def timed(func):
    """ Decorator used to benchmark function runtime"""

    def wrapped(*arg, **kwarg):
        target_base_name = sys.argv[0]
        # target_base_name = os.path.basename(__file__).split(".")[0].capitalize()
        target_function_name = func.__name__
        st = time.time()
        result = func(*arg, **kwarg)
        et = time.time()
        logging.info(
            f"[{target_base_name}][{target_function_name}] - Elapsed time: {(et-st):2.2f}"
        )
        return result

    return wrapped

