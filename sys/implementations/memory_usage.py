#!/usr/bin/env python3
"""
Memory Usage Implementation

This module demonstrates various techniques for monitoring and analyzing
memory usage in Python applications using the sys module and related tools.
"""

import sys
import gc
import psutil
import os
from collections import defaultdict
from typing import Dict, List, Any, Optional, Tuple


def basic_memory_monitoring():
    """Demonstrate basic memory monitoring using sys.getallocatedblocks()"""
    print("Basic Memory Monitoring")
    print("=" * 25)

    # Get initial memory state
    initial_blocks = sys.getallocatedblocks()
    print(f"Initial allocated blocks: {initial_blocks}")

    # Create some objects
    data = []
    for i in range(1000):
        data.append([i] * 100)  # Create lists with repeated values

    after_creation = sys.getallocatedblocks()
    print(f"After creating 1000 lists: {after_creation}")
    print(f"Blocks created: {after_creation - initial_blocks}")

    # Delete objects
    del data
    gc.collect()  # Force garbage collection

    after_deletion = sys.getallocatedblocks()
    print(f"After deletion and GC: {after_deletion}")
    print(f"Blocks freed: {after_creation - after_deletion}")


def object_size_analysis():
    """Analyze memory usage of different Python objects"""
    print("\nObject Size Analysis")
    print("=" * 21)

    test_objects = {
        'integer': 42,
        'float': 3.14159,
        'string': "Hello, World!",
        'empty_list': [],
        'small_list': [1, 2, 3, 4, 5],
        'large_list': list(range(1000)),
        'empty_dict': {},
        'small_dict': {'a': 1, 'b': 2, 'c': 3},
        'large_dict': {i: i**2 for i in range(1000)},
        'tuple': (1, 2, 3, 4, 5),
        'set': {1, 2, 3, 4, 5},
        'frozenset': frozenset([1, 2, 3, 4, 5]),
    }

    print("Object sizes (shallow):")
    print("-" * 30)
    for name, obj in test_objects.items():
        size = sys.getsizeof(obj)
        print(f"{name:25} {size}")

    # Analyze list growth
    print("\nList size growth:")
    print("-" * 20)
    sizes = []
    for i in range(0, 1001, 100):
        lst = list(range(i))
        size = sys.getsizeof(lst)
        sizes.append((i, size))
        print(f"{i:8} {size}")

    # Analyze dict growth
    print("\nDictionary size growth:")
    print("-" * 25)
    dict_sizes = []
    for i in range(0, 1001, 100):
        d = {j: j for j in range(i)}
        size = sys.getsizeof(d)
        dict_sizes.append((i, size))
        print("8")


def recursive_memory_calculation():
    """Demonstrate recursive memory usage calculation"""
    print("\nRecursive Memory Calculation")
    print("=" * 30)

    def get_total_size(obj, seen=None):
        """Recursively calculate total memory usage"""
        if seen is None:
            seen = set()

        obj_id = id(obj)
        if obj_id in seen:
            return 0

        seen.add(obj_id)
        size = sys.getsizeof(obj)

        if isinstance(obj, (list, tuple, set, frozenset)):
            size += sum(get_total_size(item, seen) for item in obj)
        elif isinstance(obj, dict):
            size += sum(get_total_size(k, seen) + get_total_size(v, seen)
                       for k, v in obj.items())
        elif hasattr(obj, '__dict__'):
            size += get_total_size(obj.__dict__, seen)

        return size

    # Test with nested structures
    nested_data = {
        'numbers': list(range(100)),
        'nested': {
            'more_numbers': [i * 2 for i in range(50)],
            'text': ['item'] * 25
        },
        'matrix': [[j for j in range(10)] for i in range(10)]
    }

    shallow_size = sys.getsizeof(nested_data)
    deep_size = get_total_size(nested_data)

    print(f"Shallow size: {shallow_size} bytes")
    print(f"Deep size: {deep_size} bytes")
    print(f"Content overhead: {deep_size - shallow_size} bytes")


