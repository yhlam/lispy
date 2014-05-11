from lispy.parser import List, Quotation, Number, Symbol


__all__ = ['evaluate', 'macro']


def evaluate(ast, vars_):
    evaluator = _evaluators[ast.__class__]
    return evaluator(ast, vars_)


def macro(func):
    func._is_macro = True
    return func


def ismacro(func):
    return getattr(func, '_is_macro', False)


def _eval_number(number, vars_):
    return number.value


def _eval_symbol(symbol, vars_):
    return vars_[symbol.identifier]


def _eval_quotation(quotation, vars_):
    return quotation.expr


def _eval_list(list_, vars_):
    func, *args = list_.elements
    funcobj = evaluate(func, vars_)
    if ismacro(funcobj):
        return funcobj(vars_, args)
    else:
        argobjs = [evaluate(arg, vars_) for arg in args]
        return funcobj(argobjs)


_evaluators = {
    Number: _eval_number,
    Symbol: _eval_symbol,
    Quotation: _eval_quotation,
    List: _eval_list
}
