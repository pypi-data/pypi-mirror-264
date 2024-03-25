# coding = utf-8
#!/usr/bin/env python

# ------------------------------ Helper functions ---------------------------------
# Description: Some useful functions used in NEP core
# --------------------------------------------------------------------------
# You are free to use, change, or redistribute the code in any way you wish
# but please maintain the name of the original author.
# This code comes with no warranty of any kind.
# Autor: Luis Enrique Coronado Zuniga


from os import listdir
from os.path import isfile, join
import simplejson
import nep
import time
import sys, os
from subprocess import Popen, call
import zmq

def logError(e):
    exc_type, exc_obj, exc_tb = sys.exc_info()
    fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
    print(exc_type, fname, exc_tb.tb_lineno)

def printError(e):
    try:
        print ("NEP ERROR:: "  + str(e))
    except:
        pass

def masterRegister(node, topic, master_ip='127.0.0.1', master_port=50000, socket="subscriber", mode="many2many", pid="none", data_type="json"):
    """
    Register a node with the master.

    Args:
        node (str): The name of the node.
        topic (str): The topic to register for.
        master_ip (str, optional): The IP address of the master. Defaults to '127.0.0.1'.
        master_port (int, optional): The port of the master. Defaults to 50000.
        socket (str, optional): The socket type. Defaults to "subscriber".
        mode (str, optional): The communication mode. Defaults to "many2many".
        pid (str, optional): The process ID. Defaults to "none".
        data_type (str, optional): The message data type. Defaults to "json".

    Returns:
        tuple: A tuple containing three elements:
            - success (bool): True if the registration was successful, False otherwise.
            - port (int or str): The port number or "none" if unsuccessful.
            - ip (str): The IP address or "none" if unsuccessful.
    """
    
    try:
        topic = topic
        client = nep.client(master_ip, master_port, transport="ZMQ", debug=False)
        time.sleep(.01)
        message = {
            'node': node,
            'topic': topic,
            'mode': mode,
            'socket': socket,
            'pid': pid,
            'msg_type': data_type
        }

        client.send_info(message)

        # Create un poller
        poller = zmq.Poller()
        poller.register(client.sock, zmq.POLLIN)

        while True:
            try:
                # Wait 2 second
                socks = dict(poller.poll(2000))

                if socks.get(client.sock) == zmq.POLLIN:
                    response = client.listen_info()
                    try:
                        topic_id = response['topic']

                        if(topic_id == topic):
                            port = response['port']
                            if "ip" in response:
                                ip = response['ip']
                            else:
                                ip = '127.0.0.1'
                            state = response['state']
                            if state == "success":
                                return True, port, ip
                            else:
                                print("NEP ERROR:: wrong socket configuration")
                                return False, port, ip
                    except Exception as e:
                        exc_type, exc_obj, exc_tb = sys.exc_info()
                        fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
                        print(exc_type, fname, exc_tb.tb_lineno)
                        print("NEP ERROR:: wrong response from master")
                        return False, "none", "none"
                else:
                    print("NEP Timeout: No response received within 2 seconds of NEP master")
            except KeyboardInterrupt:
                print("Interrupted by user")
                break
    except Exception as e:
        logError(e)


def json2dict(s, **kwargs):
    """Convert JSON to python dictionary. See jsonapi.jsonmod.loads for details on kwargs.
     
        Parameters
        ----------
        s: string
            string with the content of the json data

        Returns:
        ----------
        dict: dictionary
            dictionary with the content of the json data
    """

    if sys.version_info[0] == 3:
        return simplejson.loads(s, **kwargs)

    else:
        if str is unicode and isinstance(s, bytes):
            s = s.decode('utf8')
    
    return simplejson.loads(s, **kwargs)

def dict2json(o, **kwargs ):
    """ Load object from JSON bytes (utf-8). See jsonapi.jsonmod.dumps for details on kwargs.
     
        Parameters
        ----------
        o: dictionary
            dictionary to convert
            

        Returns:
        ----------
        s: string
            string in json format

    """
        
    if 'separators' not in kwargs:
        kwargs['separators'] = (',', ':')
        
    s = simplejson.dumps(o, **kwargs)

    import sys
    if sys.version_info[0] == 3:
        if isinstance(s, str):
            s = s.encode('utf8')

    else:
        if isinstance(s, unicode):
            s = s.encode('utf8')
        
    return s

def read_json(json_file):
    """ Read a json file and return a string 
        
        Parameters
        ----------
        json file:string
            Path +  name + extension of the json file

        Returns:
        ----------
        json_data: string
            string with the content of the json data

    """
    json_data = open (json_file).read()
    return json_data

