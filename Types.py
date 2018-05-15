import struct

Typs = {1: 'A', 2: 'NS', 28: 'AAAA'}
Clas = {1: 'IN'}


class quere:
    def __init__(self, data):
        self.trID = struct.unpack('!H', data[:2])[0]
        self.flags = data[2:4]
        self.other = data[4:12]
        self.name = data[12:-4]
        self._type_code = struct.unpack('!H', data[-4:-2])[0]
        self.type = Typs[self._type_code] if self._type_code in Typs.keys() else self._type_code
        self._clas_code = struct.unpack('!H', data[-2:])[0]
        self.clas = Clas[self._clas_code] if self._clas_code in Clas.keys() else self._clas_code

    def __str__(self):
        return f'TrID: {self.trID} Name: {self.name} Type: {self.type} Class: {self.clas}'


class typeA:
    def __init__(self, data):
        self.before_data = data[:-16]
        self.name = struct.unpack('!H', data[-16:-14])[0]
        self._type_code = struct.unpack('!H', data[-14:-12])[0]
        self.type = Typs[self._type_code]
        self._clas_code = struct.unpack('!H', data[-12:-10])[0]
        self.clas = Clas[self._type_code]
        self.ttl = struct.unpack('!I', data[-10:-6])[0]
        self.data_length = struct.unpack('!H', data[-6:-4])[0]
        self.address = struct.unpack('!4B', data[-4:])

    def __str__(self):
        return f'Name: {self.name} Type: {self.type} Class: {self.clas} TTL: {self.ttl} Data: {self.address}'

    def create_resp(self):
        return self.before_data + struct.pack('!H', self.name) + \
               struct.pack('!H', self._type_code) + struct.pack('!H', self._clas_code) + \
               struct.pack('!I', self.ttl) + struct.pack('!H', self.data_length) + \
               struct.pack('!4B', self.address[0], self.address[1], self.address[2], self.address[3])


class typeNS:
    def __init__(self, data):
        self.before_data = data[:6]
        self.count_answer = struct.unpack('!H', data[6:8])[0]
        self.between_data = data[8:28]
        self.answers = self.get_answers(data[28:])

    def __str__(self):
        return f'Count: {self.count_answer} Answers: {self.return_answers()}'

    def create_resp(self):
        return self.before_data + struct.pack('!H', self.count_answer) + self.between_data + self.return_answers()

    def get_answers(self, data):
        result = []
        i = 0
        for q in range(self.count_answer):
            result.append(NSnote(data[i:i + 18]))
            i += 18
        return result

    def return_answers(self):
        result = b''
        for a in self.answers:
            result += a.get_answer()
        return result


class NSnote:
    def __init__(self, data_of_note):
        self.name = data_of_note[:2]
        self._type_code = struct.unpack('!H', data_of_note[2:4])[0]
        self.type = Typs[self._type_code]
        self._clas_code = struct.unpack('!H', data_of_note[4:6])[0]
        self.clas = Clas[self._clas_code]
        self.ttl = struct.unpack('!I', data_of_note[6:10])[0]
        self.data_length = struct.unpack('!H', data_of_note[10:12])[0]
        self.name_server = data_of_note[12:12 + self.data_length]

    def get_answer(self):
        return self.name + struct.pack('!H', self._type_code) + \
               struct.pack('!H', self._clas_code) + struct.pack('!I', self.ttl) + \
               struct.pack('!H', self.data_length) + self.name_server


class typeAAAA:
    def __init__(self, data):
        self.before_data = data[:-28]
        self.name = struct.unpack('!H', data[-28:-26])[0]
        self._type_code = struct.unpack('!H', data[-26:-24])[0]
        self.type = Typs[self._type_code]
        self._clas_code = struct.unpack('!H', data[-24:-22])[0]
        self.clas = Clas[self._clas_code]
        self.ttl = struct.unpack('!I', data[-22:-18])[0]
        self.data_length = struct.unpack('!H', data[-18:-16])[0]
        self.data_address = data[-16:]
        self.address = self.get_ipv6(self.data_address)

    def __str__(self):
        return f'Name: {self.name} Type: {self.type} Class: {self.clas} TTL: {self.ttl} Data: {self.address}'

    def create_resp(self):
        return self.before_data + struct.pack('!H', self.name) + \
               struct.pack('!H', self._type_code) + struct.pack('!H', self._clas_code) + \
               struct.pack('!I', self.ttl) + struct.pack('!H', self.data_length) + self.data_address

    def get_ipv6(self, data_ip):
        res = []
        for i in range(0, len(data_ip), 2):
            res.append(data_ip[i:i + 2].hex())
        return ':'.join(res)

