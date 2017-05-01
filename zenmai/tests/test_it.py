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

    def test_counter(self):
        class m:
            from zenmai.actions import counter  # NOQA

        source = textwrap.dedent("""
        $let:
          c0: {$counter: 3}
          c1: {$counter: 0}
        body:
          - {$c0: "item{:04}"}
          - {$c1}
          - {$c0: "item{:04}"}
          - {$c1}
        """)

        d = self._callFUT(source, m)
        actual = loading.dumps(d)
        expected = textwrap.dedent("""
        - item0003
        - 0
        - item0004
        - 1
        """)
        self.assertDiff(actual.strip(), expected.strip())

    def test_get(self):
        class m:
            from zenmai.actions import get  # NOQA

        source = textwrap.dedent("""
        $let:
          person:
            name: foo
        body:
          - {$get: person}
          - {$get: "person#/name"}
          - {$get: "person#/age", default: 0}
        """)

        d = self._callFUT(source, m)
        actual = loading.dumps(d)
        expected = textwrap.dedent("""
        - name: foo
        - foo
        - 0
        """)
        self.assertDiff(actual.strip(), expected.strip())

    def test_format(self):
        class m:
            from zenmai.actions import format  # NOQA

        source = textwrap.dedent("""
        - $format: "{prefix}{number:04}"
          prefix: foo
          number: 0
        - $format: "{prefix}{number:04}"
          prefix: foo
          number: 1
        - $format: "{prefix}{number:04}"
          prefix: bar
          number: 0
        """)

        d = self._callFUT(source, m)
        actual = loading.dumps(d)
        expected = textwrap.dedent("""
        - foo0000
        - foo0001
        - bar0000
        """)
        self.assertDiff(actual.strip(), expected.strip())

    def test_format2(self):
        class m:
            from zenmai.actions import format  # NOQA
            from zenmai.actions import get  # NOQA

        source = textwrap.dedent("""
        $let:
          items:
            app: "{prefix}-app"
            batch: "{prefix}-batch"
        body:
          $format: {$get: items}
          prefix: dev
        """)

        d = self._callFUT(source, m)
        actual = loading.dumps(d)
        expected = textwrap.dedent("""
        app: dev-app
        batch: dev-batch
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

    def test_load__with_kwargs(self):
        from tempfile import TemporaryDirectory
        from pathlib import Path

        with TemporaryDirectory() as d:
            d = Path(d)

            a = textwrap.dedent("""
            b:
              $let:
                mydata: {value: 10}
              body:
                $load:  ./b.yaml
                data: {$get: mydata}
            """)
            loading.dumpfile(loading.loads(a), str(d.joinpath("./a.yaml")))

            b = textwrap.dedent("""
            # need: data
            name: b
            data: {$get: data}
            """)
            loading.dumpfile(loading.loads(b), str(d.joinpath("./b.yaml")))

            class m:
                from zenmai.actions import get  # NOQA
                from zenmai.actions import load  # NOQA

            d = self._callFUT(a, m, filename=str(d.joinpath("./a.yaml")))
            actual = loading.dumps(d)
            expected = textwrap.dedent("""
            b:
              name: b
              data:
                value: 10
            """)
            self.assertDiff(actual.strip(), expected.strip())

    def test_load__with_dynamicscope(self):
        from tempfile import TemporaryDirectory
        from pathlib import Path

        with TemporaryDirectory() as d:
            d = Path(d)

            a = textwrap.dedent("""
            b:
              $let:
                data: {value: 10}
              body:
                $load:  ./b.yaml
            """)
            loading.dumpfile(loading.loads(a), str(d.joinpath("./a.yaml")))

            b = textwrap.dedent("""
            # need: data
            name: b
            data: {$get: data}
            """)
            loading.dumpfile(loading.loads(b), str(d.joinpath("./b.yaml")))

            class m:
                from zenmai.actions import get  # NOQA
                from zenmai.actions import load_with_dynamicscope as load  # NOQA

            d = self._callFUT(a, m, filename=str(d.joinpath("./a.yaml")))
            actual = loading.dumps(d)
            expected = textwrap.dedent("""
            b:
              name: b
              data:
                value: 10
            """)
            self.assertDiff(actual.strip(), expected.strip())

    def test_jinja2(self):
        class m:
            from zenmai.actions import jinja2_template  # NOQA

        source = textwrap.dedent("""
        $let:
          item-template:
            $jinja2_template: |
              items:
                {% for i in nums %}
                - {{prefix|default("no")}}.{{i}}
                {% endfor %}
        body:
          listing:
            $item-template:
              nums: [1,2,3]
        """)

        d = self._callFUT(source, m)
        actual = loading.dumps(d)
        expected = textwrap.dedent("""
        listing:
          items:
          - no.1
          - no.2
          - no.3
        """)
        self.assertDiff(actual.strip(), expected.strip())

    def test_jinja2_raw_format(self):
        from tempfile import TemporaryDirectory
        from pathlib import Path

        class m:
            from zenmai.actions import jinja2_template  # NOQA
            from zenmai.actions import load  # NOQA

        with TemporaryDirectory() as d:
            d = Path(d)

            main = textwrap.dedent("""
            $let:
              readme-template:
                $jinja2_template:
                  $load: ./readme.jinja2
                  format: raw
                format: raw
            body:
              ./one.md:
                $readme-template:
                  name: one
              ./two.md:
                $readme-template:
                  name: two
              ./three.md:
                $readme-template:
                  name: three
            """)
            loading.dumpfile(loading.loads(main), str(d.joinpath("./main.yaml")))

            template = textwrap.dedent("""
            # {{name}}
            this is {{name}}.
            """)
            with open(str(d.joinpath("./readme.jinja2")), "w") as wf:
                wf.write(template)

            d = self._callFUT(main, m, filename=str(d.joinpath("./main.yaml")))
            actual = loading.dumps(d)
            expected = textwrap.dedent("""
            ./one.md: '

              # one

              this is one.'
            ./two.md: '

              # two

              this is two.'
            ./three.md: '

              # three

              this is three.'
            """)
            self.assertDiff(actual.strip(), expected.strip())

        source = textwrap.dedent("""
        $let:
          item-template:
            $jinja2_template: |
              items:
                {% for i in nums %}
                - {{prefix|default("no")}}.{{i}}
                {% endfor %}
        body:
          listing:
            $item-template:
              nums: [1,2,3]
        """)

        d = self._callFUT(source, m)
        actual = loading.dumps(d)
        expected = textwrap.dedent("""
        listing:
          items:
          - no.1
          - no.2
          - no.3
        """)
        self.assertDiff(actual.strip(), expected.strip())


class SpecialSyntaxTests(DiffTestCase):
    def _callFUT(self, source, m, filename=None):
        from zenmai import compile
        d = loading.loads(source)
        return compile(d, m, filename=filename)

    def test_quote_syntax(self):
        class m:
            pass

        source = textwrap.dedent("""
        body:
          $quote:
            $load:  foo.yaml
        """)

        d = self._callFUT(source, m)
        actual = loading.dumps(d)
        expected = textwrap.dedent("""
        body:
          $load: foo.yaml
        """)
        self.assertDiff(actual.strip(), expected.strip())

    def test_quote_syntax2(self):
        class m:
            pass

        source = textwrap.dedent("""
        body:
          $$load:  foo.yaml
        """)

        d = self._callFUT(source, m)
        actual = loading.dumps(d)
        expected = textwrap.dedent("""
        body:
          $load: foo.yaml
        """)
        self.assertDiff(actual.strip(), expected.strip())

    def test_when_syntax(self):
        class m:
            pass

        source = textwrap.dedent("""
        ok0:
          $when: true
          body: ok
        ng0:
          $when: false
          body: ng
        ok1:
          $when: true
          body:
            message: ok
        ok2:
          $when: true
          message: ok
        """)

        d = self._callFUT(source, m)
        actual = loading.dumps(d)
        expected = textwrap.dedent("""
        ok0: ok
        ok1:
          message: ok
        ok2:
          message: ok
        """)
        self.assertDiff(actual.strip(), expected.strip())

    def test_unless_syntax(self):
        class m:
            pass

        source = textwrap.dedent("""
        ok0:
          $unless: false
          body: ok
        ng0:
          $unless: true
          body: ng
        ok1:
          $unless: false
          body:
            message: ok
        ok2:
          $unless: false
          message: ok
        """)

        d = self._callFUT(source, m)
        actual = loading.dumps(d)
        expected = textwrap.dedent("""
        ok0: ok
        ok1:
          message: ok
        ok2:
          message: ok
        """)
        self.assertDiff(actual.strip(), expected.strip())

    def test_let_syntax(self):
        class m:
            from zenmai.actions import partial  # NOQA
            prefix = staticmethod(lambda d, prefix=":": prefix + d)

        source = textwrap.dedent("""
        $let:
          withPlus:
            {$partial: $prefix, prefix: +}
        body:
          definitions:
            name: {$withPlus: foo}
        """)

        d = self._callFUT(source, m)
        actual = loading.dumps(d)
        expected = textwrap.dedent("""
        definitions:
          name: +foo
        """)
        self.assertDiff(actual.strip(), expected.strip())

    def test_let_syntax_with_scope(self):
        class m:
            from zenmai.actions import partial  # NOQA
            prefix = staticmethod(lambda d, prefix=":": prefix + d)
            add = staticmethod(lambda n, v=1: n + v)

        source = textwrap.dedent("""
        $let:
          withPlus:
            {$partial: $prefix, prefix: +}
        person:
          name: {$withPlus: foo}
          age:
            $let:
              withPlus: {$partial: $add, v: 10}
            body:
              $withPlus: 10
        friends:
          - name: {$withPlus: bar}
        """)

        d = self._callFUT(source, m)
        actual = loading.dumps(d)
        expected = textwrap.dedent("""
        person:
          name: +foo
          age: 20
        friends:
        - name: +bar
        """)
        self.assertDiff(actual.strip(), expected.strip())
