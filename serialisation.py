import pickle
import os
import extra_modules.Errors as err
import AILang as ail
import time

class SharedBuffer:
    def __init__(self, fn):
        ap = os.path.abspath(__file__)
        self.fn = os.path.join(os.path.dirname(ap), 'shareddata', fn)

    def rec_ail2py(self, obj, ctx):
        if hasattr(obj, 'value'):
            to_push = obj.value
        elif hasattr(obj, 'elements'):
            x = obj.elements[:]
            to_push = []
            for e in x:
                ex = self.rec_ail2py(e, ctx)
                to_push.append(ex)
                if isinstance(ex, ail.RTResult):
                    return ex
        elif isinstance(obj, ail.BaseFunction):
            to_push = ail.RTResult().failure(err.LTPError(
                obj.pos_start, obj.pos_end,
                'AIL functions cannot be converted to Python (try converting its output to a Python datatype instead)',
                ctx
            ))
        else:
            to_push = ail.RTResult().failure(err.LTPError(
                obj.pos_start, obj.pos_end,
                'Equivalant Python datatype of input object not found',
                ctx
            ))
        
        return to_push
    
    def rec_py2ail(self, obj, parent: ail.BuiltInFunction, ctx) -> ail.RTResult: #TODO: FIX ME! (add list recursion)
        _type = type(obj)

        if _type is str:
            return ail.RTResult().success(ail.String(obj))
        elif _type is int or _type is float:
            return ail.RTResult().success(ail.Number(obj))
        elif _type is complex:
            return ail.RTResult().success(ail.IterArray([ail.Number(obj.real), ail.Number(obj.imag)]))
        elif _type is bool:
            return ail.RTResult().success(ail.Number(int(obj)))
        elif _type is list or tuple: #SAVE ME!!!!!! PLEASE
            x = list(obj)
            tpx = []
            for e in x:
                ex: ail.RTResult = self.rec_py2ail(e, parent, ctx)
                if ex.should_return():
                    return ex
                else:
                    tpx.append(ex.value)
            return ail.RTResult().success(ail.IterArray(tpx))
        elif _type is None:
            return ail.RTResult().success(ail.Number.null)
        elif _type is bytes or _type is bytearray:
            return ail.RTResult().success(ail.IterArray([ail.Number(int(byte)) for byte in obj]))
        else: 
            return ail.RTResult().failure(err.LTPError(
                parent.pos_start, parent.pos_end,
                f'Equivalant AILang datatype of object in shared memory buffer not found',
                ctx
            ))
    def write_frm_ail(self, obj, ctx):
        # Datatype conversion
        to_push = self.rec_ail2py(obj, ctx)
        if type(to_push) is ail.RTResult: return to_push
        
        # Serialisation and dumping
        try:
            with open(self.fn, 'wb') as f:
                pickle.dump(to_push, f)
            return ail.RTResult().success(ail.Number.null)
        except Exception as e:
            return ail.RTResult().failure(err.IOError(
                obj.pos_start, obj.pos_end,
                f'Failed to complete serialisation and dumping of object' +
                e,
                ctx
            ))
        
    def read_frm_ail(self, parent: ail.BuiltInFunction, ctx):
        try:
            with open(self.fn, 'rb') as f:
                python_obj = pickle.load(f)
            return self.rec_py2ail(python_obj, parent, ctx)
        except Exception as e:
            return ail.RTResult().failure(err.IOError(
                parent.pos_start, parent.pos_end,
                f'Failed to complete deserialisation of object' +
                e,
                ctx
            ))

    def write_frm_py(self, obj):
        with open(self.fn, 'wb') as f:
            pickle.dump(obj, f)

    def read_frm_py(self):
        with open(self.fn, 'rb') as f:
            return pickle.load(f)
        
    def wait_for_write(self):
        if not os.path.isfile(self.fn):
            while not os.path.isfile(self.fn):
                time.sleep(0.5)
        else:
            current_modified = last_modified = os.path.getmtime(self.fn)
            while current_modified != last_modified:
                current_modified = os.path.getmtime(self.fn)
                time.sleep(0.5)

    
#TODO: TEST MEH!!! (LTP)