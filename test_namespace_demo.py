import sys
import os

# Add the test_namespace directory to Python path
sys.path.insert(0, '/Users/pradeepsahu/dev_data/CodeExcutingAgent/test_namespace')

print("=== Testing Implicit Namespace Packages ===")

try:
    # This should work without any __init__.py files
    from mypkg.module1 import hello_from_module1, MyClass
    print("✅ Successfully imported from mypkg.module1")
    print(f"   Result: {hello_from_module1()}")
    
    obj = MyClass()
    print(f"   Class instance: {obj.name}")
    
except ImportError as e:
    print(f"❌ Failed to import from mypkg.module1: {e}")

try:
    # This should also work
    from mypkg.subpkg.module2 import hello_from_module2, calculate
    print("✅ Successfully imported from mypkg.subpkg.module2")
    print(f"   Result: {hello_from_module2()}")
    print(f"   Calculate 5+3 = {calculate(5, 3)}")
    
except ImportError as e:
    print(f"❌ Failed to import from mypkg.subpkg.module2: {e}")

# Check if these are namespace packages
import mypkg
print(f"\n=== Package Information ===")
print(f"mypkg.__path__: {mypkg.__path__}")
print(f"mypkg.__file__: {getattr(mypkg, '__file__', 'No __file__ (namespace package)')}")

import mypkg.subpkg
print(f"mypkg.subpkg.__path__: {mypkg.subpkg.__path__}")
print(f"mypkg.subpkg.__file__: {getattr(mypkg.subpkg, '__file__', 'No __file__ (namespace package)')}")