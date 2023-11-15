# Word Chain

A package to build word chains from a given list of words. 

[![Tests](https://github.com/shaunhegarty/wordchain/actions/workflows/test.yml/badge.svg)](https://github.com/shaunhegarty/wordchain/actions/workflows/test.yml)

## Installation
```
pip install python-wordchain
```

## Sample Usage
```python
from wordchain.wordchain import WordChainer

WORD_LIST = ["bird", "bind", "bord", "bond", "bend", "bing", "bong", "sing", "song"]

chainer = WordChainer(word_list=WORD_LIST)
chainer.get_chains('bird', 'song')

```
This yields:
```python
[('bird', 'bord', 'bond', 'bong', 'song'),
 ('bird', 'bind', 'bing', 'sing', 'song'),
 ('bird', 'bind', 'bond', 'bong', 'song'),
 ('bird', 'bind', 'bing', 'bong', 'song')]
```

## Testing
Running the test suite from repository root:
```
pytest -v tests/tests.py
```

Run tests using docker and tox:
```
docker run --rm $(docker build -q . -f Dockerfile.tox) tox
```
