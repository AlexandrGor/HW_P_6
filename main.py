import requests
from pprint import pprint
import json

documents = [
  {"type": "passport", "number": "2207 876234", "name": "Василий Гупкин"},
  {"type": "invoice", "number": "11-2", "name": "Геннадий Покемонов"},
  {"type": "insurance", "number": "10006", "name": "Аристарх Павлов"}
            ]
directories = {
              '1': ['2207 876234', '11-2'],
              '2': ['10006'],
              '3': []
              }

def search_person():
  number = input("\nВведите номер документа: ")
  for doc in documents:
    if doc["number"] == number:
      print(f"Искомый владелец: {doc['name']}")
      return doc['name']
  print("\nВладелец с таким номером не найден........")

def search_shelf():
  number = input("\nВведите номер документа: ")
  for shelf in directories:
    if number in directories[shelf]:
      print(f"Документ на полке: {shelf}")
      return shelf
  print("\nТакого документа нет........")

def all_documents():
  print('\nСписок всех документов:')
  for doc in documents:
    print(f'{doc["type"]} "{doc["number"]}" "{doc["name"]}"')

def new_document():
  number = input("\nВведите номер нового документа: ")
  type_ = input("Введите тип нового документа: ")
  name = input("Введите имя владельца: ")
  documents.append({"type": type_, "number": number, "name": name})
  while True:
    print("Доступные полки:", ' '.join(list(directories.keys())))
    shelf = input("На какой полке будет документ: ")
    if shelf in directories:
      directories[shelf].append(number)
      break
    print("\nПолка указана неверно........")
  print(f"Документ {number} успешно добавлен")

def delete_document():
  doc_numbers = []
  for doc in documents:
    doc_numbers.append(doc["number"])
  print("\nСписок доступных к удалению документов:",
  f"\n{', '.join(doc_numbers)}")
  number = input("Удалить документ с номером: ")
  if number in doc_numbers:
    for doc in documents:
      if doc["number"] == number:
        documents.remove(doc)
        break
    for shelf in directories:
      if number in directories[shelf]:
        directories[shelf].remove(number)
        break
    print(f"Документ {number} успешно удален")
  else:
    print("\nТакого документа нет........")

def move_document():
  doc_numbers = []
  for doc in documents:
    doc_numbers.append(doc["number"])
  print("\nСписок доступных к перемещению документов:",
  f"\n{', '.join(doc_numbers)}")
  number = input("Переместить документ с номером: ")
  if number in doc_numbers:
    for shelf in directories:
      if number in directories[shelf]:
        print(f"\nВыбранный документ на полке: {shelf}")
        available_shelves = list(directories.keys())
        available_shelves.remove(shelf)
        print("Доступные полки:", *available_shelves)
        next_shelf = input("Переместить документ на полку: ")
        if next_shelf in list(directories.keys()):
          if shelf == next_shelf:
            print("Документ останется на месте........")
          else:
            directories[shelf].remove(number)
            directories[next_shelf].append(number)
            print(f"Документ {number} успешно перемещен с полки {shelf} на {next_shelf}")
        else:
          print("\nТакой полки не существует........")
        break
  else:
    print("\nТакого документа нет........")

def new_shelf():
  print("\nСуществующие полки:", *list(directories.keys()))
  new_shelf = input("Введите номер новой полки: ")
  if new_shelf not in list(directories.keys()):
    directories.update({new_shelf : []})
    print(f"Полка {new_shelf} успешно создана")
  else:
    print("\nТакая полка уже существует........")

def secretary_programm():
  command_dict = {'p' : "search_person()", 'l' : "all_documents()",
                  's' : "search_shelf()", 'a' : "new_document()",
                  'd' : "delete_document()", 'm' : "move_document()",
                  'as' : "new_shelf()"}
  while True:
    command = input("\nВведите команду:\n"
    "p  – найти владельца по номеру документа;\n"
    "s  – найти полку с документом;\n"
    "l  – вывод списка документов;\n"
    "a  – добавить новый документ;\n"
    "d  – удалить документ;\n"
    "m  – переместить документ на другую полку;\n"
    "as – создать новую полку;\n"
    "q – выход из программы.\n"              
    "Команда: ")
    if command == 'q':
      break
    if command in command_dict:
      eval(command_dict[command])
    else:
      print("\nКоманда введена неверно............")


class YaUploader:
  token = ''

  def __init__(self, folder_path):
    self.folder_path = folder_path
  def new_folder(self):
    url = 'https://cloud-api.yandex.net/v1/disk/resources'
    headers = {'Content-Type': 'application/json',
               'Authorization': 'OAuth {}'.format(self.token)}
    params = {'path': self.folder_path}
    try:
      res = requests.put(url, headers=headers, params=params)
      res.raise_for_status()
    except:
      pass
    if res.status_code == 201:
      return 'Папка на создана на Я.Диск'
    if res.status_code == 409:
      return "Ошибка 409, возможно папка уже существует, либо в названии папки есть /"
    return f'Ошибка {res.status_code}'



if __name__ == '__main__':
  #secretary_programm()

  folder = input('Новая яндекс-папка: ')
  uploader = YaUploader(folder)
  print(uploader.new_folder())