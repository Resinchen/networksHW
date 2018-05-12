import base64
import os


class Mail:
    def __init__(self, retr_data, top_data):
        self.tfrom = top_data.split('From: ')[1].split('\n')[0].strip() if top_data.__contains__('From: ') else None
        self.to = top_data.split('To: ')[1].split('\n')[0].strip() if top_data.__contains__('To: ') else None
        self.subject = top_data.split('Subject: ')[1].split('\n')[0].strip() if top_data.__contains__('Subject: ') else None
        self.date = top_data.split('\nDate:')[-1].split('\n')[0].strip() if top_data.__contains__('Date: ') else None
        self.content_type = top_data.split('Content-Type:')[1].split('\n')[0].strip() if top_data.__contains__('Content-Type: ') else 'text/plain'
        self.boundary = top_data.split('boundary="')[1].split('"')[0] if self.content_type.__contains__('multipart/mixed') else None
        self.contents = self._get_contents(retr_data)

    def _get_contents(self, retr_data):
        if self.boundary is None:
            return [retr_data.split('\r\n.\r\n')[0].split('\r\n\r\n')[1]]
        else:
            return retr_data.split(self.boundary)[2:-1]

    def get_folder_with_contents(self, index):
        a = os.getcwd()
        path_folder = '{}/mail_{}'.format(a, index)
        if not os.path.exists(path_folder):
            os.mkdir(path_folder)

        if self.content_type.split('/')[0] == 'text':
            if self.content_type.split('/')[1] == 'plain':
                filename = 'text_message.txt'
                file_name = path_folder + '/' + filename
                data = self.contents[0]
                with open(file_name, 'wb') as f:
                    f.write(data.encode())
            elif self.content_type.split('/')[1] == 'html':
                filename = 'html_message.html'
                file_name = path_folder + '/' + filename
                data = self.contents[0]
                with open(file_name, 'wb') as f:
                    f.write(data.encode())

        else:
            for content in self.contents:
                content_ttype = content.split('Content-Type: ')[1].split('\n')[0]

                if content_ttype.__contains__('text'):
                    if content_ttype.__contains__('plain'):
                        filename = 'text_message.txt'
                        file_name = path_folder + '/' + filename
                        data = content.split('\r\n\r\n')[1].split('--')[0]
                        with open(file_name, 'wb') as f:
                            f.write(data.encode())
                    elif content_ttype.__contains__('html'):
                        filename = 'html_message.html'
                        file_name = path_folder + '/' + filename
                        data = content.split('\r\n\r\n')[1].split('--')[0]
                        with open(file_name, 'wb') as f:
                            f.write(data.encode())

                elif content_ttype.__contains__('audio'):
                    filename = content.split('filename="')[1].split('"')[0]
                    data = content.split('\r\n\r\n')[1]
                    data_decoded = base64.b64decode(data)
                    file_name = path_folder + '/' + filename
                    with open(file_name, 'wb') as f:
                        f.write(data_decoded)

                elif content_ttype.__contains__('image'):
                    filename = content.split('filename="')[1].split('"')[0]
                    data = content.split('\r\n\r\n')[1]
                    data_decoded = base64.b64decode(data)
                    file_name = path_folder + '/' + filename
                    with open(file_name, 'wb') as f:
                        f.write(data_decoded)
        print('Письмо сохранено по пути: {}'.format(path_folder))
