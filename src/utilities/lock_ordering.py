from contextlib import contextmanager

@contextmanager
def ordered_locks(nodes, lock_attr='lock', lock_type='gen_rlock'):
    """Acquire read/write locks on nodes in global order to avoid deadlocks"""
    sorted_nodes = sorted(nodes, key=lambda n: id(n)) # Sort nodes by their id to ensure a consistent order
    locks = [getattr(getattr(n, lock_attr), lock_type)() for n in sorted_nodes]
    try:
        for lock in locks:
            lock.acquire()
        yield
    finally:
        for lock in reversed(locks):  # release in reverse order
            lock.release()