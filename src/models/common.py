# ./src/models/common.py
from .deps import List, NewType
URL = NewType("URL", str)
URLs = List[URL]
