class immutable:
    def partial(self, func, /, *args, **keywords):
        def newfunc(*fargs, **fkeywords):
            newkeywords = {**keywords, **fkeywords}
            self.__change_scope()
            try:
                newargs = [self.scope[-1]]
            except AttributeError:
                newargs = [self.value]
            temp = func(*newargs, *fargs, **newkeywords)
            self.value = newargs[0]
            return temp
        newfunc.func = func
        newfunc.args = args
        newfunc.keywords = keywords
        return newfunc

    def __init__(self, __object):
        from copy import deepcopy
        self.deepcopy = deepcopy
        self.value = __object
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
        self.type = str(type(__object)).split("'")[1].split('.')[-1]
        self.scope = [self.value]
        self.base = base
        for method in dir(__object):
            try:
                if method in ['__setitem__', '__getitem__', '__len__']:
                    self.__dict__[method[0:-2]] = self.partial(eval(self.type + '.' + method))
                    continue
                self.__dict__[method] = self.partial(eval(self.type + '.' + method))
            except AttributeError:
                self.__dict__[method] = __object.__dict__[method]
                continue
        self.type = type(__object)

    def __setitem__(self, key, value):
        self.__change_scope()
        self.__dict__['__setitem'](key, value)

    def __getitem__(self, key):
        self.__change_scope()
        return self.__dict__['__getitem'](key)

    def __len__(self):
        self.__change_scope()
        return self.__dict__['__len']()

    def __change_scope(self):
        try:
            raise SyntaxError
        except SyntaxError as traceback:
            path = self.get_path(traceback.__traceback__.tb_frame.f_back)
            while path[0] in ['newfunc', '__setitem__', '__len__', '__getitem__']:
                path.pop(0)
        if path is None:
            raise NameError("variable is not defined")
        for _ in range(len(self.scope) - len(path)):
            self.value = self.scope.pop(-1)
        for _ in range(len(path) - len(self.scope)):
            self.scope[-1] = self.deepcopy(self.value)
            self.scope.append(self.value)

    @classmethod
    def __hash(cls, value):
        string = str(value)
        values = []
        for letter in string:
            values.append(ord(letter))
        value = 0
        for i, val in enumerate(values):
            value += cls.BASE ** i * val
        return value

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
