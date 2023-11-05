import nltk
import sys

TERMINALS = """
Adj -> "country" | "dreadful" | "enigmatical" | "little" | "moist" | "red"
Adv -> "down" | "here" | "never"
Conj -> "and" | "until"
Det -> "a" | "an" | "his" | "my" | "the"
N -> "armchair" | "companion" | "day" | "door" | "hand" | "he" | "himself"
N -> "holmes" | "home" | "i" | "mess" | "paint" | "palm" | "pipe" | "she"
N -> "smile" | "thursday" | "walk" | "we" | "word"
P -> "at" | "before" | "in" | "of" | "on" | "to"
V -> "arrived" | "came" | "chuckled" | "had" | "lit" | "said" | "sat"
V -> "smiled" | "tell" | "were"
"""
# 
NONTERMINALS = """
S -> NV | NV NP | NV NP P NP | NV P DAN Conj NP V | Det NV DAN | NV P NP | NP Adv V NP Conj NV P NP Adv
S -> NP V Adv Conj V NP | NP V DAN P NP Conj V NP P Det AAA NP | NP V Det AAA NP P NP P NP 
NV -> NP V
DN -> Det NP
DAN -> Det Adj | Det Adj NP
AAA -> Adj | Adj Adj | Adj Adj Adj
NVDN -> NP V D NP
NP -> N | Det N
"""
#SIMPLIFICAR
grammar = nltk.CFG.fromstring(NONTERMINALS + TERMINALS)
parser = nltk.ChartParser(grammar)


def main():

    # If filename specified, read sentence from file
    if len(sys.argv) == 2:
        with open(sys.argv[1]) as f:
            s = f.read()

    # Otherwise, get sentence as input
    else:
        s = input("Sentence: ")

    # Convert input into list of words
    s = preprocess(s)

    # Attempt to parse sentence
    try:
        trees = list(parser.parse(s))
    except ValueError as e:
        print(e)
        return
    if not trees:
        print("Could not parse sentence.")
        return

    # Print each tree with noun phrase chunks
    for tree in trees:
        tree.pretty_print()

        print("Noun Phrases Chunks:")
        for np in np_chunk(tree):
            print(" ".join(np.leaves()))


def preprocess(sentence):
    words = nltk.word_tokenize(sentence.lower())
    words = [word for word in words if any(char.isalpha() for char in word)]
    return words

def np_chunk(tree):
    np_chunks = []

    for subtree in tree.subtrees(lambda t: t.label() in ["NP"]):
        contains_np = any((subtree.label() == "NP" or subtree.label() == "N")  for subtree in subtree.subtrees())

        if contains_np:
            np_chunks.append(subtree)

    noun_phrases = []
    for np_chunk in np_chunks:
        noun_phrases.append(np_chunk)

    return noun_phrases



if __name__ == "__main__":
    main()
