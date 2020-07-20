_author_ = 'Srikrishna'

import sys
import time
import zmq
import threading
import uav_pubsub as uav

def create_zmq(zmq_type, con_string, prefix="", verbose=False):
    context = zmq.Context()
    if "PUB" in zmq_type:
        if verbose:
            print("[MAIN] [ZMQ] Binding publisher started " + con_string)
        sock_new = context.socket(zmq.PUB)
        sock_new.bind(con_string)
        if verbose:
            print("[MAIN] [ZMQ] Publisher bound complete " + con_string)
    elif "SUB" in zmq_type:
        if verbose:
            print("[MAIN] [ZMQ] Subscriber connect started " + con_string)
        sock_new = context.socket(zmq.SUB)
        sock_new.connect(con_string)
        sock_new.setsockopt(zmq.SUBSCRIBE, prefix)
        if verbose:
            print("[MAIN] [ZMQ] Subscriber connect complete " + con_string + " Prefix " + prefix)
    else:
        return None
    return sock_new


uav_zmq_tel_connection_str = "tcp://127.0.0.1:5600"
uav_zmq_tel_socket = create_zmq("PUB", uav_zmq_tel_connection_str, verbose=True)

uav_zmq_control_connection_str = "tcp://127.0.0.1:5601"  # NS-3
ftr = "@@@G_0"
uav_zmq_control_socket = create_zmq("SUB", uav_zmq_control_connection_str, ftr, True)

uav_thread = threading.Thread(target=uav.UAV, args=(format(0, "03d"), (14550), #(14550)(5760 + i * 10)
                                                            uav_zmq_tel_socket, uav_zmq_control_socket, True))  # DIRECT
uav_obj = []
uav_thread.setName("UAV_1")
uav_thread.deamon = True
uav_thread.start()
uav_obj.append(uav_thread)