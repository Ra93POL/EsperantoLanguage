# -*- coding: utf-8 -*-
'''
Этот модуль выполняет комплексный анализ тескта на ЕЯ Эсперанто.
'''

from PrepearingText import Prepearing # для langModules/__init__.py
from MorphologicalAnalysis import getMorphA
from PostMorphologicalAnalysis import getPostMorphA
from SyntacticAnalysis import getSyntA

#import BeautySafe as BS

def NL2ResultA(sentence): # natural language to internal language
  ''' Принимает объект предложения и возвращает его уже, но с анализами '''
  GrammarNazi = {}

  # Анализируем предложение
  #BS.FWrite("- "*10 + BS.getTime() + " -"*10 + "\n\n")
  sentence, GrammarNazi['getMorphA'] = getMorphA(sentence)
  #BS.safeResults(sentence, u"Морфологический анализ")
  #BS.safeUnknown(list_res)
  sentence, GrammarNazi['getPostMorphA'] = getPostMorphA(sentence)
  #BS.safeResults(list_res, u"Промежуточный анализ")
  sentence, GrammarNazi['getSyntA'] = getSyntA(sentence)
  #BS.safeResults(list_res, u"Синтаксический анализ")

  print GrammarNazi
  return sentence, GrammarNazi

def IL2NL(IL):
  NL = IL
  return NL
