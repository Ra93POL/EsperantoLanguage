# -*- coding: utf-8 -*-
''' Модуль вспомогательный. Сохраняет результаты анализов для последующего
    выявления ошибок и неточностей.
'''
import os, datetime, codecs

file_path = 'analisys.txt'

def fwrite(data):
  global file_path
  if not os.path.exists(file_path):
    f = open(file_path, 'w')
    f.close()
  with codecs.open(file_path, 'a', 'utf-8') as f:
    #f = open(file_path, 'w')
    f.write(data)#.decode('utf-8'))
    f.close()

def safeResults(l, title, space=''):
  ''' удобно сохраняет список словарей или словарь словарей'''
  #f = _getFO()
  if title != None: fwrite(('- '*10)+title+(' -'*10)+u'\n')

  if str(type(l))[7:-2] == 'dict':
    l2 = []
    for k, v in l.items():
      l2.append(v)
    l = l2

  for res in l:
    if str(type(res))[7:-2] in ['int', 'str']:
      fwrite(space + str(res) + u'\n')
      continue
    for k, v in res.items():
      if str(type(v))[7:-2] == 'list':
        fwrite(space + k + u' : \n')
        #f.close()
        safeResults(v, None, space+'    ')
        #f = _getFO()
        continue
      fwrite(space + k + ' : ' + unicode(v) + u'\n')
    index = l.index(res)
    if index != len(l)-1: fwrite(u'\n')
  #f.close()

def safeUnknown(list_res):
  ''' запись нераспознанных слов '''
  #f = _getFO()
  l = []
  for res in list_res:
    #if res.has_key('POSpeech') == 0:
    #if len(res) == 1:
    if res['POSpeech'] == '':
      l.append(res['word'])
  index = 0
  while index < len(l):
    if l.count(l[index]) > 1: del l[index]
    index += 1
  t = ''
  for word in l: t += word + ' '
  fwrite(u'Нераспознанные слова: ' + t + u'\n\n')
  #f.close()

def FWrite(text):
  ''' Функция для свободной записи '''
  #f = _getFO()
  fwrite(text)
  #f.close

def getTime():
  now = datetime.datetime.now()
  return now.strftime("%Y.%m.%d %H:%M:%S")
