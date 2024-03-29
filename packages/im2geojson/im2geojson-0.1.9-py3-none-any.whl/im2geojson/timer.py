
"""
Timer Context Manager.
"""
from time import perf_counter


class Timer(object):
    """
    Create a Timer object.

    A context manager Timer object.

    Attributes
    ----------
    elapsed_time : int
        The elapsed time of the timer.
    """

    def __init__(self):
        """
        
        """
        self.elapsed_time = 0
        self._in_progress = None

    def __enter__(self):
        """Enter the runtime context and print status.
        """
        self._start = perf_counter()
        self._in_progress = True
        self.print_status()
        return self
    
    def __exit__(self, exc_type, exc_value, exc_traceback):
        """bool: Exit the runtime context and print status."""
        self._stop = perf_counter()
        self._in_progress = False
        self.elapsed_time = self._stop - self._start
        self.print_status()
        return False

    def print_status(self):
        """Print the current status."""
        if self._in_progress is None:
            print('Ready')
        elif self._in_progress:
            print('Running...')
        elif not self._in_progress:
            t = format(self.elapsed_time, '.2f')
            print(f'Finished in {t} seconds')

    @property
    def is_finished(self):
        """bool: Return True if timer has finished."""
        return self._in_progress is not None and not self._in_progress