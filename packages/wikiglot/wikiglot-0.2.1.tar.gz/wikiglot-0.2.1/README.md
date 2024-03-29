# wikiglot

[![CI](https://github.com/jolars/wikiglot/actions/workflows/ci.yml/badge.svg)](https://github.com/jolars/wikiglot/actions/workflows/ci.yml)
[![codecov](https://codecov.io/gh/jolars/wikiglot/graph/badge.svg?token=7SXl0HF8QV)](https://codecov.io/gh/jolars/wikiglot)

## Overview

**wikiglot** parses entries in Wiktionary pages. It is designed to be simple and flexible.

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

You can also parse entries for words in other languages that are available on the Swedish Wiktionary page:

```python
parser.lookup("funicular", "en")
```

## Limitations

**wikiglot** parses Wiktionary pages one-by-one, which can be slow if you need to look up a large number of words. If that is the case, you might prefer a solution that relies on a downloaded version of Wiktionary.

## Contributing

When writing commit messages, please use the [conventional commits format](https://www.conventionalcommits.org/en/v1.0.0/).

## Versioning

wikiglot uses [semantic versioning](https://semver.org).
