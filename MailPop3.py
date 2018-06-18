import base64
import os


class Mail:
    def __init__(self, retr_data, top_data):
        top_dict = self._get_top_dict(top_data)
        self.tfrom = top_dict['From'] if 'From' in top_dict.keys() else None
        self.to = top_dict['To'] if 'To' in top_dict.keys() else None
        self.subject = top_dict['Subject'] if 'Subject' in top_dict.keys() else None
        self.date = top_dict['Date'] if 'Date' in top_dict.keys() else None
        self.content_type = top_dict['Content-Type'] if 'Content-Type' in top_dict.keys() else 'text/plain'
        self.boundary = top_dict['boundary'] if self.content_type == 'multipart/mixed;' else None
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

    def _get_top_dict(self, top_data):
        res = dict()
        top_lines = top_data.split('\r\n')
        for line in top_lines[:-2]:
            if 'boundary' in line:
                i = line.find('boundary=') + len('boundary=')
                res[line[1:i-1]] = line[i+1:-1]
                continue
            if '\t' in line:
                continue
            v = line.split(':')
            res[v[0]] = v[1].strip()
        return res
