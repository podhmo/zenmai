from dictknife import loading
import zenmai


class Driver:
    def __init__(self, module, srcfile, format=None):
        self.module = module
        self.srcfile = srcfile
        self.format = format

    def transform(self, d):
        return zenmai.compile(d, self.module, here=self.srcfile)

    def load(self, fp):
        return loading.load(fp)

    def dump(self, d, fp):
        return loading.dump(d, fp, format=self.format)

    def run(self, inp, outp):
        loading.setup()
        data = self.load(inp)
        result = self.transform(data)
        self.dump(result, outp)
