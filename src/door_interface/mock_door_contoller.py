## Mock of the door contoller
from ctypes.wintypes import MSG
import socket
from threading import Thread

main_socket = None
main_port = 4040
door_id = 43

REQ_OPEN = b"REQ_DOOR_OPEN"
REQ_CLOSE = b"REQ_DOOR_CLOS"

MSGLEN = len(REQ_OPEN)
class DoorSocketMock():
    """ Mock class to pretend we have a door controller speaking a bespoke TCP protocol """
    def __init__(self,sock=None):
        if sock is None:
            self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        else:
            self.sock = sock

        try:
            self.sock.bind(("127.0.0.1", main_port))
            self.sock.listen(5)
            self.id_string = "[real_fake_door {}]".format(door_id)
        except Exception as e:
            print("[real_fake_door 43] failed to init socket: {}".format(e))
            exit(1)

    def accept_conn(self):
        (self.client_sock, self.client_addr) = self.sock.accept()
        self.handle_req()

    def handle_req(self):
        print("Got client socket: {} ".format(self.client_addr))
        data = self.client_sock.recv(MSGLEN)
        if (len(data) < MSGLEN):
            print(" Message too short. Ignoring.".format(self.id_string))
            self.req_okay = False
            self.answer_req()
            return

        # print("[dbg] Received {} bytes of data: {}".format(len(data), data))
        if (data == REQ_OPEN):
            print("{} Opening door for [{}] ".format(self.id_string, data))
            self.req_okay = True
        elif (data ==  REQ_CLOSE):
            print("{} Closing door for [{}]".format(self.id_string, data))
            self.req_okay = True
        else:
            print("{} Garbled request, ignoring: [{}]".format(self.id_string, data.decode()))
            self.req_okay = False

        self.answer_req()

    def answer_req(self):
        if (self.req_okay):
            self.client_sock.send(b"Thank you for using our service.")
        else:
            self.client_sock.send(b"Your data is bad and you should feel bad. Bye.")
        self.client_sock.close()
        
def loop():
    mock_door = DoorSocketMock()
    while(True):
        t = mock_door.accept_conn()
loop()