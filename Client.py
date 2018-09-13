import socket
import threading
import json
import sys

class Client:
    def __init__(self):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            self.sock.connect(('localhost', 49152))
        except:
            print("Cannot connect to host.")
            quit(1)
        print("Connected!")

        t = threading.Thread(target=self.listen)
        t.start()

        self.sendMessages()

    def sendMessages(self):
        while True:
            data = {
                'msg': input("Msg:"),
                'status': 'Active',
                'from': str(self.sock.getsockname()[0])
            }
            self.sock.send(json.dumps(data).encode('utf-8'))

    def listen(self):
        while True:
            data = self.sock.recv(1024)
            data.decode('utf-8')
            if data:
                if data['from'] == "host":
                    print(data['msg'])
                else:
                    data = json.loads(data)
                    print(data['from'] + ":" + data['msg'])

Client()