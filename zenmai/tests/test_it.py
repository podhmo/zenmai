import unittest
import difflib
import textwrap
from dictknife import loading
loading.setup()  # xxx


class DiffTestCase(unittest.TestCase):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.addTypeEqualityFunc(str, 'assertDiff')

    def assertDiff(self, first, second, msg=None):
        self.assertIsInstance(first, str, 'First argument is not a string')
        self.assertIsInstance(second, str, 'Second argument is not a string')

        msg = msg or "{} != {}".format(repr(first)[:40], repr(second)[:40])

        if first != second:
            # don't use difflib if the strings are too long
            if (len(first) > self._diffThreshold or len(second) > self._diffThreshold):
                self._baseAssertEqual(first, second, msg)

            firstlines = first.splitlines(keepends=True)
            secondlines = second.splitlines(keepends=True)
            if not firstlines[-1].endswith("\n"):
                firstlines[-1] = firstlines[-1] + "\n"
            if not secondlines[-1].endswith("\n"):
                secondlines[-1] = secondlines[-1] + "\n"
            diff = '\n' + ''.join(difflib.unified_diff(firstlines, secondlines, fromfile="first", tofile="second"))
            raise self.fail(self._formatMessage(diff, msg))


class Tests(DiffTestCase):
    def _callFUT(self, source, m):
        from zenmai import compile
        d = loading.loads(source)
        return compile(d, m)

    def test_return_value_with_action(self):
        class m:
            @staticmethod
            def inc(n):
                return n + 1

            @staticmethod
            def inc2(n):
                return {"$inc": n + 1}

        source = textwrap.dedent("""
        n:
          $inc2: 10
        """)

        d = self._callFUT(source, m)
        actual = loading.dumps(d)
        expected = textwrap.dedent("""
        n: 12
        """)
        self.assertDiff(actual.strip(), expected.strip())


class ActionsTests(DiffTestCase):
    def _callFUT(self, source, m, filename=None):
        from zenmai import compile
        d = loading.loads(source)
        return compile(d, m, filename=filename)

    def test_import(self):
        class m:
            from zenmai.actions import import_  # NOQA

        source = textwrap.dedent("""
        main:
          $import: zenmai.actions.suffix
          as: s

        definitions:
          $s.suffix:
            name: foo
          suffix: +
        """)

        d = self._callFUT(source, m)
        actual = loading.dumps(d)
        expected = textwrap.dedent("""
        definitions:
          name+: foo
        """)
        self.assertDiff(actual.strip(), expected.strip())

    def test_import_with_physical_path(self):
        class m:
            from zenmai.actions import import_  # NOQA

        source = textwrap.dedent("""
        main:
          {$import: ./_inc.py, as: f}

        n: {$f.inc: 10}
        """)
        d = self._callFUT(source, m, filename=__file__)
        actual = loading.dumps(d)
        expected = textwrap.dedent("""
        n: 11
        """)
        self.assertDiff(actual.strip(), expected.strip())

    def test_from(self):
        class m:
            from zenmai.actions import from_  # NOQA

        source = textwrap.dedent("""
        main:
          - $from: zenmai.actions.suffix
            import: suffix

        definitions:
          $suffix:
            name: foo
          suffix: +
        """)

        d = self._callFUT(source, m)
        actual = loading.dumps(d)
        expected = textwrap.dedent("""
        definitions:
          name+: foo
        """)
        self.assertDiff(actual.strip(), expected.strip())

    def test_from_with_physical_path(self):
        class m:
            from zenmai.actions import from_  # NOQA

        source = textwrap.dedent("""
        main:
          {$from: ./_inc.py, import: inc}

        n: {$inc: 10}
        """)
        d = self._callFUT(source, m, filename=__file__)
        actual = loading.dumps(d)
        expected = textwrap.dedent("""
        n: 11
        """)
        self.assertDiff(actual.strip(), expected.strip())

    def test_concat(self):
        class m:
            from zenmai.actions import concat  # NOQA

        source = textwrap.dedent("""
        person:
          $concat:
            - name: foo
            - age: 10
        """)

        d = self._callFUT(source, m)
        actual = loading.dumps(d)
        expected = textwrap.dedent("""
        person:
          name: foo
          age: 10
        """)
        self.assertDiff(actual.strip(), expected.strip())

    def test_load(self):
        from tempfile import TemporaryDirectory
        from pathlib import Path

        with TemporaryDirectory() as d:
            d = Path(d)

            main = textwrap.dedent("""
            definitions:
              one:
                $load: "./one/one.yaml"
              two:
                $load: "./two/two.yaml"
            """)
            loading.dumpfile(loading.loads(main), str(d.joinpath("./main.yaml")))

            one = textwrap.dedent("""
            type: object
            properties:
              value:
                $load: "./value.yaml"
            """)
            loading.dumpfile(loading.loads(one), str(d.joinpath("./one/one.yaml")))

            value = textwrap.dedent("""
            description: value
            type: integer
            """)
            loading.dumpfile(loading.loads(value), str(d.joinpath("./one/value.yaml")))

            two = textwrap.dedent("""
            type: object
            properties:
              value:
                $load: "../one/value.yaml"
            """)
            loading.dumpfile(loading.loads(two), str(d.joinpath("./two/two.yaml")))

            class m:
                from zenmai.actions import load  # NOQA

            d = self._callFUT(main, m, filename=str(d.joinpath("./main.yaml")))
            actual = loading.dumps(d)
            expected = textwrap.dedent("""
            definitions:
              one:
                type: object
                properties:
                  value:
                    description: value
                    type: integer
              two:
                type: object
                properties:
                  value:
                    description: value
                    type: integer
            """)
            self.assertDiff(actual.strip(), expected.strip())
