import spacy

nlp = spacy.load("en_core_web_sm")

def get_wiki_query(sentence):
    doc = nlp(sentence)
    nouns = list(filter(lambda x: x.pos_=="NOUN" or x.pos_=="PROPN", doc))
    # Get the last noun token in the list, since it's likely to be the most specific
    if nouns:
        return nouns[-1].text
    else:
        # If no nouns found, return the entire sentence
        return sentence

if __name__ == '__main__':
    sentence = "What color is an apple?"
    print(get_wiki_query(sentence))
    sentence = "Where can I find the best cringe?"
    print(get_wiki_query(sentence))
    sentence = "Where can I find the best cringe?"
    print(get_wiki_query(sentence))