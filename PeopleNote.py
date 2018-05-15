class People:
    def __init__(self, entry):
        self.id = entry['id']
        self.first_name = entry['first_name']
        self.last_name = entry['last_name']
        self.sex = self.prepare_sex(entry['sex'])
        self.online = self.prepare_online(entry['online'])
        self.bdate = self.prepare_date(entry['bdate']) if 'bdate' in entry.keys() else 'Скрыто'
        self.city = entry['city']['title'] if 'city' in entry.keys() else 'Не указан'

    def prepare_sex(self, sex):
        if sex == 1:
            return 'Female'
        elif sex == 2:
            return 'Male'

    def prepare_online(self, online):
        if online == 0:
            return 'Offline'
        elif online == 1:
            return 'Online'

    def prepare_date(self, date):
        month = {'1': 'Январь', '2': 'Февраль', '3': 'Март', '4': 'Апрель',
                 '5': 'Май', '6': 'Июнь', '7': 'Июль', '8': 'Август',
                 '9': 'Сентябрь', '10': 'Октябрь', '11': 'Ноябрь', '12': 'Декабрь'}

        splited_date = date.split('.')
        splited_date[1] = month[splited_date[1]]
        return ' '.join(splited_date)

    def __str__(self):
        return f'ID: {self.id}, NAME: {self.first_name},' \
               f' SURNAME: {self.last_name}, SEX: {self.sex}, ' \
               f'ONLINE: {self.online}, BDATE: {self.bdate}, ' \
               f'CITY: {self.city}'
