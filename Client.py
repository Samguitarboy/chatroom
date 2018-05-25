import socket
import threading
from PyQt5.QtWidgets import QMainWindow,QApplication
import client_ui
import sys


class Client:
    def __init__(self, host, port):
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock = sock
        self.sock.connect((host, port))
        self.sock.send(b'1')


    def sendThreadFunc(self):
        count=1
        while True:
            try:

                if count == 1:
                    nickname = input()
                    print('Now Lets Chat, ', nickname)
                    self.sock.send(nickname.encode())
                    count+=1

                myword = input()
                myword = nickname + ":" + myword
                self.sock.send(myword.encode())

            except ConnectionAbortedError:
                print('Server closed this connection!')
            except ConnectionResetError:
                print('Server is closed!')

    def recvThreadFunc(self):
        while True:
            try:
                otherword = self.sock.recv(1024) # socket.recv(recv_size)
                print(otherword.decode())
            except ConnectionAbortedError:
                print('Server closed this connection!')

            except ConnectionResetError:
                print('Server is closed!')

class Main(QMainWindow,client_ui.Ui_MainWindow):
    def __init__(self):
        super(self.__class__,self).__init__()
        self.setupUi(self)

def main():
    app=QApplication(sys.argv)
    MainWindow=Main()
    MainWindow.show()
    sys.exit(app.exec_())
    c = Client('140.138.145.58', 5550)
    th1 = threading.Thread(target=c.sendThreadFunc)
    th2 = threading.Thread(target=c.recvThreadFunc)
    threads = [th1, th2]

    for t in threads:
        t.setDaemon(True)
        t.start()

    t.join()


if __name__ == "__main__":
    main()
