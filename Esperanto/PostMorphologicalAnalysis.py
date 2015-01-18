# -*- coding: utf-8 -*-
''' Модуль выполняет расширенный морфологический разбор слова,
    то есть на основе связей в предложении.
    По завершению удаляются все служебные части речи.
    Можно приступать к синтаксичекому анализу предложения.

    В текущие результаты добавляются новые ключи:
      'feature' - особенность, характеристика слова,
                то есть то, что выделяет его из общей группы, делает более частным.
                Другими словами, сюда прячутся прилагательные и притяжательные местоимения, наречия.
    '''

def pr(sentence):
  import BeautySafe as BS
  list_res = sentence.getSentence('dict')
  #sentence = 'montru miajn kursojn de rusia dolaro'
  BS.FWrite('----'+BS.getTime()+'\n')

  sentence = ''
  for k, v in list_res.items():
    sentence += v['word'] + ' '
  BS.FWrite('    '+sentence+'\n\n')

  BS.safeResults(list_res, 'PostMorphA')
  print 'Ready! :)'

def processingPreposition(index, # индекс предлога
                          sentence):
  # меняем падеж следующего существительного за предлогом, согласно предлогу
  if sentence.GetSet(index+1, 'POSpeech') == 'noun':
    sentence.GetSet(index+1, 'case', sentence.GetSet(index, 'give_case')) # меняем падеж существительного
    index += 1
  else:
    pass # здесь ошибка, так как после предлога может следовать лишь существительное

  # здесь устанавливаем связи
  
  return index

def _getPostMorphA(index, sentence):
  ''' Расширяет морфологический анализ '''
  GN = []

  #if sentence.GetSet(index, 'link') != []: return index

  # обработка существительного перед глаголом
  if sentence.GetSet(index, 'POSpeech') == 'verb':
    pass
  # обработка двух существительных вокруг предлога
  elif sentence.GetSet(index, 'POSpeech') == 'preposition':
    index = processingPreposition(index, sentence)

  return index, GN

def getPostMorphA(sentence):
  ''' Обёртка '''
  GrammarNazi = []

  # Прячем признак действия и признак признака (нарчия или прилагательного)
  # Они станут характеристикой глагола или прилагательного, наречия.
  # Эта процедура выполняется только перед пряткой прилагательных
  # В Эсперанто это облегчается тем, что у всех наречий одинаковое окончание.

  #TASK обстоятельства, выраженные существительным, обозначить как наречие
  index = 0
  while index < sentence.getLen():
    word = sentence.GetSet(index)

    if word['POSpeech'] == 'adverb':
      if word['base'] == u'ankaŭ': # стоит перед словом, к которому относится
        if index+1 < sentence.getLen():
          sentence.addFeature(index+1, index)
          continue
        else:
          GrammarNazi.append([4, u'Нарече \'%s\' ставится перед словом, к которому относится!' % word['word']])
          sentence.delByIndex(index) # просто игнорируем это наречие
          continue
      if index+1 < sentence.getLen():
        if sentence.GetSet(index+1, 'POSpeech') in ['verb', 'adjective', 'adverb']:
          sentence.addFeature(index+1, index)
          continue
        else: pass
        #ERROR решить вопрос с наречием et une, которое здесь как une.
      index2 = 0 # "свободноплавающее" нарчие. Добавим его к глаголу.
      while index2 < sentence.getLen():
        if sentence.GetSet(index2, 'POSpeech') == 'verb':
          sentence.addFeature(index2, index) #EX_ERROR если последний  index2, то возникает интересная ошибка.
          break
        index2 += 1
    else:
      index += 1
  
  # прячем признак предмета: прилагательные и притяжательные местоимения -
  # они станут характеристикой существительного,
  # что облегчит дальнейший анализ (избавит от "спотыканий" об эти части речи)
  index = 0
  while index < sentence.getLen():
    word = sentence.GetSet(index)
    
    if word['POSpeech'] == 'adjective':
      del word['case'], word['number'] # отсутствует проверка соответствия на падеж и число
    elif word['POSpeech'] == 'pronoun':
      if word['category'] == 'possessive':
        del word['number'] # res['case'], res['category'] тоже можно было бы удалить, но оно понадобится в синтаксическом разборе
      else:
        index += 1
        continue
    elif word['POSpeech'] == 'conjunction':
      index += 1
      pass
    else:
      index += 1
      continue

    if sentence.GetSet(index+1, 'POSpeech') == 'noun':
      sentence.addFeature(index+1, index)
      index -= 1
    elif sentence.GetSet(index+1, 'POSpeech') == 'conjunction':
      pass # союз, а за ним - второе прилагательное (притяжательное местоимение)
    else: pass # здесь ошибка, так как за прилагательным должно следовать существительное
    index += 1

  # выполняем основную задачу модуля - промежуточный анализ
  index = 0
  while index < sentence.getLen():
    index, GN = _getPostMorphA(index, sentence)
    GrammarNazi.extend(GN)
    index += 1

  # удаляем служебные части речи
  sentence.delByCharacteristic('POSpeech', 'preposition')
  pr(sentence)
  return sentence, GrammarNazi

if __name__ == '__main__':
  from MorphologicalAnalysis import getMorphA
  import BeautySafe as BS
  
  #sentence = 'montru miajn kursojn de rusia dolaro'
  sentence = ''
  BS.FWrite('----'+BS.getTime()+'\n')

  list_res = getMorphA(sentence)
  BS.safeResults(list_res, 'MorphA')
  BS.safeUnknown(list_res)
  tree = getPostMorphA(list_res)

  BS.FWrite('\n    '+sentence+'\n')
  sentence = ''
  for k, v in tree.items():
    sentence += v['word'] + ' '
  BS.FWrite('    '+sentence+'\n\n')

  BS.safeResults(tree, 'PostMorphA')
  print 'Ready! :)'
