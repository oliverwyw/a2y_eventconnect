import os
import sys
import re
from porterstemmer import PorterStemmer

# source: https://en.wikipedia.org/wiki/Wikipedia%3aList_of_English_contractions
contractions = {
"a'ight ": "alright",
"ain't ": "am not",
"amn't": "am not",
"arencha ": "are not you",
"aren't": "are not",
"'bout ": "about",
"can't": "cannot",
"cap'n ": "captain",
"cause ": "because",
"'cept ": "except",
"could've": "could have",
"couldn't": "could not",
"couldn't've": "could not have",
"cuppa": "cup of",
"dammit ": "damn it",
"daren't": "dare not",
"daresn't": "dare not",
"dasn't": "dare not",
"didn't": "did not",
"doesn't": "does not",
"don't": "do not",
"dunno ": "do not know",
"d'ye ": "do you",
"e'en ": "even",
"e'er ": "ever",
"em ": "them",
"everybody's": "everybody is",
"everyone's": "everyone is",
"fo'c'sle ": "forecastle",
"'gainst ": "against",
"g'day ": "good day",
"gimme ": "give me",
"giv'n ": "given",
"gi'z ": "give us",
"gonna ": "going to",
"gon't ": "go not",
"gotta ": "got to",
"hadn't": "had not",
"had've": "had have",
"hasn't": "has not",
"haven't": "have not",
"he'd": "he had",
"he'll": " he will",
"helluva ": "hell of a",
"he's": "he is",
"here's": "here is",
"how'd ": "how did",
"howdy ": "how do you do",
"how'll": "how will",
"how're": "how are",
"how's": "how is",
"i'd": "i would",
"i'd've": "i would have",
"i'd'nt": "i would not",
"i'd'nt've": "i would not have",
"i'll": "i will",
"i'm": "i am",
"imma ": "i am going to",
"i'm'o ": "i am going to",
"innit ": "isn't it",
"ion ": "i do not",
"i've": "i have",
"isn't": "is not",
"it'd": "it would",
"it'll": "it will",
"it's": "it is",
"idunno ": "i do not know",
"kinda ": "kind of",
"let's": "let us",
"ma'am ": "madam",
"mayn't": "may not",
"may've": "may have",
"methinks ": "i think",
"mightn't": "might not",
"might've": "might have",
"mustn't": "must not",
"mustn't've": "must not have",
"must've": "must have",
"'neath ": "beneath",
"needn't": "need not",
"nal ": "and all",
"ne'er ": "never",
"o'clock": "of the clock",
"o'er": "over",
"ol'": "old",
"oughtn't": "ought not",
"'round": "around",
"shalln't": "shall not",
"shan't": "shall not",
"she'd": "she had",
"she'll": "she will",
"she's": "she is",
"should've": "should have",
"shouldn't": "should not",
"shouldn't've ": "should not have",
"somebody's": "somebody is",
"someone's": "someone is",
"something's": "something is",
"so're ": "so are",
"so's ": "so is",
"so've ": "so have",
"that'll": "that will",
"that're ": "that are",
"that's": "that is",
"that'd": "that had",
"there'd": "there had",
"there'll": "there will",
"there're": "there are",
"there's": "there is",
"these're": "these are",
"these've": "these have",
"they'd": "they would",
"they'll": "they will",
"they're": "they are",
"they've": "they have",
"this's": "this is",
"those're ": "those are",
"those've ": "those have",
"thout ": "without",
"'til ": "until",
"tis ": "it is",
"to've ": "to have",
"twas ": "it was",
"tween ": "between",
"twere ": "it were",
"wanna": "want to",
"wasn't": "was not",
"we'd": "we would",
"we'd've": "we would have",
"we'll": "we will",
"we're": "we are",
"we've": "we have",
"weren't": "were not",
"whatcha": "what are you",
"what'd": "what did",
"what'll": "what will",
"what're": "what are",
"what's": "what is",
"what've": "what have",
"when's": "when is",
"where'd": "where did",
"where'll": "where will",
"where're": "where are",
"where's": "where is",
"where've": "where have",
"which'd": "which had",
"which'll": "which will",
"which're": "which are",
"which's": "which is",
"which've": "which have",
"who'd": "who would",
"who'd've": "who would have",
"who'll": "who will",
"who're": "who are",
"who's": "who is",
"who've": "who have",
"why'd": "why did",
"why're": "why are",
"why's": "why is",
"willn't": "will not",
"won't": "will not",
"wonnot": "will not",
"would've": "would have",
"wouldn't": "would not",
"wouldn't've": "would not have",
"y'all": "you all",
"y'all'd've": "you all would have ",
"y'all'd'n't've": "you all would not have ",
"y'all're": "you all are ",
"y'all'ren't": "you all are not ",
"y'at ": "you at",
"yes'm": "yes madam",
"yessir": "yes sir",
"you'd": "you had / you would",
"you'll": "you will",
"you're": "you are",
"you've": "you have",
"when'd": "when did",
"willn't": "will not",
}



def removeSGML(text):
    """
    Removes SGML tags from text
    param: text - text to remove SGML tags from
    return: text without SGML tags
    """
    return re.sub(r'<.*?>', '', text)



