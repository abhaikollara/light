class Integer(int):
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return str(self.value)


class Boolean:
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return str(self.value).lower()


TRUE = Boolean(True)
FALSE = Boolean(False)


class String:
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return str(self.value)


class Returned:
    def __init__(self, obj):
        self.obj = obj

    def __str__(self):
        return f"Returned({str(self.obj)})"


class Function:
    def __init__(self, params, body, closure):
        self.params = params
        self.body = body
        self.closure = closure

    def __repr__(self):
        return f"{repr(self.params)}"
