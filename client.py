import requests
import json

adress='http://127.0.0.1:5000/'

def add_record(id):
    request=requests.post(adress+'records/add', json={'record_id':'%s' %(id)})
    print(request)

def remove_record(id):
    request=requests.delete(adress+'records/%s' %(id))
    print(request,'\n')

def put_record(id):
    title = input("Record's title: ")
    year = input("Year: ")
    artist = input("Artist: ")
    genre = input("Genre: ")
    numberoftracks = input("Number of tracks: ")
    length = input("Length of the album:")
    request = requests.put(adress + 'records/%s' % (id),
                           json={'Title': title, 'Year': int(year), 'Artist': artist,
                                 'Genre': genre, 'NumberOfTracks': int(numberoftracks), 'Length': length})
    print(request, '\n')



def get_info(id):
    response = requests.get(adress + 'records/%s' % (id))
    print(response, '\n')
    response_dictionary = json.loads(response.text)
    print('Info about record:', id)
    for key in response_dictionary[id]:
        print(key, ':', response_dictionary[id][key])

def print_all():
    response=requests.get(adress+'ListOfRecords')
    response_dict=json.loads(response.text)
    print(response)
    print("List of records: ")
    for i in response_dict:
       print("Number of record: ",i)

def get_info_all():
    response=requests.get(adress+'sets')
    response_dict=json.loads(response.text)
    print(response)
    print ("List of sets: ")
    for i in response_dict:
        print("Nr of set: ",i)


menu = {}
menu['1']="Get list of records (GET)"
menu['2']="Add record id (POST)"
menu['3']="Update record info (PUT)"
menu['4']="Get set info (GET)"
menu['5']="Delete set (DELETE)"
menu['6']="Exit "

while True:
  options=menu.keys()
  for entry in options:
      print(entry, menu[entry])
  print('\n')
  select = input("Select function: ")
  if select == '1':
      print_all()
  elif select == '2':
      id = input("Input id of record to create: ")
      add_record(id)
  elif select == '3':
      id = input("Update record data \n  Input id of record to update: ")
      put_record(id)
  elif select == '4':
      id = input("Get record data \n Input record id: ")
      get_info(id)
  elif select == '5':
      id = input("Delete record data \n Input id of record to delete: ")
      remove_record(id)
  elif select == '6':
      print("Exit")
      break
  else:
      print("ERROR !!!  \n \n")
  print('\n ')