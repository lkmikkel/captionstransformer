
try:
    import unittest2 as unittest
except ImportError:
    import unittest
from StringIO import StringIO
from captionstransformer.rt import Reader, Writer
from captionstransformer import core
from datetime import timedelta

class TestRTReader(unittest.TestCase):
    def setUp(self):
        test_content = StringIO(u"""<window bgcolor="black" duration="00:00:10.000" wordwrap="true" width="352">
<font face="Verdana" size="4" color="#FFFFFF">
<center>

<time begin="00:00:00.166" whatever="couldntcareless"><clear/>
Some text

<time begin="00:00:00.766"><clear/>
Moar text

<time begin="00:00:02.033"><clear/>
Text<br>
Text<br>

<time begin="00:00:04.766"><clear/>
In physics, we explore the<br>
very small to the very large.<br>
""")
        self.reader = Reader(test_content)

    def test_read(self):
        captions = self.reader.read()
        self.assertTrue(captions is not None)
        self.assertEqual(len(captions), 4)
        first = captions[0]
        self.assertEqual(type(first.text), unicode)
        self.assertEqual(first.text, u"Some text")
        self.assertEqual(first.start, core.get_date(second=0, millisecond=166))
        self.assertEqual(first.end, core.get_date(second=0, millisecond=766))

        fourth = captions[3]
        self.assertEqual(fourth.end, core.get_date(second=10, millisecond=0))

if __name__ == '__main__':
    unittest.main()
