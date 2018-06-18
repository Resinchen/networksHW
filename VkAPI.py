import requests
from PeopleNote import People


def update_token():
    return "29991d94b580c41085f4251b42527c8abc5a579b7aab92b60954f02809b609725eed182162558c9408579"


def main(user_id):
    access_token = update_token()
    req = create_request(user_id, access_token)
    resp = get_response(req)
    peoples = get_notes_people(resp)

    print('Give command for sort: (name, sex, online, bdate, city)')
    command = input()
    sorted_people = None

    if command == 'name':
        sorted_people = sort_by_names(peoples)
    elif command == 'sex':
        sorted_people = sort_by_sex(peoples)
    elif command == 'online':
        sorted_people = sort_by_online(peoples)
    elif command == 'bdate':
        sorted_people = sort_by_bdate(peoples)
    elif command == 'city':
        sorted_people = sort_by_city(peoples)

    if sorted_people:
        presented(sorted_people)
        saved_sorted_people(command, sorted_people)


def create_request(user_id, access_token):
    return f'https://api.vk.com/method/friends.get?user_id={user_id}&order=hints&fields=name,sex,bdate,' \
           f'city&access_token={access_token}&v=5.52 '


def get_response(request):
    return requests.get(request).json()


def get_notes_people(json_response):
    result = []
    for r in json_response['response']['items']:
        result.append(People(r))
    return result


def sort_by_names(peoples):
    result = dict()
    for p in peoples:
        if p.first_name not in result.keys():
            result[p.first_name] = []
        result[p.first_name].append(p)
    return result


def sort_by_sex(peoples):
    result = dict()
    for p in peoples:
        if p.sex not in result.keys():
            result[p.sex] = []
        result[p.sex].append(p)
    return result


def sort_by_online(peoples):
    result = dict()
    for p in peoples:
        if p.online not in result.keys():
            result[p.online] = []
        result[p.online].append(p)
    return result


def sort_by_bdate(peoples):
    result = dict()
    for p in peoples:
        if p.bdate not in result.keys():
            result[p.bdate] = []
        result[p.bdate].append(p)
    return result


def sort_by_city(peoples):
    result = dict()
    for p in peoples:
        if p.city not in result.keys():
            result[p.city] = []
        result[p.city].append(p)
    return result


def presented(sorted_dict):
    for k, v in sorted_dict.items():
        print('[', k.upper(), ']')
        for vv in v:
            print("\t {}".format(vv))
        print('Count note: ', len(v))
        print()
    print('Count keys: {}'.format(len(sorted_dict.keys())))


def saved_sorted_people(name_sort, sorted_people):
    filename = name_sort + '.txt'
    res = ''
    for k, v in sorted_people.items():
        res += '[' + k.upper() + ']\n'
        for vv in v:
            res += "\t {}\n".format(vv)
        res += 'Count note: {}\n\n'.format(len(v))
    res += 'Count keys: {}'.format(len(sorted_people.keys()))

    with open(filename, 'w', encoding='utf-8') as f:
        f.write(res)


if __name__ == '__main__':
    print("Get id user")
    user_id = input()
    main(user_id)
