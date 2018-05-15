import pickle
import socket
from os.path import exists

from Types import quere, typeA, typeNS, typeAAAA

PORT = 53
# SERVER = 'ns1.e1.ru'
SERVER = '8.8.8.8'
LOCALHOST = '127.0.0.1'
KNOWED_TYPE = ['A', 'NS', 'AAAA']

class DNS_Cache:
    def __init__(self):
        self.__cache = dict()
        self.__sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.__sock.bind((LOCALHOST, PORT))
        self.__sock.settimeout(6)

    def _send_to_server(self, message):
        send_sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        send_sock.sendto(message, (SERVER, PORT))
        data, addr = send_sock.recvfrom(512)
        return data

    def _serialize_cache(self, cache):
        with open('cache_DNS.ch', 'wb') as f:
            pickle.dump(cache, f)

    def _deserialize_cache(self):
        with open('cache_DNS.ch', 'rb') as f:
            data = pickle.load(f)
        return data

    def _set_def_dict(self):
        return {'A': None, 'NS': None, 'AAAA': None}

    def _get_resp_obj(self, type, message):
        if type == 'A':
            return typeA(message)
        elif type == 'NS':
            return typeNS(message)
        elif type == 'AAAA':
            return typeAAAA(message)

    def _read_cache(self):
        if exists('cache_DNS.ch'):
            return self._deserialize_cache()
        else:
            return dict()

    def main_work(self):
        try:
            self.__cache = self._read_cache()

            while True:
                message, address = self.__sock.recvfrom(512)
                cur_que = quere(message)

                if cur_que.name in self.__cache.keys() and self.__cache[cur_que.name][cur_que.type] is not None:
                    print('Look in cache! {}-{}'.format(cur_que.name, cur_que.type))
                    response = self.__cache[cur_que.name][cur_que.type]
                    self.__sock.sendto(response.create_resp(), address)
                else:
                    print('Not look!!! {}-{}'.format(cur_que.name, cur_que.type))
                    if cur_que.type in KNOWED_TYPE:
                        response = self._send_to_server(message)
                        if cur_que.name not in self.__cache.keys():
                            self.__cache[cur_que.name] = self._set_def_dict()
                        resp_obj = self._get_resp_obj(cur_que.type, response)
                        self.__cache[cur_que.name][cur_que.type] = resp_obj
                        self.__sock.sendto(response, address)
                    else:
                        response = self._send_to_server(message)
                        self.__sock.sendto(response, address)


                print()
        except socket.timeout:
            self._serialize_cache(self.__cache)
            for k, v in self.__cache.items():
                for k1, v1 in v.items():
                    print(f'{k1}: {v1}')
                print('-+-+-+-+-+-+-+-')


if __name__ == '__main__':
    dns = DNS_Cache()
    dns.main_work()
