_author_ = 'Srikrishna'

import sys
import time
import zmq
import threading
import uav_pubsub as uav

class MyGCS():
    def __init__(self, tel_port, control_port, uav_instances, verbose):
        self.uav_count = uav_instances
        self.tel_msg_count = 0
        self.control_msg_count = 0
        self.verbose = verbose
        self.running = True
        self.prefix = "[GCS]"

        # Setting up ZMQ related parameters
        self.zmq_tel_port = tel_port
        self.zmq_control_port = control_port
        self.zmq_tel_connection_str = "tcp://127.0.0.1:" + str(self.zmq_tel_port)
        self.zmq_control_connection_str = "tcp://127.0.0.1:" + str(self.zmq_control_port)
        self.zmq_tel_socket = self.create_zmq("SUB", self.zmq_tel_connection_str, "", verbose=self.verbose)
        self.zmq_control_socket = self.create_zmq("PUB", self.zmq_control_connection_str, verbose=self.verbose)

        self.flying = 0
        self.arm = 0

    def create_zmq(self, zmq_type, con_string, prefix="", verbose=False):
        context = zmq.Context()
        if "PUB" in zmq_type:
            if verbose:
                print(self.prefix + " [ZMQ] Binding publisher started " + con_string)
            sock_new = context.socket(zmq.PUB)
            sock_new.bind(con_string)
            if verbose:
                print(self.prefix + " [ZMQ] Publisher bound complete " + con_string)
        elif "SUB" in zmq_type:
            if verbose:
                print(self.prefix + " [ZMQ] Subscriber connect started " + con_string)
            sock_new = context.socket(zmq.SUB)
            sock_new.connect(con_string)
            sock_new.setsockopt(zmq.SUBSCRIBE, prefix)
            if verbose:
                print(self.prefix + " [ZMQ] Subscriber connect complete " + con_string)
        else:
            return None
        return sock_new

    def connection_close(self):
        if self.verbose:
            print(self.prefix + " Closing the connections")
        print(self.prefix + " From destructor")
        self.send_data("TERMINATE", "000", self.zmq_control_socket, self.verbose)
        self.running = False
        self.zmq_control_socket.close()
        self.zmq_tel_socket.close()

    def connect_uav(self):
        for i in range(self.uav_count):
            self.send_data("COMMAND:CONNECT", format(i, "03d"), self.zmq_control_socket, self.verbose)

    def arm_disarm_throttle(self):
        if not self.arm:
            cmd = "COMMAND:ARM"
            for i in range(self.uav_count):
                self.send_data(cmd, format(i, "03d"), self.zmq_control_socket, self.verbose)
            self.arm = 1

        elif self.arm:
            cmd = "COMMAND:DISARM"
            for i in range(self.uav_count):
                self.send_data(cmd, format(i, "03d"), self.zmq_control_socket, self.verbose)
            self.arm = 0

    def takeoff(self):
        if self.arm:
            alt = 10
            speed = 5
            mode = "LOITER"
            cmd = "COMMAND:TAKEOFF|ALT=" + str(alt) + "|MODE=" + str(mode) + "|SPEED=" + str(speed)
            for i in range(self.uav_count):
                self.send_data(cmd, format(i, "03d"), self.zmq_control_socket, self.verbose)
            self.flying = 1

    def land(self):
        if self.flying:
            cmd = "COMMAND:LAND"
            for i in range(self.uav_count):
                self.send_data(cmd, format(i, "03d"), self.zmq_control_socket, self.verbose)
            self.send_data(cmd, "000", self.zmq_control_socket, self.verbose)
            self.flying = 0

    def rtl(self):
        if self.flying:
            cmd = "COMMAND:RTL"
            for i in range(self.uav_count):
                self.send_data(cmd, format(i, "03d"), self.zmq_control_socket, self.verbose)

    def go_to(self):
        if self.flying:
            x = self.tb_goto_x.text()
            y = self.tb_goto_y.text()
            self.lbl_status.setText("Goto: X=" + str(x) + " Y=" +str(y))
            cmd = "COMMAND:GOTO|X=" + str(x) + "|Y=" + str(y)
            print(cmd)
            self.send_data(cmd, "000", self.zmq_control_socket, self.verbose)

    def go_up(self):
        if self.flying:
            cmd = "COMMAND:GO_UP"
            for i in range(self.uav_count):
                self.send_data(cmd, format(i, "03d"), self.zmq_control_socket, self.verbose)

    def go_down(self):
        if self.flying:
            cmd = "COMMAND:GO_DOWN"
            for i in range(self.uav_count):
                self.send_data(cmd, format(i, "03d"), self.zmq_control_socket, self.verbose)

    def go_left(self):
        if self.flying:
            cmd = "COMMAND:GO_LEFT"
            for i in range(self.uav_count):
                self.send_data(cmd, format(i, "03d"), self.zmq_control_socket, self.verbose)

    def go_right(self):
        if self.flying:
            cmd = "COMMAND:GO_RIGHT"
            for i in range(self.uav_count):
                self.send_data(cmd, format(i, "03d"), self.zmq_control_socket, self.verbose)

    def go_forward(self):
        if self.flying:
            cmd = "COMMAND:GO_FORWARD"
            for i in range(self.uav_count):
                self.send_data(cmd, format(i, "03d"), self.zmq_control_socket, self.verbose)

    def go_backward(self):
        if self.flying:
            cmd = "COMMAND:GO_BACKWARD"
            for i in range(self.uav_count):
                self.send_data(cmd, format(i, "03d"), self.zmq_control_socket, self.verbose)

    def send_data(self, message, uav_id, sock, verbose):
        try:
            self.control_msg_count += 1
            msg_send = "@@@G_" + uav_id + "***" + str(self.control_msg_count) + "***" + \
                       repr(time.time()) + "***" + message + "***"
                       #str(time.time()) + "***" + message + "***"
            if verbose:
                print(self.prefix + " CONTROL: sending " + msg_send)
            sock.send(msg_send)
        except:
            print(self.prefix + " CONTROL: Exception occurred while sending data")




GCS_instance = MyGCS(5501, 5500, 1 , True)


def print_menu():  ## Your menu design here
    print 30 * "-", "MENU", 30 * "-"
    print "1. Connect UAV"
    print "2. ARM/DISARM"
    print "3. TAKEOFF"
    print "4. GOTO"
    print "5. LAND"
    print "6. Exit"
    print 67 * "-"

loop = True


while loop:  ## While loop which will keep going until loop = False
    print_menu()  ## Displays menu
    choice = input("Enter your choice [1-6]: ")

    if choice == 1:
        print "Connect UAV"
        GCS_instance.connect_uav()
        ## You can add your code or functions here
    elif choice == 2:
        print "ARM/DISARM"
        GCS_instance.arm_disarm_throttle()
        ## You can add your code or functions here
    elif choice == 3:
        print "TAKEOFF"
        #GCS_instance.takeoff()
        ## You can add your code or functions here
    elif choice == 4:
        print "GOTO"
        #GCS_instance.go_to()
        ## You can add your code or functions here
    elif choice == 5:
        print "LAND"
        ## You can add your code or functions here
    elif choice == 6:
        print "Exit"
        ## You can add your code or functions here
        loop = False  # This will make the while loop to end as not value of loop is set to False
    else:
        # Any integer inputs other than values 1-5 we print an error message
        raw_input("Wrong option selection. Enter any key to try again..")


