Probe attribute presence without invoking descriptors in the
assigner core: fixes infinite recursion on Python 3.15, where caching
dataclass docstring descriptors write during reads, while preserving
first-write acceptance for uninitialized slots.
