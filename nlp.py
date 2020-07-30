import nltk
from nltk.tokenize import sent_tokenize, word_tokenize, PunktSentenceTokenizer #ML tokenizer
from nltk.corpus import stopwords, state_union
from nltk.stem import PorterStemmer

#ps = PorterStemmer()

#ex_text = "Starbucks announced Thursday that it would require all customers to wear facial coverings while visiting any of its 9,000 store locations across the United States. The rule will go into effect on July 15."

train_text = state_union.raw("2005-GWBush.txt")
sample_text = state_union.raw("2006-GWBush.txt")

custom_toke = PunktSentenceTokenizer(train_text)

tokenized = custom_toke.tokenize(sample_text)

def process_content():
    try: 
        for i in tokenized:
            words = nltk.word_tokenize(i)
            tagged = nltk.pos_tag(words)
            
            #Regular Expressions
            #Chunk an search for RB (adverbs), verb (vb) and proper noun 
            chunkGram = r"""Chunk: {<.*>+}
                                    }<VB.?|IN|DT>+{"""
            
            chunkParse = nltk.RegexpParser(chunkGram)
            chunked = chunkParse.parse(tagged)
            
            #chunked.draw()
            
    except Exception as e:
        print(str(e))

process_content()
#stop_words = set(stopwords.words("english"))

#words = word_tokenize(ex_text)

#filter_sentence = []

# for w in words:
# 	if w not in stop_words:
# 		w = ps.stem(w)
# 		filter_sentence.append(w)

# print(filter_sentence)
