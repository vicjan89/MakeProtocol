import sys

from yaml import load
from textengines.ReStructuredText import ReStructuredText

from Pris import Pris

path = sys.argv[1]

try:
    from yaml import CLoader as Loader, CDumper as Dumper
except ImportError:
    from yaml import Loader, Dumper

with open(path, 'r', encoding='utf-8') as stream:
    data = load(stream, Loader=Loader)

rst = ReStructuredText(path=path.split('.')[0]+'.rst', static='_static')

pris = Pris(**data)
pris.add_context(te=rst, contacts=pris.contacts)
pris.get_protocol()
rst.save()