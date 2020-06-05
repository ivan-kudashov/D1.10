import sys
import requests

base_url = "https://api.trello.com/1/{}"
auth_params = {
    'key': "c1bbcf84104292cdf1b48489292b6b27",
    'token': "ce9aaaf859d79849b1611678238e3c9fb0d28473e789285059bb5eb6ee73d6b7",
}
board_id = "5eda20004e22e92092a21d7a"

def read():
    column_data = requests.get(base_url.format('boards') + '/' + board_id + '/lists', params=auth_params).json()

    for column in column_data:
        task_data = requests.get(base_url.format('lists') + '/' + column['id'] + '/cards', params=auth_params).json()
        print(column['name'] + " кол-во задач ({})".format(len(task_data)))

        if not task_data:
            print('\t' + 'Нет задач!')
            continue
        for task in task_data:
            print('\t' + task['name'] + '\t' + task['id'])

def create(name, column_name):
    column_id = column_check(column_name)
    if column_id is None:
        column_id = createColumn(column_name)['id']
    requests.post(base_url.format('cards'), data={'name': name, 'idList': column_id, **auth_params})

def move(name, column_name):
    duplicate = task_duplicates(name)
    if len(duplicate) > 1:
        print("Дубликатов задач:")
        for index, task in enumerate(duplicate):
            task_column_name = requests.get(base_url.format('lists') + '/' + task['idList'], params=auth_params).json()['name']
            print("Задача №{}\tid: {}\tКолонка: {}\t ".format(index, task['id'], task_column_name))
        task_id = input("Введите ID задачи, которую требуется переместить: ")
    else:
        task_id = duplicate[0]['id']

    column_id = column_check(column_name)
    if column_id is None:
        column_id = createColumn(column_name)['id']
    requests.put(base_url.format('cards') + '/' + task_id + '/idList', data={'value': column_id, **auth_params})

def column_check(column_name):
    column_data = requests.get(base_url.format('boards') + '/' + board_id + '/lists', params=auth_params).json()
    for column in column_data:
        if column['name'] == column_name:
            return column['id']
    return

def createColumn(column_name):
    return requests.post(base_url.format('lists'), data={'name': column_name, 'idBoard': board_id, **auth_params}).json()

def task_duplicates(task_name):
    column_data=requests.get(base_url.format('boards')+'/'+board_id+'/lists', params=auth_params).json()
    duplicate=[]
    for column in column_data:
        column_tasks=requests.get(base_url.format('lists')+'/'+ column['id']+'/cards', params=auth_params).json()
        for task in column_tasks:
            if task['name'] == task_name:
                duplicate.append(task)
    return duplicate

if __name__ == "__main__":
    if len(sys.argv) <= 2:
        read()
    elif sys.argv[1] == 'create':
        create(sys.argv[2], sys.argv[3])
    elif sys.argv[1] == 'createColumn':
        createColumn(sys.argv[2])
    elif sys.argv[1] == 'move':
        move(sys.argv[2], sys.argv[3])