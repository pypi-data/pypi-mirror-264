# wikiglot

```{toctree}
:maxdepth: 2
:hidden:
:caption: Contents

Home<self>
api
changelog
```

Welcome to the documentation for **wikiglot**! This project is a Python library for parsing Wiktionary pages. It is designed to be fast, flexible, and easy to use.

## Installing

**wikiglot** can be installed from source via pip:

```sh
pip install git+https://github.com/jolars/wikiglot
```

## Usage

Using **wikiglot** is simple. Here's an example of how to parse the entry from the Swedish Wiktionary page for "katt" (cat):

```python
from wikiglot import Wiktionary

parser = Wiktionary("sv")
parser.lookup("katt")
```

You can also parse entries for words in other languages that are available on the Swedish Wiktionary page, like so:

```python
parser.lookup("funicular", "en")
```
