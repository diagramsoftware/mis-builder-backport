# -*- coding: utf-8 -*-
# Copyright 2016-2018 ACSONE SA/NV (<http://acsone.eu>)
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

import traceback

from openerp.tools.safe_eval import test_expr, _SAFE_OPCODES, _import

from .data_error import DataError, NameDataError

_BUILTINS = {
    '__import__': _import,
    'True': True,
    'False': False,
    'None': None,
    'str': str,
    'unicode': unicode,
    'bool': bool,
    'int': int,
    'float': float,
    'long': long,
    'enumerate': enumerate,
    'dict': dict,
    'list': list,
    'tuple': tuple,
    'map': map,
    'abs': abs,
    'min': min,
    'max': max,
    'sum': sum,
    'reduce': reduce,
    'filter': filter,
    'round': round,
    'len': len,
    'repr': repr,
    'set': set,
    'all': all,
    'any': any,
    'ord': ord,
    'chr': chr,
    'cmp': cmp,
    'divmod': divmod,
    'isinstance': isinstance,
    'range': range,
    'xrange': xrange,
    'zip': zip,
    'Exception': Exception,
}

__all__ = ['mis_safe_eval']


def mis_safe_eval(expr, locals_dict):
    """ Evaluate an expression using safe_eval

    Returns the evaluated value or DataError.

    Raises NameError if the evaluation depends on a variable that is not
    present in local_dict.
    """
    try:
        c = test_expr(expr, _SAFE_OPCODES, mode='eval')
        globals_dict = {'__builtins__': _BUILTINS}
        # pylint: disable=eval-used,eval-referenced
        val = eval(c, globals_dict, locals_dict)
    except NameError:
        val = NameDataError('#NAME', traceback.format_exc())
    except ZeroDivisionError:
        # pylint: disable=redefined-variable-type
        val = DataError('#DIV/0', traceback.format_exc())
    except Exception:
        val = DataError('#ERR', traceback.format_exc())
    return val
