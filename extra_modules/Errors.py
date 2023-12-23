from extra_modules.string_with_arrows import string_with_arrows

# PYTHON-WISE MODULE LOAD ERROR

class RequiredModuleNotLoaded(Exception):
    pass

# GENERAL ERRORS

class Error:
    def __init__(self, pos_start, pos_end, error_name, details):
        self.pos_start = pos_start
        self.pos_end = pos_end
        self.error_name = error_name
        self.details = details

    def as_str(self):
        result  = f'{self.error_name}: {self.details}'
        result += '\n' + f'File {self.pos_start.fn}, line {self.pos_start.ln + 1}'
        result += '\n\n' + string_with_arrows(self.pos_start.ftxt, self.pos_start, self.pos_end)
        return result
    
class IllegalCharError(Error):
    def __init__(self, pos_start, pos_end, details):
        super().__init__(pos_start, pos_end, 'Illegal Character', details)

class ExpectedCharError(Error):
    def __init__(self, pos_start, pos_end, details):
        super().__init__(pos_start, pos_end, 'Expected Character', details)

class InvalidSyntaxError(Error):
    def __init__(self, pos_start, pos_end, details):
        super().__init__(pos_start, pos_end, 'Invalid Syntax', details)

class SyntaxNotImplementedError(Error):
    def __init__(self, pos_start, pos_end, details):
        super().__init__(pos_start, pos_end, 'Invalid Syntax', details)

class RTError(Error):
    def __init__(self, pos_start, pos_end, details, context):
        super().__init__(pos_start, pos_end, 'Runtime Error', details)
        self.context = context

    def as_str(self):
        result  = self.generate_traceback()
        result += '\n' + f'{self.error_name}: {self.details}'
        result += '\n\n' + string_with_arrows(self.pos_start.ftxt, self.pos_start, self.pos_end)
        return result

    def generate_traceback(self):
        result = ''
        pos = self.pos_start
        ctx = self.context

        while ctx:
            result = '\n' + f'  File {pos.fn}, line {pos.ln + 1}, in {ctx.display_name}' + result
            pos = ctx.parent_entry_pos
            ctx = ctx.parent

        return 'Traceback (most recent call last):' + result
    
class FunctionalityNotImplementedError(RTError):
    def __init__(self, pos_start, pos_end, details, context):
        super().__init__(pos_start, pos_end, details, context)
        self.error_name = 'Functionality Not Implemented Error'

class IntegerOverflowError(RTError):
    def __init__(self, pos_start, pos_end, details, context):
        super().__init__(pos_start, pos_end, details, context)
        self.error_name = 'Integer Overflow Error'

class MallocError(RTError):
    def __init__(self, pos_start, pos_end, details, context):
        super().__init__(pos_start, pos_end, details, context)
        self.error_name = 'Memory Allocation Error'

class FileOperationError(RTError):
    def __init__(self, pos_start, pos_end, details, context):
        super().__init__(pos_start, pos_end, details, context)
        self.error_name = 'File Operation Error'

class PLoadError(FileOperationError):
    def __init__(self, pos_start, pos_end, details, context):
        super().__init__(pos_start, pos_end, details, context)
        self.error_name = 'External Program Loading Error'

class MLoadError(FileOperationError):
    def __init__(self, pos_start, pos_end, details, context):
        super().__init__(pos_start, pos_end, details, context)
        self.error_name = 'Module Loading Error'

class LTPError(RTError):
    def __init__(self, pos_start, pos_end, details, context):
        super().__init__(pos_start, pos_end, details, context)
        self.error_name = 'Link To Python Error'

class UnknownRTError(RTError):
    def __init__(self, pos_start, pos_end, details, context):
        super().__init__(pos_start, pos_end, details, context)
        self.error_name = 'Unknown Runtime Error'