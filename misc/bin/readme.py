import sys
import contextlib
from io import StringIO
import subprocess


@contextlib.contextmanager
def indent(n):
    buf = StringIO()
    with contextlib.redirect_stdout(buf):
        yield buf
    buf.seek(0)

    prefix = " " * n
    write = sys.stdout.write
    for line in buf:
        write(prefix)
        write(line)
    sys.stdout.flush()


@contextlib.contextmanager
def block(code):
    print("")
    print(".. code-block:: {}".format(code))
    print("")
    with indent(2) as buf:
        yield buf
    print("")


def main():
    print("")
    print("example")
    print("----------------------------------------")
    print("")

    print("main.py")
    with block("python"):
        with open("examples/readme/main.py") as rf:
            for line in rf:
                print(line.rstrip())

    print("run.")

    with block("bash"):
        print("$ cat examples/readme/data.yaml > examples/readme/main.py")

    print("data.yaml")
    with block("yaml"):
        with open("examples/readme/data.yaml") as rf:
            for line in rf:
                print(line.rstrip())

    print("output")
    with block("yaml"):
        cmd = "cat examples/readme/data.yaml | python examples/readme/main.py"
        p = subprocess.run(cmd, shell=True, check=True, stdout=subprocess.PIPE)
        for line in p.stdout.decode("utf-8").split("\n"):
            print(line)


if __name__ == "__main__":
    main()
