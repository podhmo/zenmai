import sys
import argparse
import logging
from dictknife import loading
from zenmai.langhelpers import import_module, import_symbol


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("-m", "--module", default="zenmai.actions")
    parser.add_argument("--driver", default="zenmai.driver:Driver")
    parser.add_argument("--logging", default="INFO", choices=["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"])
    parser.add_argument("-f", "--format", default=None, choices=["yaml", "json"])
    parser.add_argument("--data", action="append")
    parser.add_argument("file", default=None)

    loading.setup()  # xxx:
    args = parser.parse_args()

    driver_cls = args.driver
    if ":" not in driver_cls:
        driver_cls = "swagger_marshmallow_codegen.driver:{}".format(driver_cls)

    module = import_module(args.module)
    data = [loading.loadfile(path) for path in args.data]
    driver = import_symbol(driver_cls)(module, args.file, format=args.format, data=data)

    # todo: option
    logging.basicConfig(
        format="%(levelname)5s:%(name)30s:%(message)s",
        level=logging._nameToLevel[args.logging]
    )
    if args.file is None:
        driver.run(sys.stdin, sys.stdout)
    else:
        with open(args.file) as rf:
            driver.run(rf, sys.stdout)
