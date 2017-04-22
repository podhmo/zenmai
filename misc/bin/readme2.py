import subprocess
from indent import block


def main():
    print("")
    print("command line example")
    print("----------------------------------------")
    print("")

    print("main.yaml")
    with block("yaml"):
        with open("examples/readme2/main.yaml") as rf:
            for line in rf:
                print(line.rstrip())

    print("nums.yaml")
    with block("yaml"):
        with open("examples/readme2/nums.yaml") as rf:
            for line in rf:
                print(line.rstrip())

    print("filters.py")
    with block("python"):
        with open("examples/readme2/filters.py") as rf:
            for line in rf:
                print(line.rstrip())

    print("run.")

    with block("bash"):
        print("$ zenmai examples/readme2/main.yaml")

    print("output")
    with block("yaml"):
        cmd = "make -C examples/readme2"
        p = subprocess.run(cmd, shell=True, check=True, stdout=subprocess.PIPE)
        for line in p.stdout.decode("utf-8").split("\n"):
            print(line)


if __name__ == "__main__":
    main()
