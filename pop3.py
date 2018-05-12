import socket
import ssl

from MailPop3 import Mail

# 1-письмо с mp3
# 2-письмо html
# 3-письмо с картинкой

POP_SERVER = 'pop.yandex.ru'
SSL_POP_PORT = 995

class POP3Client:
    def __init__(self):
        self.cache_answer = []
        self._start_work()
        self._create_socket()
        self._socket_logining()
        self._start_main_work()

    def _start_work(self):
        print('Приветствую')
        print('------------------------------')
        print('Вы подключаетесь к ЯндексПочта')
        print('Пожалуйста, авторизуйтесь')
        print('------------------------------')
        print('Введите email')
        #self.email_addr = input()
        self.email_addr = 'testIMAPChe@yandex.ru'
        print('Введите пароль')
        #self.email_password = input()
        self.email_password = 'fortest'
        print('------------------------------')
        print()

    def _create_socket(self):
        self.sock = ssl.SSLSocket(socket.socket(socket.AF_INET, socket.SOCK_STREAM))
        self.sock.connect((POP_SERVER, SSL_POP_PORT))
        self.cache_answer.append(self.sock.recv(1024))

    def _socket_logining(self):
        self.sock.send('USER {}\r\n'.format(self.email_addr).encode())
        self.cache_answer.append(self.sock.recv(1024))
        self.sock.send('PASS {}\r\n'.format(self.email_password).encode())
        self.cache_answer.append(self.sock.recv(1024))
        print('Вы авторизированы!')

    def _start_main_work(self):
        self.count_message = self.cache_answer[-1].decode().replace('\r\n', '').split(' ')[1]
        print('Выберите сообшение из диапазона 1-{}'.format(self.count_message))
        self.current_num_message = input()

        self.sock.send('RETR {}\r\n'.format(self.current_num_message).encode())
        self.message = self._get_full_multy_recv()
        self.cache_answer.append(self.message)

        self.sock.send('TOP {} 0\r\n'.format(self.current_num_message).encode())
        self.top = self._get_full_multy_recv().decode()
        self.cache_answer.append(self.top)
        self.mail = Mail(self.message.decode(), self.top)

        print('------------------------------')
        print()

    def _get_full_multy_recv(self):
        data = self.sock.recv(1024)
        data_all = b''
        while b'\r\n.\r\n' not in data_all:
            data = self.sock.recv(1024)
            data_all += data
        return data_all

    def _print_help(self):
        print('------------------------------')
        print('''Для общения используйте следующие команды:
                • subject - вывод тему
                • top - вывод заголовки
                • date - вывод дату
                • sender - вывод адресанта
                • save - сохранить данные письма в отдельную папку
                • help - вывод спарвки
                • quit - выход из программы''')
        print()
        print('------------------------------')

    def main_work(self):
        print('Далее вводите команды для работы с письмом')
        print()
        self._print_help()
        while True:
            comand = input().lower()
            if comand == 'subject':
                print('Subject: ' + self.mail.subject)
            elif comand == 'top':
                print(self.top)
            elif comand == 'date':
                print('Date: ' + self.mail.date)
            elif comand == 'sender':
                print('Sender: ' + self.mail.tfrom)
            elif comand == 'help':
                self._print_help()
            elif comand == 'save':
                self.mail.get_folder_with_contents(self.current_num_message)
                print('Saved!')
            elif comand == 'quit':
                self.sock.send(b'QUIT\r\n')
                self.cache_answer.append(self.sock.recv(1024))
                self.sock.close()
                print('Quited')
                break
            else:
                print('Неверная команда!')


def main():
    p = POP3Client()
    p.main_work()


if __name__ == '__main__':
    main()
