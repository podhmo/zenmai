import subprocess
from indent import block


def main():
    print("")
    print("code example")
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
        cmd = "make -C examples/readme"
        p = subprocess.run(cmd, shell=True, check=True, stdout=subprocess.PIPE)
        for line in p.stdout.decode("utf-8").split("\n"):
            print(line)


if __name__ == "__main__":
    main()
