# -*- coding: utf-8 -*-
# Author: Ra93POL
# Date: 2.12.2014
""" Модуль, содержащий объекты предложения и текста. Не зависимы от ЕЯ.
    Объекты предоставляют удобный интерфейс,
    что позволяет разгрузить модули ЕЯ от руктинного и отвлекающего кода.
"""


class Sentence():
  """ Класс объекта предложения. Индексы списка и ключи словаря должны совпадать.
      При инициализации класса ему передаётся предложение в виде списка слов.
  """
  dict_sentence = {}

  def __init__(self, list_sentence):
    self.dict_sentence = {index: {} for index in range(len(list_sentence))}
    for index in range(len(list_sentence)):
      self.dict_sentence[index]['word'] = list_sentence[index]
      self.dict_sentence[index]['feature'] = []
      self.dict_sentence[index]['link'] = []

  def _syncLinks(self, words, deleted):
    """ Синхронизирует ссылки в словах """
    for word in words:
      for indexLink in word["link"]:
        t = 1
        index = word["link"].index(indexLink)
        for indexDel in deleted:
          if indexLink > indexDel:
            word["link"][index] -= t
          elif indexLink == indexDel:
            del word["link"][index]
          t =+ 1

  def _sync(self):
    """ Синхронизирует ключи словаря, то есть смещает их.
        Используется после удаления слов. """
    deleted = [] # индексы некогда удалённых слов, в порядке возрастания
    prev_sdvig = 0

    prev_index = -1
    sdvig = 0
    for  index, dict_word in self.dict_sentence.items():
      sdvig = index - prev_index - 1
      if sdvig > prev_sdvig: deleted.append(index-1)
      self.dict_sentence[index-sdvig] = self.dict_sentence[index]
      if sdvig > 0:
        del self.dict_sentence[index]
      prev_index = index-sdvig
      prev_sdvig = sdvig
    # синхронизируем ссылки
    self._syncLinks(self.dict_sentence.values(), deleted)

  def GetSet(self, index, parametr_name=None, parametr_value=None): # Get or Set Data
    """ Получение информации о слове по имени слова или по его порядковому номеру.
        Данные возвращаются все или только один параметр.
        Или же изменение данных, если указаны все три параметра."""
    if parametr_name == None :
      return self.dict_sentence[index]
    elif parametr_value == None:
      return self.dict_sentence[index][parametr_name]
    else:
      self.dict_sentence[index][parametr_name] = parametr_value

  def _getByCharacteristic(self, name, value, results, sentence):
    if str(type(sentence)) == "<type 'dict'>":
      sentence = sentence.values()
    for word in sentence:
      if word.has_key(name):
        if word[name] == value:
          results.append(word)
      if word.has_key("feature"):
        self._getByCharacteristic(name, value, results, word["feature"])
  def getByCharacteristic(self, name, value):
    results = []
    self._getByCharacteristic(name, value, results, self.dict_sentence)
    return results

  def delByCharacteristic(self, name, value):
    """ Удаляет слова, содержащие определённые характеристики """
    indexes = self.dict_sentence.keys()
    for index in indexes:
      if self.dict_sentence[index].has_key(name):
        if self.dict_sentence[index][name] == value:
          del self.dict_sentence[index]
    self._sync()

  def delByIndex(self, *indexes):
    """ Удаляет слово по его индексму или самому слову """
    for index in indexes:
      del self.dict_sentence[index]
    self._sync()

  def GetAndDel(self, index):
    word = self.dict_sentence[index]
    self._syncLinks([word], [index])
    self.delByIndex(index)
    return word
    #for indexLink in word["link"]:
    #  t = 0
    #  if indexLink < index:
    #    index2 = word["link"].index(indexLink)
    #    word["link"][index2] = indexLink - t
    #  elif indexLink == indexDel:
    #    index2 = word["link"].index(indexLink)
    #    del word["link"][index2]
    #  t =+ 1
    

  def addFeature(self, index, *indexes):
    """ Добавляет к слову определения и обстоятельства как его характеристику
        Первый аргумент - индекс главного слова, следующие аргументы -
        индексы обстоятельств и определений.
        Порядок значений второго аргумента может быть произвольным. """
    indexes = list(indexes)
    # удаляем повторяющиеся индексы
    i = 0
    while i < len(indexes):
      if indexes.count(indexes[i]) > 1: del indexes[i]
      else: i += 1
    word = self.dict_sentence[index]
    # добавляем определения и обстоятельства
    for index_feature in indexes:
      feature = self.dict_sentence[index_feature]
      word['feature'].append(feature)
    # удаляем из предложения
    self.delByIndex(*indexes)

  def addLink(self, index_control, index_obient):
    """ Устанавливает ссылку """
    if index_obient not in self.dict_sentence[index_control]["link"]:
      self.dict_sentence[index_control]["link"].append(index_obient)

  def getObient(self, index):
    """ Возвращает индексы тех слов, которые подчиняются слову по
        переданому индексу"""
    return self.dict_sentence[index]["link"]

  def getControl(self, index):
    """ Возвращает индексы тех слов, к которым подчинено слово по
        переданому индексу"""
    pass

  def getSentence(self, Type):
    if Type == 'str':
      pass
    elif Type == 'dict': return self.dict_sentence
    elif Type == 'listDict':
      l = len(self.dict_sentence)
      listDict = []
      for index in range(l): listDict.append(self.dict_sentence[index])
      return listDict
    elif Type == 'forLogicDict':
      return "it must be ready for Logic module)))"
    elif Type == 'beautyDict':
      return "it must be beauty)))"

  def getLen(self, func=None):
    """ Возвращает длину предложения. Может применить к длин функцию,
        например range, после этого возвратится список """
    if func == None: return len(self.dict_sentence)
    else: return func(len(self.dict_sentence))

  def functionToValues(self, index, parametr_name, function):
    """ Метод применяет функцию к каждому элементу параметра слова.
        То есть, можеть менять элементы параметров feature, link. """
    word = self.dict_sentence[index]
    for i in range(len(word[parametr_name])):
      word[parametr_name][i] = function(word[parametr_name][i])

class Text():
  """ Класс объекта ткста.
      Возможности: анализ, обработка (изменение времени и прочее)
  """
  def __init__(self):
    pass

if __name__ == '__main__':
  s = "Hello0 my1 smarControl2 t3 home4 I5 createdObient6 your7 intellect8"
  s = Sentence(s.split())

  #s.GetSet(1, "bl", "gggg")
  #s.GetSet(2, "bl", "gggg")
  s.GetSet(7, "bl", "gggg")

  s.delByCharacteristic("bl", "gggg")
  print("111111111111111111")
  #s.delByWI(0)
  #s.delByWI("your7")

  s.addLink(2, 6)
  s.delByIndex(0)
  s.delByIndex(4)

  print s.getSentence("str"), '\n'
  print s.getSentence("list"), '\n'
  print s.getSentence("dict"), '\n'
  print s.getSentence("beautyDict"), '\n'
