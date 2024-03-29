from wikiglot import Wiktionary

wiki = Wiktionary("da")

lemmas = wiki.lemmatize("hunden")

glossary = []

for lemma in lemmas:
    glossary.append(wiki.lookup(lemma))