def memory_profile_function(func):
    """Decorator to profile memory usage of functions"""
    def wrapper(*args, **kwargs):
        # Get initial memory state
        initial_blocks = sys.getallocatedblocks()

        # Record starting time and memory
        start_time = __import__('time').time()

        # Execute function
        result = func(*args, **kwargs)

        # Calculate execution time
        end_time = __import__('time').time()
        execution_time = end_time - start_time

        # Get final memory state
        final_blocks = sys.getallocatedblocks()
        blocks_used = final_blocks - initial_blocks

        print(f"\nMemory profile for {func.__name__}:")
        print(f"  Execution time: {execution_time:.4f} seconds")
        print(f"  Memory blocks used: {blocks_used}")
        print(f"  Initial blocks: {initial_blocks}")
        print(f"  Final blocks: {final_blocks}")

        return result
    return wrapper


@memory_profile_function
def memory_intensive_operation():
    """A memory-intensive operation for profiling"""
    data = []
    for i in range(1000):
        # Create nested data structures
        item = {
            'id': i,
            'data': list(range(100)),
            'metadata': {'created': True, 'size': 100}
        }
        data.append(item)

    # Process data
    total = sum(item['id'] for item in data)
    return total


def reference_counting_demo():
    """Demonstrate reference counting concepts"""
    print("\nReference Counting Demo")
    print("=" * 25)

    def show_refcount(obj, label):
        """Show reference count for an object"""
        count = sys.getrefcount(obj)
        print(f"{label}: {count} references")

    # Create an object
    test_list = [1, 2, 3]
    show_refcount(test_list, "After creation")

    # Create additional references
    ref1 = test_list
    ref2 = test_list
    show_refcount(test_list, "After creating refs")

    # Add to container
    container = [test_list]
    show_refcount(test_list, "After adding to container")

    # Pass to function (creates temporary reference)
    show_refcount(test_list, "Inside function call")

    # Delete references
    del ref1
    show_refcount(test_list, "After deleting ref1")

    del ref2
    show_refcount(test_list, "After deleting ref2")

    del container[0]
    show_refcount(test_list, "After removing from container")


def memory_efficient_data_structures():
    """Compare memory usage of different data structures"""
    print("\nMemory-Efficient Data Structures")
    print("=" * 35)

    # Test different ways to store the same data
    data_size = 1000

    # Method 1: List of tuples
    list_of_tuples = [(i, i**2, f"item_{i}") for i in range(data_size)]
    list_size = sys.getsizeof(list_of_tuples)
    for item in list_of_tuples:
        list_size += sys.getsizeof(item)

    # Method 2: List of lists
    list_of_lists = [[i, i**2, f"item_{i}"] for i in range(data_size)]
    list_list_size = sys.getsizeof(list_of_lists)
    for item in list_of_lists:
        list_list_size += sys.getsizeof(item)

    # Method 3: Dictionary
    dict_data = {i: {'square': i**2, 'name': f"item_{i}"} for i in range(data_size)}
    dict_size = sys.getsizeof(dict_data)
    for key, value in dict_data.items():
        dict_size += sys.getsizeof(key) + sys.getsizeof(value)

    # Method 4: Class instances
    class DataItem:
        def __init__(self, id_val, square, name):
            self.id = id_val
            self.square = square
            self.name = name

    class_instances = [DataItem(i, i**2, f"item_{i}") for i in range(data_size)]
    class_size = sys.getsizeof(class_instances)
    for item in class_instances:
        class_size += sys.getsizeof(item) + sys.getsizeof(item.__dict__)

    print("Memory usage comparison:")
    print(f"  List of tuples: {list_size} bytes")
    print(f"  List of lists:  {list_list_size} bytes")
    print(f"  Dictionary:     {dict_size} bytes")
    print(f"  Class instances: {class_size} bytes")

    # Find most efficient
    methods = {
        'List of tuples': list_size,
        'List of lists': list_list_size,
        'Dictionary': dict_size,
        'Class instances': class_size
    }

    most_efficient = min(methods.items(), key=lambda x: x[1])
    print(f"\nMost memory efficient: {most_efficient[0]} ({most_efficient[1]} bytes)")


def garbage_collection_insights():
    """Demonstrate garbage collection behavior"""
    print("\nGarbage Collection Insights")
    print("=" * 30)

    # Create objects with circular references
    class Node:
        def __init__(self, value):
            self.value = value
            self.next = None

    # Create circular reference
    node1 = Node(1)
    node2 = Node(2)
    node1.next = node2
    node2.next = node1

    initial_blocks = sys.getallocatedblocks()
    print(f"Blocks before circular reference: {initial_blocks}")

    # Delete references
    del node1
    del node2

    after_del = sys.getallocatedblocks()
    print(f"Blocks after deleting references: {after_del}")

    # Force garbage collection
    collected = gc.collect()
    after_gc = sys.getallocatedblocks()

    print(f"Objects collected by GC: {collected}")
    print(f"Blocks after GC: {after_gc}")
    print(f"Blocks freed by GC: {after_del - after_gc}")


