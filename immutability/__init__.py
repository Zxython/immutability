class immutable:
    supported_dunder_methods = ['__setitem__', '__getitem__', '__len__', '__iadd__', '__add__', '__abs__',
                                '__exit__', '__call__', '__floordiv__', '__neg__', '__rtruediv__', '__rmul__',
                                '__mul__', '__pow__', '__cmp__', '__sub__', '__aenter__', '__aexit__',
                                '__aiter__', '__and__', '__anext__', '__await__', '__bool__', '__ceil__',
                                '__delete__', '__delitem__', '__delslice__', '__divmod__', '__enter__',
                                '__eq__', '__float__', '__floor__', '__fspath__', '__ge__', '__get__',
                                '__getinitargs__', '__getnewargs__', '__getstate__', '__gt__', '__hex__',
                                '__iand__', '__idiv__', '__ifloordiv__', '__ilshift__', '__imatmul__', '__imod__',
                                '__missing__', '__imul__', '__index__', '__bytes__', '__iter__', '__repr__',
                                '__copy__', '__contains__', '__int__', '__oct__', '__pos__', '__long__',
                                '__next__', '__trunc__', '__invert__', '__complex__', '__reduce__', '__unicode__',
                                '__reversed__', '__le__', '__lt__', '__ior__', '__ipow__', '__irshift__', '__isub__',
                                '__itruediv__', '__ixor__', '__lshift__', '__matmul__', '__mod__', '__or__', '__ne__',
                                '__radd__', '__rand__', '__rdiv__', '__rdivmod__', '__rfloordiv__', '__rlshift__',
                                '__xor__', '__truediv__', '__setstate__', '__setslice__', '__set__', '__rxor__',
                                '__rsub__', '__rshift__', '__rrshift__', '__rpow__', '__round__', '__ror__',
                                '__rmod__', '__rmatmul__']

    def partial(self, func, /, *args, **keywords):
        def newfunc(*fargs, **fkeywords):
            newkeywords = {**keywords, **fkeywords}
            self.__change_scope()
            newargs = [self.scope[-1]]
            temp = func(*newargs, *fargs, **newkeywords)
            return temp

        newfunc.func = func
        newfunc.args = args
        newfunc.keywords = keywords
        return newfunc

    def __init__(self, __object):
        from copy import deepcopy
        self.deepcopy = deepcopy
        try:
            raise SyntaxError
        except SyntaxError as traceback:
            frame = traceback.__traceback__.tb_frame.f_back
            base = str(frame).split(' ')[-1][0:-1]
            if base == 'immutable':
                frame = frame.f_back
                base = str(frame).split(' ')[-1][0:-1]
            for key, val in frame.f_globals.items():
                if key not in globals().keys():
                    globals()[key] = val
                    if str(val)[0] == '<':
                        val_elements = (str(val).split('.'))
                        if len(val_elements) > 1:
                            val_elements = val_elements[-1].split("'")[0]
                            if val_elements != 'immutable':
                                globals()[val_elements] = val
        self.type = str(type(__object)).split("'")[1].split('.')[-1]
        self.scope = [__object]
        self.base = base
        for method in dir(__object):
            try:
                if method in self.supported_dunder_methods:
                    self.__dict__[method[0:-2]] = self.partial(eval(self.type + '.' + method))
                    continue
                self.__dict__[method] = self.partial(eval(self.type + '.' + method))
            except AttributeError:
                self.__dict__[method] = __object.__dict__[method]
                continue
        self.type = type(__object)

    def __change_scope(self):
        try:
            raise SyntaxError
        except SyntaxError as traceback:
            path = self.get_path(traceback.__traceback__.tb_frame.f_back)
            while path[0] == 'newfunc' or path[0] in self.supported_dunder_methods:
                path.pop(0)
        if path is None:
            raise NameError("variable is not defined")
        for _ in range(len(self.scope) - len(path)):
            self.scope.pop(-1)
        for _ in range(len(path) - len(self.scope)):
            temp = self.deepcopy(self.scope[-1])
            self.scope.append(self.scope[-1])
            self.scope[-1] = temp

    def get_path(self, frame):
        path = []
        while True:
            temp = frame.f_back
            if temp is None:
                del self
                return None
            frame = temp
            current_frame = str(frame).split(' ')[-1][0:-1]
            path.append(current_frame)
            if current_frame == self.base:
                break
        return path

    def __str__(self):
        self.__change_scope()
        return str(self.scope[-1])

    def __setitem__(self, key, value):
        self.__change_scope()
        self.__dict__['__setitem'](key, value)

    def __getitem__(self, key):
        self.__change_scope()
        return self.__dict__['__getitem'](key)

    def __len__(self):
        self.__change_scope()
        return self.__dict__['__len']()

    def __iadd__(self, other):
        self.__change_scope()
        return self.__dict__['__iadd'](other)

    def __add__(self, other):
        self.__change_scope()
        return self.__dict__['__add'](other)

    def __abs__(self):
        self.__change_scope()
        return self.__dict__['__abs']()

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.__change_scope()
        return self.__dict__['__exit'](exc_type, exc_val, exc_tb)

    def __call__(self, *args, **kwargs):
        self.__change_scope()
        return self.__dict__['__call'](args, kwargs)

    def __floordiv__(self, other):
        self.__change_scope()
        return self.__dict__['__floordiv'](other)

    def __neg__(self):
        self.__change_scope()
        return self.__dict__['__neg']()

    def __rtruediv__(self, other):
        self.__change_scope()
        return self.__dict__['__rtruediv'](other)

    def __rmul__(self, other):
        self.__change_scope()
        return self.__dict__['__rmul'](other)

    def __mul__(self, other):
        self.__change_scope()
        return self.__dict__['__mul'](other)

    def __pow__(self, power, modulo=None):
        self.__change_scope()
        return self.__dict__['__pow'](power, modulo)

    def __cmp__(self, other):
        self.__change_scope()
        return self.__dict__['__cmp'](other)

    def __sub__(self, other):
        self.__change_scope()
        return self.__dict__['__sub'](other)

    def __aenter__(self):
        self.__change_scope()
        return self.__dict__['__aenter']()

    def __aexit__(self, exc_type, exc_val, exc_tb):
        self.__change_scope()
        return self.__dict__['__aexit'](exc_type, exc_val, exc_tb)

    def __aiter__(self):
        self.__change_scope()
        return self.__dict__['__aiter']()

    def __and__(self, other):
        self.__change_scope()
        return self.__dict__['__and'](other)

    def __anext__(self):
        self.__change_scope()
        return self.__dict__['__anext']()

    def __await__(self):
        self.__change_scope()
        return self.__dict__['__await']()

    def __bool__(self):
        self.__change_scope()
        return self.__dict__['__bool']()

    def __ceil__(self):
        self.__change_scope()
        return self.__dict__['__ceil']()

    def __delete__(self, instance):
        self.__change_scope()
        return self.__dict__['__delete'](instance)

    def __delitem__(self, key):
        self.__change_scope()
        return self.__dict__['__delitem'](key)

    def __delslice__(self, i, j):
        self.__change_scope()
        return self.__dict__['__delslice'](i, j)

    def __divmod__(self, other):
        self.__change_scope()
        return self.__dict__['__divmod'](other)

    def __enter__(self):
        self.__change_scope()
        return self.__dict__['__enter']()

    def __eq__(self, other):
        self.__change_scope()
        return self.__dict__['__eq'](other)

    def __float__(self):
        self.__change_scope()
        return self.__dict__['__float']()

    def __floor__(self):
        self.__change_scope()
        return self.__dict__['__floor']()

    def __fspath__(self):
        self.__change_scope()
        return self.__dict__['__fspath']()

    def __ge__(self, other):
        self.__change_scope()
        return self.__dict__['__ge'](other)

    def __get__(self, instance, owner):
        self.__change_scope()
        return self.__dict__['__get'](instance, owner)

    def __getinitargs__(self):
        self.__change_scope()
        return self.__dict__['__getinitargs']()

    def __getnewargs__(self):
        self.__change_scope()
        return self.__dict__['__getnewargs']()

    def __getstate__(self):
        self.__change_scope()
        return self.__dict__['__getstate']()

    def __gt__(self, other):
        self.__change_scope()
        return self.__dict__['__gt'](other)

    def __hex__(self):
        self.__change_scope()
        return self.__dict__['__hex']()

    def __iand__(self, other):
        self.__change_scope()
        return self.__dict__['__iand'](other)

    def __idiv__(self, other):
        self.__change_scope()
        return self.__dict__['__idiv'](other)

    def __ifloordiv__(self, other):
        self.__change_scope()
        return self.__dict__['__ifloordiv'](other)

    def __ilshift__(self, other):
        self.__change_scope()
        return self.__dict__['__ilshift'](other)

    def __imatmul__(self, other):
        self.__change_scope()
        return self.__dict__['__imatmul'](other)

    def __imod__(self, other):
        self.__change_scope()
        return self.__dict__['__imod'](other)

    def __missing__(self, key):
        self.__change_scope()
        return self.__dict__['__missing'](key)

    def __imul__(self, other):
        self.__change_scope()
        return self.__dict__['__imul'](other)

    def __index__(self):
        self.__change_scope()
        return self.__dict__['__index']()

    def __bytes__(self):
        self.__change_scope()
        return self.__dict__['__bytes']()

    def __iter__(self):
        self.__change_scope()
        return self.__dict__['__iter']()

    def __repr__(self):
        self.__change_scope()
        return self.__dict__['__repr']()

    def __copy__(self):
        self.__change_scope()
        return self.__dict__['__copy']()

    def __contains__(self, item):
        self.__change_scope()
        return self.__dict__['__contains'](item)

    def __int__(self):
        self.__change_scope()
        return self.__dict__['__int']()

    def __oct__(self):
        self.__change_scope()
        return self.__dict__['__oct']()

    def __pos__(self):
        self.__change_scope()
        return self.__dict__['__pos']()

    def __long__(self):
        self.__change_scope()
        return self.__dict__['__long']()

    def __next__(self):
        self.__change_scope()
        return self.__dict__['__next']()

    def __trunc__(self):
        self.__change_scope()
        return self.__dict__['__trunc']()

    def __invert__(self):
        self.__change_scope()
        return self.__dict__['__invert']()

    def __complex__(self):
        self.__change_scope()
        return self.__dict__['__complex']()

    def __reduce__(self):
        self.__change_scope()
        return self.__dict__['__reduce']()

    def __unicode__(self):
        self.__change_scope()
        return self.__dict__['__unicode']()

    def __reversed__(self):
        self.__change_scope()
        return self.__dict__['__reversed']()

    def __le__(self, other):
        self.__change_scope()
        return self.__dict__['__le'](other)

    def __lt__(self, other):
        self.__change_scope()
        return self.__dict__['__lt'](other)

    def __ior__(self, other):
        self.__change_scope()
        return self.__dict__['__ior'](other)

    def __ipow__(self, other):
        self.__change_scope()
        return self.__dict__['__ipow'](other)

    def __irshift__(self, other):
        self.__change_scope()
        return self.__dict__['__irshift'](other)

    def __isub__(self, other):
        self.__change_scope()
        return self.__dict__['__isub'](other)

    def __itruediv__(self, other):
        self.__change_scope()
        return self.__dict__['__itruediv'](other)

    def __ixor__(self, other):
        self.__change_scope()
        return self.__dict__['__ixor'](other)

    def __lshift__(self, other):
        self.__change_scope()
        return self.__dict__['__lshift'](other)

    def __matmul__(self, other):
        self.__change_scope()
        return self.__dict__['__matmul'](other)

    def __mod__(self, other):
        self.__change_scope()
        return self.__dict__['__mod'](other)

    def __or__(self, other):
        self.__change_scope()
        return self.__dict__['__or'](other)

    def __ne__(self, other):
        self.__change_scope()
        return self.__dict__['__ne'](other)

    def __radd__(self, other):
        self.__change_scope()
        return self.__dict__['__radd'](other)

    def __rand__(self, other):
        self.__change_scope()
        return self.__dict__['__rand'](other)

    def __rdiv__(self, other):
        self.__change_scope()
        return self.__dict__['__rdiv'](other)

    def __rdivmod__(self, other):
        self.__change_scope()
        return self.__dict__['__rdivmod'](other)

    def __rfloordiv__(self, other):
        self.__change_scope()
        return self.__dict__['__rfloordiv'](other)

    def __rlshift__(self, other):
        self.__change_scope()
        return self.__dict__['__rlshift'](other)

    def __xor__(self, other):
        self.__change_scope()
        return self.__dict__['__xor'](other)

    def __truediv__(self, other):
        self.__change_scope()
        return self.__dict__['__truediv'](other)

    def __setstate__(self, state):
        self.__change_scope()
        return self.__dict__['__setstate'](state)

    def __setslice__(self, i, j, sequence):
        self.__change_scope()
        return self.__dict__['__setslice'](i, j, sequence)

    def __set__(self, instance, value):
        self.__change_scope()
        return self.__dict__['__set'](instance, value)

    def __rxor__(self, other):
        self.__change_scope()
        return self.__dict__['__rxor'](other)

    def __rsub__(self, other):
        self.__change_scope()
        return self.__dict__['__rsub'](other)

    def __rshift__(self, other):
        self.__change_scope()
        return self.__dict__['__rshift'](other)

    def __rrshift__(self, other):
        self.__change_scope()
        return self.__dict__['__rrshift'](other)

    def __rpow__(self, other):
        self.__change_scope()
        return self.__dict__['__rpow'](other)

    def __round__(self, n=None):
        self.__change_scope()
        return self.__dict__['__round'](n)

    def __ror__(self, other):
        self.__change_scope()
        return self.__dict__['__ror'](other)

    def __rmod__(self, other):
        self.__change_scope()
        return self.__dict__['__rmod'](other)

    def __rmatmul__(self, other):
        self.__change_scope()
        return self.__dict__['__rmatmul'](other)
