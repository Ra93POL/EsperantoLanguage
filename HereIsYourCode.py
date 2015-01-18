import LingvoObjects, Esperanto

def getAnalysis(NL):
  # подгатавливаем текст 
  list_sentence = LangModule.Prepearing(NL)
  # возвращаем предложения в виде объекта
  obj_sentence = LingvoObjects.Sentence(list_sentence)
  # делаем полный морфологический и синтаксический анализы
  result, GrammarNazi = LangModule.NL2ResultA(obj_sentence)
  return result.getSentence('dict')

#-----------------------------------------------------------------#

sentence = "montru dolaran kurson de gruzia banko"
#sentence = "montru dolaran kurson de gruzia banko malrapide"
#sentence = "Vi estas studento"

print getAnalysis()