def tokenizeText(text):
    """
    Tokenizes text into words
    param: text - text to tokenize
    return: list of words
    """
    out = []
    word_list = text.strip().split()
    for word in word_list:
        curr_word = word.lower()

        # remove common punctuations from end of word
        if curr_word[-1] == '.' or curr_word[-1] == ',' \
            or curr_word[-1] == '!' or curr_word[-1] == '?': 
            curr_word = curr_word[:-1]
        
        # tokenize '
        if "'" in curr_word:
            if curr_word in contractions:
                curr_word = contractions[curr_word]
            elif curr_word[-2:] == "'s" or curr_word[-2:] == "s'":
                curr_word = curr_word[:-2] + " 's"
            elif curr_word[-2:] == "'d":
                curr_word = curr_word[:-2] + " would"
        
        w = curr_word.split()
        out.extend(w)

    # no need to tokenize dates like 2019-01-01 and 2019/01/01 since they are already kept together
    # no need to tokenize words like self-driving since they are already kept together
    # no need to tokenize numbers like 1,000,000 since they are already kept together

    return out



def removeStopwords(word_list):
    """
    Removes stopwords from text
    param: word_list - list of words to remove stopwords from
    return: list of words without stopwords
    """
    file = open('stopwords', 'r')
    raw_stopwords = file.read().splitlines()
    file.close()

    # remove whitespace from stopwords
    stopwords = []
    for word in raw_stopwords:
        new_word = word.strip()
        stopwords.append(new_word)

    out = []
    for word in word_list:
        if word not in stopwords:
            out.append(word)
    
    return out



def stemWords(word_list):
    """
    Stems words in text
    param: word_list - list of words to stem
    return: list of stemmed words
    """
    out = []
    for word in word_list:
        ps = PorterStemmer()
        stemmed_word = ps.stem(word, 0, len(word) - 1)
        out.append(stemmed_word)

    return out



def preprocessText(text):
    """
    Preprocesses text
    param: text - text to preprocess
    return: a list of preprocessed words 
    """
    text = removeSGML(text)
    word_list = tokenizeText(text)
    word_list = removeStopwords(word_list)
    word_list = stemWords(word_list)

    return word_list



def summarize(collection):
    """
    Summarizes collection
    param: collection - collection to summarize
    return: word_count - number of words in collection
            vocab_size - size of vocabulary
            freq50 - dict of 50 most frequent words with their frequencies
    """
    word_count = 0
    vocab = {}
    freq50 = []

    for doc in collection:
        word_count += len(collection[doc])
        for word in collection[doc]:
            if word in vocab:
                vocab[word] += 1
            else:
                vocab[word] = 1
    
    vocab_size = len(vocab.keys())
    freq50_key = sorted(vocab, key=vocab.get, reverse=True)[:50]
    for key in freq50_key:
        freq50.append((key, vocab[key]))

    num25 = word_count * 0.25
    count = 0
    unique = 0
    for word in sorted(vocab, key=vocab.get, reverse=True):
        if count < num25:
            count += vocab[word]
            unique += 1
        else:
            print("number of unique words acccounting for 25% of the collection: " + str(unique))
            break

    return word_count, vocab_size, freq50



if __name__ == "__main__":

    if len(sys.argv) == 2:
        folder = sys.argv[1]
        collection = dict()
        for filename in os.listdir(folder):
            file = open(os.path.join(folder, filename), 'r', encoding = 'iso-8859-1')
            text = file.read()
            file.close()
            collection[filename] = preprocessText(text)
        
        word_count, vocab_size, freq50 = summarize(collection)
        f = open("preprocess.output", 'w')
        f.write("Words "+ str(word_count) + '\n')
        f.write("Vocabulary " + str(vocab_size) + '\n')
        f.write("Top 50 words\n")

        for word in freq50:
            f.write(word[0] + " " + str(word[1]) + '\n')
        f.close()

    
    # this part is for write-up questions
    elif len(sys.argv) == 1:
        folder = 'cranfieldDocs/'
        dir_lst = os.listdir(folder)
        dir_lst.sort()

        # first subset
        collection1 = {}
        for fileidx in range(0, 443):
            filename = dir_lst[fileidx]
            file = open(os.path.join(folder, filename), 'r', encoding = 'iso-8859-1')
            text = file.read()
            file.close()
            collection1[filename] = preprocessText(text)
        word_count1, vocab_size1, _ = summarize(collection1)

        # second subset
        collection2 = {}
        for fileidx in range(700, 1400):
            filename = dir_lst[fileidx]
            file = open(os.path.join(folder, filename), 'r', encoding = 'iso-8859-1')
            text = file.read()
            file.close()
            collection2[filename] = preprocessText(text)
        word_count2, vocab_size2, _ = summarize(collection2)

        # print output
        print("Words in collection 1: " + str(word_count1))
        print("Vocabulary size of collection 1: " + str(vocab_size1))
        print("Words in collection 2: " + str(word_count2))
        print("Vocabulary size of collection 2: " + str(vocab_size2))


    else:
        print("Invalid number of arguments")