class immutable:
    def partial(self, func, /, *args, **keywords):
        def newfunc(*fargs, **fkeywords):
            newkeywords = {**keywords, **fkeywords}
            self.__change_scope()
            try:
                newargs = [self.value.copy()]
            except AttributeError:
                newargs = [self.value]
            temp = func(*newargs, *fargs, **newkeywords)
            self.value = newargs[0]
            return temp
        newfunc.func = func
        newfunc.args = args
        newfunc.keywords = keywords
        return newfunc

    def __init__(self, value):
        self.value = value
        self.type = str(type(value)).split("'")[1].split('.')[-1]
        try:
            raise SyntaxError
        except SyntaxError as traceback:
            frame = traceback.__traceback__.tb_frame.f_back
            base = str(frame).split(' ')[-1][0:-1]
            if base == 'immutable':
                frame = frame.f_back
                base = str(frame).split(' ')[-1][0:-1]
        self.scope = [self.value]
        self.base = base
        for method in dir(value):
            try:
                if method == '__setitem__':
                    self.__dict__['__setitem'] = self.partial(eval(self.type + '.' + method))
                    continue
                self.__dict__[method] = self.partial(eval(self.type + '.' + method))
            except AttributeError:
                self.__dict__[method] = value.__dict__[method]
                continue

    def __setitem__(self, key, value):
        self.__dict__['__setitem'](key, value)

    def __change_scope(self):
        try:
            raise SyntaxError
        except SyntaxError as traceback:
            path = self.get_path(traceback.__traceback__.tb_frame.f_back)
            while path[0] in ['newfunc', '__setitem__']:
                path.pop(0)
        if path is None:
            raise NameError("variable is not defined")
        for _ in range(len(self.scope) - len(path)):
            self.value = self.scope.pop(-1)
        for _ in range(len(path) - len(self.scope)):
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
        return str(self.value)
