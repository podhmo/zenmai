class Symbol(object):
    def __init__(self, name):
        self.name = name

    def __repr__(self):
        return "<S {!r}>".format(self.name)


missing = Symbol("missing")
