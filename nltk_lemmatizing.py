from nltk.stem import WordNetLemmatizer

lemmatizer = WordNetLemmatizer()

#pos = part of speech 'a' = adverb, default = 'n' /noun
print(lemmatizer.lemmatize('better',pos ='a'))
print(lemmatizer.lemmatize('best',pos ='a'))
print(lemmatizer.lemmatize('run',pos ='a'))