def system_memory_monitoring():
    """Monitor system memory usage (requires psutil)"""
    print("\nSystem Memory Monitoring")
    print("=" * 26)

    try:
        import psutil
        process = psutil.Process(os.getpid())

        # Get memory information
        memory_info = process.memory_info()
        memory_percent = process.memory_percent()

        print(f"Process RSS (Resident Set Size): {memory_info.rss} bytes")
        print(f"Process VMS (Virtual Memory Size): {memory_info.vms} bytes")
        print(f"Memory usage percentage: {memory_percent:.2f}%")

        # System memory
        system_memory = psutil.virtual_memory()
        print(f"System total memory: {system_memory.total} bytes")
        print(f"System available memory: {system_memory.available} bytes")
        print(f"System memory usage: {system_memory.percent:.2f}%")

    except ImportError:
        print("psutil not available. Install with: pip install psutil")
        print("Falling back to basic memory info...")

        # Basic fallback using sys
        print(f"Max size (sys.maxsize): {sys.maxsize}")
        print(f"Max size in MB: {sys.maxsize // (1024*1024)} MB")


def memory_leak_detection():
    """Simple memory leak detection"""
    print("\nMemory Leak Detection")
    print("=" * 22)

    def create_objects(count):
        """Create some objects and return them"""
        return [{'data': list(range(100)), 'id': i} for i in range(count)]

    # Baseline
    gc.collect()
    baseline_blocks = sys.getallocatedblocks()
    baseline_objects = len(gc.get_objects())

    print(f"Baseline - Blocks: {baseline_blocks}, Objects: {baseline_objects}")

    # Create objects
    data = create_objects(100)
    after_creation_blocks = sys.getallocatedblocks()
    after_creation_objects = len(gc.get_objects())

    print(f"After creation - Blocks: {after_creation_blocks}, Objects: {after_creation_objects}")
    print(f"Created - Blocks: {after_creation_blocks - baseline_blocks}, Objects: {after_creation_objects - baseline_objects}")

    # Delete objects
    del data
    gc.collect()

    after_deletion_blocks = sys.getallocatedblocks()
    after_deletion_objects = len(gc.get_objects())

    print(f"After deletion - Blocks: {after_deletion_blocks}, Objects: {after_deletion_objects}")
    print(f"Remaining - Blocks: {after_deletion_blocks - baseline_blocks}, Objects: {after_deletion_objects - baseline_objects}")

    # Check for potential leaks
    block_diff = after_deletion_blocks - baseline_blocks
    object_diff = after_deletion_objects - baseline_objects

    if block_diff > 100:  # Allow some tolerance
        print(f"⚠️  Potential memory leak detected: {block_diff} extra blocks")
    else:
        print("✓ Memory appears to be properly cleaned up")


def main():
    """Main function to run all memory usage examples"""

    examples = {
        'basic': basic_memory_monitoring,
        'sizes': object_size_analysis,
        'recursive': recursive_memory_calculation,
        'profile': lambda: memory_intensive_operation(),
        'refcount': reference_counting_demo,
        'efficient': memory_efficient_data_structures,
        'gc': garbage_collection_insights,
        'system': system_memory_monitoring,
        'leaks': memory_leak_detection,
    }

    if len(sys.argv) < 2:
        print("Memory Usage Analysis Examples")
        print("==============================")
        print()
        print("Available examples:")
        for name in examples.keys():
            print(f"  {name}")
        print()
        print("Usage: python memory_usage.py <example_name>")
        print("Example: python memory_usage.py basic")
        return

    example_name = sys.argv[1].lower()

    if example_name in examples:
        try:
            examples[example_name]()
        except Exception as e:
            print(f"Error running example '{example_name}': {e}")
            import traceback
            traceback.print_exc()
    else:
        print(f"Unknown example: {example_name}")
        print(f"Available examples: {', '.join(examples.keys())}")
        sys.exit(1)


if __name__ == "__main__":
    main()
