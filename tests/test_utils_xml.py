import os
import sys


sys.path.insert(1, os.path.join(sys.path[0], ".."))
from rich import traceback
from travers import xmler

traceback.install()


T = """<mydocument has="an attribute">
  <and>
    <many>elements</many>
    <many>more elements</many>
  </and>
  <plus a="complex">
    element as well
  </plus>
</mydocument>"""


def test_xml_parse():
    doc = xmler.parse(T)
    assert doc["mydocument"]["@has"] == "an attribute"
    assert doc["mydocument"]["and"]["many"] == ["elements", "more elements"]
    assert doc["mydocument"]["plus"]["@a"] == "complex"
    assert doc["mydocument"]["plus"]["#text"] == "element as well"


if __name__ == "__main__":
    test_xml_parse()
