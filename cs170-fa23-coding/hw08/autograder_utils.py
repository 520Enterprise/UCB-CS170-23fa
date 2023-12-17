import time
import signal
import contextlib
import cProfile

def is_independent_set(adj_list, vertices):
    """
    Return True if vertices is an independent set in adj_list, False otherwise.

    args:
        adj_list:List[List[int]] = the adjacency list of the graph
        vertices:List[int] = a list of vertices

    return:
        bool: True if vertices is an independent set in adj_list, False otherwise.
    """
    for u in vertices:
        for v in vertices:
            if u != v and v in adj_list[u]:
                return False
    return True

class TimeoutException(Exception):
    def __init__(self, message="Operation timed out"):
        super().__init__(message)

@contextlib.contextmanager
def handle_timeout(seconds):
    def timeout_handler(num, stack):
        raise TimeoutException("Code execution timed out")
    
    # no-op if signal module is not available (for Windows compatability)
    if hasattr(signal, 'SIGALRM') and hasattr(signal, 'alarm'):
        # Set up the signal handler for SIGALRM (alarm signal)`
        signal.signal(signal.SIGALRM, timeout_handler)
        # Set the alarm to trigger after the specified number of seconds
        signal.alarm(seconds)
    
    try:
        yield
    except TimeoutException as e:
        print(e)
    finally:
        # no-op if signal module is not available (for Windows compatability)
        if hasattr(signal, 'SIGALRM') and hasattr(signal, 'alarm'):
            # Cancel the alarm regardless of whether an exception occurred or not
            signal.alarm(0)
    
def validate_tour(tour, dist_arr):
    """Returns the length of the tour if it is valid, -1 otherwise
    """
    n = len(tour)
    cost = 0
    for i in range(n):
        if dist_arr[tour[i-1]][tour[i]] == float('inf'):
            return -1
        cost += dist_arr[tour[i-1]][tour[i]]
    return cost
    
class TimerWrapper:
    def __init__(self, func):
        self.func = func
        self.elapsed_time = 0

    def __call__(self, *args, **kwargs):
        start = time.time()
        result = self.func(*args, **kwargs)
        self.elapsed_time += time.time() - start
        return result