import sys
from io import StringIO
from zenmai.driver import Driver
from zenmai import actions


def loadfile(filename, data=None, driver_factory=Driver, module=actions):
    if filename is None:
        return load(sys.stdin, data=data, driver_factory=driver_factory, module=module)
    else:
        with open(filename) as rf:
            return load(
                rf, filename=filename, data=data, driver_factory=driver_factory, module=module
            )


def load(rf, filename=None, data=None, driver_factory=Driver, module=actions):
    filename = filename or getattr(rf, "name", None)
    driver = driver_factory(module, filename, data=data)
    return driver.transform(driver.load(rf))


def loads(s, filename=None, data=None, driver_factory=Driver, module=actions):
    return load(StringIO(), filename, data=data, driver_factory=driver_factory, module=module)
