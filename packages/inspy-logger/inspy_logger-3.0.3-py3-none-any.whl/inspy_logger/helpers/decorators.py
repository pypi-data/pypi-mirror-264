"""


Author: 
    Inspyre Softworks

Project:
    inSPy-Logger

File: 
    inspy_logger/helpers/decorators.py
 

Description:
    Contains decorators used by the inSPy-Logger package.

"""


def method_alias(*alias_names: (str, list[str])):
    """
    A decorator that allows you to add aliases to a class's method.

    Args:
        *alias_names (str, list[str]):
            The name(s) of the alias(es) to add.

    Returns:
        method:
            The decorated method.
    """
    def method_decorator(meth):
        meth._alias_names = alias_names
        return meth

    return method_decorator


def method_logger(func):
    """
    A decorator to log a method's execution.

    Args:
        func (method):
            The method to log.

    Returns:
        method:
            The decorated method.
    """
    def wrapper(self, *args, **kwargs):
        # Set up the logger with method-specific config.
        name = f'{self.__class__.__name__}.{func.__name__}'
        logger = self.class_logger.get_child()

        # Add the logger to the instance for use in the method
        self._current_logger = logger

        # Execute the called method
        res = func(self, *args, **kwargs)

        # Remove the logger after method execution
        del self._current_logger

        return res
    return wrapper


def add_aliases(cls):
    """
    A decorator to add aliases to a class's methods.

    Args:
        cls (class):
            The class to add aliases to.

    Returns:
        class:
            The decorated class.
    """
    for name, method in list(cls.__dict__.items()):
        if hasattr(method, '_alias_names'):
            for alias_name in method._alias_names:
                setattr(cls, alias_name, method)
    return cls
