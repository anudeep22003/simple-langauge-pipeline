import functools
import time


class Decorators:

    def debug(func):
        """Print the function signature and return value"""
        @functools.wraps(func)
        def wrapper_debug(*args, **kwargs):
            args_repr = [repr(a) for a in args]                      # 1
            kwargs_repr = [f"{k}={v!r}" for k, v in kwargs.items()]  # 2
            signature = ", ".join(args_repr + kwargs_repr)           # 3
            print(f"Calling {func.__name__}({signature})")
            value = func(*args, **kwargs)
            print(f"{func.__name__!r} returned {value!r}")           # 4
            return value
        return wrapper_debug

    def timer(func):
        """Print the runtime of the decorated function"""
        @functools.wraps(func)
        def wrapper_timer(*args, **kwargs):
            start_time = time.perf_counter()    # 1
            value = func(*args, **kwargs)
            end_time = time.perf_counter()      # 2
            run_time = end_time - start_time    # 3
            print(f"------------------- Finished {func.__name__!r} in {run_time:.4f} secs -------------------")
            return value
        return wrapper_timer

    def catch_exception(func):
        """ Automatically insert a try block and catch and explain exception is caught."""
        @functools.wraps(func)
        def catcher(*args, **kwargs):
            try: 
                catcher(*args, **kwargs)
            except Exception as e:
                print(f"Exception caught: {type(e)!r}\t args: {e.args}")
    
    def singleton(cls, *args, **kwargs):
        """ 
        To ensure that only a single instance of a class is created
        Will be particularly useful for socket connection handler classes such as:
        - Sql interfacer
        - neo4j interfacer 
        - Sidebrain backend interfacer
        """
        instances = {}
        print(f'Dict {{instances}} value:{str(instances.items())}')
        
        @functools.wraps(cls)
        def _singleton(*args, **kwargs):
            if cls not in instances:
                instances[cls]=cls(*args, **kwargs)
                print(f'Dict {{instances}} value:{str(instances.items())} after a pass')
            return instances[cls]
        return _singleton
    
    def logger(func):
        """ Log the function to a text file """
        
        def _logger(*args, **kwargs):
            with open('/Users/anudeepyegireddi/Development/Sidebrain/nlp-apps/simple-language-pipeline/src/data/log_file.txt', mode = 'a') as f:
                f.write(f"Function:  {func.__name__}\n")
                value = func(*args, **kwargs)
                f.write(str(value))
            
            return value
            
        return _logger
