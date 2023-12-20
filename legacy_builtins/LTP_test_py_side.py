# /Library/Frameworks/Python.framework/Versions/3.11/bin/python3.11 "/Volumes/Data stuffs/Python/AILang/builtins/LTP_test_py_side.py"
import sys, os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import serialisation as ser

buf = ser.SharedBuffer('test.ser')
buf.wait_for_write()
buf.wait_for_write()

print(buf.read_frm_py())