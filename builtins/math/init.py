# Imports
from extra_modules.context_and_datatypes import *
import os

# Initalise
module_name = 'math'
to_be_pushed = []

# Get funcs & variables #TODO!
spec = importlib.util.spec_from_file_location('math_constants', os.path.join(os.path.dirname(__file__), 'math_constants.py'))
my_module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(my_module)
to_be_pushed.extend(getattr(my_module,'local_pusher'))

'''
spec = importlib.util.spec_from_file_location('math_linalg', os.path.join(os.path.dirname(__file__), 'math_linalg.py'))
my_module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(my_module)
to_be_pushed.extend(getattr(my_module,'local_pusher'))
'''

spec = importlib.util.spec_from_file_location('math_functions', os.path.join(os.path.dirname(__file__), 'math_functions.py'))
my_module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(my_module)
to_be_pushed.extend(getattr(my_module,'local_pusher'))