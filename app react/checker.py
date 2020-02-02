import stanfordnlp
from googletrans import Translator
#from google.cloud import translate_v2 as translate
import jsons

class ReturnWord():
    def __init__(self):
        self.text = ""
        self.upos = ""
        self.xpos = ""
        self.case = ""
        self.gender = ""
        self.number = ""
        self.governor = ""
        self.relation = ""
        self.notes = []
        self.translation = ""
        self.other_translations = []
        
    def set_vars(self, text, upos, xpos, governor, relation):
        self.text = text
        self.upos = upos
        self.xpos = xpos
        self.governor = governor
        self.relation = relation

class Evaluate():
    def __init__(self):
        self.translator = Translator()
        self.nlp_de = stanfordnlp.Pipeline(lang='de')
        #self.nlp_en = stanfordnlp.Pipeline(lang='en')
        self.prep_akk = ['bis', 'durch', 'für', 'gegen', 'ohne', 'um']
        self.prep_dat = ['aus', 'ausser', 'bei', 'nach', 'mit', 'seit', 'von', 'zu']
        self.prep_acc_dat = ['an', 'auf', 'hinter', 'in', 'neben', 'über', 'unter', 'von', 'zwischen']

        self.nominative = { 'Masc': 'der', 'Fem': 'die', 'Neut': 'das' }
        self.accusative = { 'Masc': 'den', 'Fem': 'die', 'Neut': 'das' }
        self.dative = { 'Masc': 'dem', 'Fem': 'der', 'Neut': 'den' }
        self.genitive = { 'Masc': 'des', 'Fem': 'der', 'Neut': 'des' }

    def check(self, sentence):
        doc_de = self.nlp_de(sentence)
        sentences_ret = []

        for sentence in doc_de.sentences:
            words_ret = [ReturnWord() for _ in range(len(sentence.words))]
            for word in sentence.words:
                #print("[%d] Word: %s" % (int(word.index), word.text))
                eng = self.translator.translate(word.lemma, src='de', dest='en')
                #print(dir(words_ret[int(word.index) - 1].translations))
                #print(format(eng.extra_data))
                #print(format(eng.extra_data['all-translations']))
                words_ret[int(word.index) - 1].translation = eng.text
                if(eng.extra_data['all-translations'] is not None):
                    words_ret[int(word.index) - 1].other_translations.extend(eng.extra_data['all-translations'][0][1])
                words_ret[int(word.index) - 1].set_vars(word.text, word.upos, word.xpos, word.governor, word.dependency_relation)
                #print("%s, %s, %s, %s" % (words_ret[int(word.index) - 1].text, words_ret[int(word.index) - 1].upos, words_ret[int(word.index) - 1].xpos, words_ret[int(word.index) - 1].relation))
                if(word.upos == 'ADP'):
                    #print("%s is ADP" % word.text)
                    if(word.lemma in self.prep_akk):
                        #print("%s is accusative" % word.text)
                        words_ret[int(word.index) - 1].notes.append(word.text + " takes the accusative case.")
                        words_ret[word.governor - 1].notes.append("Because " + word.text + " is accusative, so is " + sentence.words[word.governor - 1].text)
                        words_ret[word.governor - 1].case = "Acc"
                    elif(word.lemma in self.prep_dat):
                        #print("%s is dative" % word.text)
                        words_ret[int(word.index) - 1].notes.append(word.text + " takes the dative case.")
                        words_ret[word.governor - 1].notes.append("Because " + word.text + " is dative, so is " + sentence.words[word.governor - 1].text)
                        words_ret[word.governor - 1].case = "Dat"
                    elif(word.lemma in self.prep_acc_dat):
                        #print("%s is akk/dat" % word.text)
                        words_ret[int(word.index) - 1].notes.append(word.text + " takes Dative if it answers the question 'where?'")
                        words_ret[int(word.index) - 1].notes.append(word.text + " takes the Accusative if it answers the question 'where to?'")
                        words_ret[word.governor - 1].notes.append(sentence.words[word.governor - 1].text + " takes either the Accusative or Dative case.")
                        words_ret[word.governor - 1].case = "Acc|Dat"
                if(word.upos == 'NOUN'):
                    words_ret[int(word.index) - 1].gender = (self.nlp_de(word.text).sentences[0].words[0].feats.split('|')[1].split('=')[1])
                    #print("%s, %s" % (words_ret[int(word.index) - 1].gender, word.text))
                
                feats = word.feats.split('|')
                for feat in feats:
                    pair = feat.split('=')
                    #print("%s: %s" % (word.text, pair))
                    if(pair[0] == "Gender" and words_ret[int(word.index) - 1].gender == ""): words_ret[int(word.index) - 1].gender = pair[1]
                    elif(pair[0] == "Number"): words_ret[int(word.index) - 1].number = pair[1]
                    elif(pair[0] == "Case" and words_ret[int(word.index) - 1].case == ""): words_ret[int(word.index) - 1].case = pair[1]
                    #if(len(pair) is 2): print("%s gender: %s (pair[1] is %s)" % (word.text, words_ret[int(word.index) - 1].gender, pair[1]))
                if(word.dependency_relation == 'obj' or word.dependency_relation == 'dobj'):
                    words_ret[int(word.index) - 1].notes.append(word.text + " is probably a direct object, which takes the accusative case.")
                    words_ret[int(word.index) - 1].case = "Acc"
                if(word.dependency_relation == 'iobj'):
                    words_ret[int(word.index) - 1].notes.append(word.text + " is probably an indirect object, which takes the dative case.")
                    words_ret[int(word.index) - 1].case = "Dat"
                    
            for word in sentence.words:
                #print("%s == 'ART' ? %s" % (word.xpos, (word.xpos == 'ART')))
                if(word.xpos == 'ART'):
                    #print(words_ret[word.governor - 1].case)
                    if('Acc' in words_ret[word.governor - 1].case):
                        #print("%s is Acc %s" % (str(words_ret[word.governor - 1].text), str(words_ret[word.governor - 1].case)))
                        nom = self.nominative[words_ret[word.governor - 1].gender]
                        article = self.accusative[words_ret[word.governor - 1].gender]
                        words_ret[int(word.index) - 1].notes.append("%s %s takes the accusative case, so the article should be %s" % (nom.capitalize(), words_ret[word.governor - 1].text, article))
                    if('Dat' in words_ret[word.governor - 1].case):
                        #print("%s is Dat %s" % (str(words_ret[word.governor - 1].text), str(words_ret[word.governor - 1].case)))
                        nom = self.nominative[words_ret[word.governor - 1].gender]
                        article = self.dative[words_ret[word.governor - 1].gender]
                        words_ret[int(word.index) - 1].notes.append("%s %s takes the dative case, so the article should be %s" % (nom.capitalize(), words_ret[word.governor - 1].text, article))
                    if('Gen' in words_ret[word.governor - 1].case):
                        #print("%s is Gen %s" % (str(words_ret[word.governor - 1].text), str(words_ret[word.governor - 1].case)))
                        nom = self.nominative[words_ret[word.governor - 1].gender]
                        article = self.genitive[words_ret[word.governor - 1].gender]
                        words_ret[int(word.index) - 1].notes.append("%s %s takes the genitive case, so the article should be %s" % (nom.capitalize(), words_ret[word.governor - 1].text, article))
        return jsons.dumps(words_ret)

#evaluator = Evaluate()
#sentence = "Ich kann nicht in die Schule gehen"
#print(evaluator.check(sentence))

# Needs api key
#translate_client = translate.Client()

#nlp_en = stanfordnlp.Pipeline(lang='en')

#english = translate_client.translate(sentence, target_language='en')['translatedText']

#doc_en = nlp_en(english)

#oc_en.sentences[0].print_dependencies()


#for ret in words_ret:
    #print("%s (%s)" % (ret.text, ret.translation))
 #   for note in ret.notes:
  #      print('\tNote: ' + note)
    #print('\tTranslations: ' + str(ret.other_translations))


