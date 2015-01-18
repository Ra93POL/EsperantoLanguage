# -*- coding: utf-8 -*-
''' Модуль выполняет синтаксический анализ предложения

  Определяются члены предложения и устанавливаются связи слов.

  Добавляются новые ключи:
    'link' - синтаксическая связь с другим словом. Значение:
    список порядковых номеров подчинённых (т. е. тех, кто к нему относится)
    #[{'index': INTEGER, 'type': 'parent/slave'}]
    'MOSentence' - член предложения
'''

def forPronounAndNoun(case):
  ''' Определяет член предложения для имени существительного
      и притяжательного местоимепния по падежу '''
  if case == 'accusative': return 'direct supplement'
  elif case == 'nominative': return 'object'
  else: return 'supplement'

def setMOS_ToSign(features):
  """ Определение члена предложения у признаков:
      прилагательного, наречия, """
  GN = []
  for feature in features:
    if feature['POSpeech'] == 'adjective':
      feature['MOSentence'] = 'definition'
      if len(feature['feature']) > 0:
        GN.extend(setMOS_ToSign(feature['feature']))

    elif feature['POSpeech'] == 'adverb':
      feature['MOSentence'] = 'circumstance'
      if len(feature['feature']) > 0:
        GN.extend(setMOS_ToSign(feature['feature']))
  return GN

def setMOSentence(index, sentence):
  GN = []
  word = sentence.GetSet(index)

  if word['POSpeech'] == 'verb':
    word['MOSentence'] = 'predicate'
    if len(word['feature']) > 0:
      GN.extend(setMOS_ToSign(word['feature']))

  #ATTENTION обстоятельства, выраженные существительным, определяются в модуле
  # промежуточного анализа как наречие.
  elif word['POSpeech'] == 'noun':
    word['MOSentence'] = forPronounAndNoun(word['case'])
    if len(word['feature']) > 0:
      GN.extend(setMOS_ToSign(word['feature']))

  elif word['POSpeech'] == 'pronoun':
    if word['category'] == 'possessive':
      word['MOSentence'] = 'definition'    # ? Появилось определение
    elif word['category'] == 'personal':
      word['MOSentence'] = forPronounAndNoun(res['case'])
    else: word['MOSentence'] = '' # не притяжательное и не личное местоимение

  else: word['MOSentence'] = ''

  return index, GN

def setLinks(index, sentence):
  ''' Устанавливает связи членов предложения. Обстоятельства и определения
      спрятаны в тех, к кому они относятся. Работаем лишь со сказуемым,
      подлежащим и дополнением. '''
  GN = []
  word = sentence.GetSet(index)

  # после if следуют те, для кого мы устанавливаем связи (ищем slave)
  if word['MOSentence'] == 'predicate':
    # ищем прямое дополнение
    index2 = index+1
    while index2 < sentence.getLen():
      if sentence.GetSet(index2, 'MOSentence') == 'direct supplement':
        word['link'].append(index2)
        break
      index2 += 1

  #TASK если у прямого дополнения нескеолько дполнений, то они проигнорируются
  if word['MOSentence'] == 'direct supplement':
    # ищем прямое дополнение
    index2 = index+1
    while index2 < sentence.getLen():
      if sentence.GetSet(index2, 'MOSentence') == 'supplement':
        word['link'].append(index2)
        break
      index2 += 1

  return index, GN

def getSyntA(sentence):
  GrammarNazi = []

  # определяет члены предложения
  index = 0
  while index < sentence.getLen():
    index, GN = setMOSentence(index, sentence)
    GrammarNazi.extend(GN)
    index += 1

  # устанавливает связи членов предложения
  index = 0
  while index < sentence.getLen():
    index, GN = setLinks(index, sentence)
    GrammarNazi.extend(GN)
    index += 1

  return sentence, GrammarNazi
