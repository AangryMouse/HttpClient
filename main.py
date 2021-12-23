from copy import deepcopy
import socket
import re


class HttpClient:
    def __init__(self, url, type_request, headers=None, data=None, cookies=None):
        self.url = url
        self.type_request = type_request.upper()
        self.headers = deepcopy(headers) if headers is not None else {}
        self.data = deepcopy(data) if data is not None else {}
        self.cookies = deepcopy(cookies) if cookies is not None else {}
        self.host = re.split("//|\?|#|/", self.url)[1]
        self.path = url.split(self.host)[1] if url.split(self.host)[1] != '' else '/'
        self.answer = ''

    def send_request(self, timeout=3):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
            sock.connect((self.host, 80))
            sock.settimeout(timeout)
            try:
                sock.send(self.text_request())
                data = sock.recv(1024)
            except BlockingIOError:
                print("Time is up!!")
            else:
                self.answer = data.decode('utf-8')

    def text_request(self):
        enter = '\n'
        body = '&'.join([f'{e}={self.data[e]}' for e in self.data])
        request = (f'{self.type_request} {self.path} HTTP/1.1\n' 
                  f'Host: {self.host}\n' 
                  f'{f"{enter}".join([f"{head}: {self.headers[head]}" for head in self.headers])}\n'
                  f'Cookie: {";".join([f"{e}={self.cookies[e]}"for e in self.cookies])}\n'
                  f'Content-Type: application/x-www-form-urlencoded\n' 
                  f'Content-Length: {len(body)}\n\n' 
                  f'{body}\n')
        return request.encode('utf-8')

    def save_in_file(self, path):
        with open(path, mode='w', encoding='utf-8') as file:
            file.write(self.answer)



a = HttpClient('http://hw1.alexbers.com', 'get', data={'as': 'sa', 'qw': 'qwe'})

a.send_request()
a.save_in_file(r'C:\Users\aplas\httpclient\venv\qwe')
