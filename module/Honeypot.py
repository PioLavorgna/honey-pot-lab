import socket
import datetime

class HoneypotServer:
    
    def __init__(self,host,port,log_file):
        self.host = host
        self.port = port
        self.logger = Logger(log_file)
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.running = True

    def start(self):
        self.server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.server_socket.bind((self.host, self.port))
        self.server_socket.listen(5)
        print(f'\n>> Honeypot listening on {self.host} : {self.port} OPEN\n')
        try:
            while self.running:
                try:
                    client_socket, client_address = self.server_socket.accept()
                    print(
                        '\n\n___________________________________________________________________\n'\
                        f'\tConnection from {client_address[0]} : {client_address[1]}\n'\
                        '+-------------------------------------------------------------------+\n'\
                    )
                    self.logger.log_connection(client_address,client_socket)
                    client_socket.close()
                except OSError as e:
                    pass
        except Exception as e:
            print(f'Errore generico: {e}')   
        finally:
            self.server_socket.close()
            pass

    def stop(self):
        self.running = False
        self.server_socket.close()

class Logger:

    def __init__(self,log_file):
        self.log_file = log_file

    def log_connection (self, client_address, client_socket):
        with open(self.log_file, 'a') as log_file:
            log_file.write(
                '\n_____________________________________________________________________________________________________________\n'\
                f'| DATETIME [{datetime.datetime.now()}]'\
                f'\n| IP CLIENT [{client_address[0]}]'\
                f'\n| PORT CONNECTED [{client_address[1]}]\n'\
                '+-----------------------------------------------------------------------------------------------------------+\n'\
            )
