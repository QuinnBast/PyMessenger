import socket
import threading
import json

class Server:
    def __init__(self):
        # Configure the server and allow it to accept connections
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # Bind the socket to the local machine
        self.server.bind(('localhost', 49152))
        # Make the socket able to listen for connections on the port
        self.server.listen(5)

        # Maintain a list of all client threads
        self.threads = {}

        print("Awaiting Connections.")
        self.watchConnections()

    def watchConnections(self):
        while True:
            # If the server has data, a new connection is ready to be established.
            conn, address = self.server.accept()
            print(str(address[0]) + " has connected.")
            t = threading.Thread(target=self.listen, args=(conn, address))
            self.threads[conn] = t
            t.start()

    def sendAll(self, data):
        for c in self.threads:
            c.send(json.dumps(data).encode('utf-8'))

    def listen(self, conn, address):
        while True:
            # Try to read data from the client.
            # This function is blocking until data is recieved
            try:
                data = conn.recv(1024)
            except:
                # Remove the connection from the list and stop the listening thread.
                thread = self.threads[conn]
                self.threads.pop(conn)

                dc_msg = str(conn.getsockname()[0]) + " has disconnected."
                print(dc_msg)

                # Tell remaining connections they disconnected
                data = {
                    'msg': dc_msg,
                    'status': 'Inactive',
                    'from': 'host'
                }
                self.sendAll(data)
                break

            # turn the data back into a string and load into a json object
            data = json.loads(data.decode('utf-8'))

            # Ensure data was received
            if data:
                output = data['from'] + ": " + data['msg']
                print(output)
                self.sendAll(data)

Server()
