import string
import unidecode
from nltk.corpus import stopwords

OTHER_STOPWORDS = ['plus', 'a', ' ', '', '<<', '>>', '«', '»', 'fait',
                   "dun", "dune", 'selon', 'entre', 'ans', 'sest', 'quil', 'sans', 'dont']

STOPWORDS_EN = ['hours', 'minute', 'new', 'said', 'sent', 'one', 'made', 'amid']


def text_cleaning(text, lang):
    # Remove punctuations
    words = text.split()
    table = str.maketrans('', '', string.punctuation)
    words = [w.translate(table) for w in words]

    # Put every words lowercase
    words = [w.lower() for w in words]

    for i, w in enumerate(words):
        # Remove accents
        words[i] = unidecode.unidecode(w)
        # Remove numbers
        try:
            int(w)
        except ValueError:
            pass
        else:
            words.remove(w)

    # for w in words:
    #     # Remove words too long
    #     if len(w) >= 20:
    #         words.remove(w)
    #
    #     # Remove youtube stuff
    #     elif 'ampvideoyou' in w:
    #         words.remove(w)
    #
    #     elif re.search('.+bordershare.+', w):
    #         print(w)
    #         words.remove(w)

    # Remove words from lists
    stopwords_list = stopwords.words(lang) + OTHER_STOPWORDS + STOPWORDS_EN
    words = [w for w in words if w not in stopwords_list]

    return words

