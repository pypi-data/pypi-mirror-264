# coding = utf-8
#!/usr/bin/env python

# ------------------------------ Publisher ---------------------------------
# Description: Low-level Publisher Class
# --------------------------------------------------------------------------
# You are free to use, change, or redistribute the code in any way you wish
# but please maintain the name of the original author.
# This code comes with no warranty of any kind.
# Autor: Luis Enrique Coronado Zuniga


import time
import os
import zmq
import simplejson
import sys
import nep
import base64
import msgpack


try:
    import cv2
except ImportError:
    pass



class publisher:
    """ 
    The Publisher class is used for inter-process communication between nodes. It supports ZeroMQ publishers. 

    Parameters
    ----------
    topic : str
        The topic name to which the messages are published.

    node : str, optional
        The name of the node, by default "default".

    msg_type : str, optional
        The type of the message, by default "json".

    conf : dict, optional
        The configuration of the publisher, by default {'transport': "ZMQ", 'network': "broker", 'mode':"many2many", "master_ip":"0.0.0.0"}.

    debug: bool, optional
        If True, additional information about the publisher is displayed, by default False.

    Raises
    ------
    ValueError
        If the transport parameter is not supported, a ValueError is raised.

    Notes
    -----
    The Publisher class uses ZeroMQ for inter-process communication. It supports different modes of communication: one-to-many, many-to-one, and many-to-many. The class also provides methods for sending different types of messages, including bytes, MsgPack, strings, JSON, and images.

    The class uses a ZeroMQ context and a publisher socket for communication. The socket is connected based on the network configuration. The class also provides methods for serializing and sending messages.

    The Publisher class also handles errors and exceptions, such as when the socket is already in use or when the message type is not compatible.
    """

    def __init__(self, topic, node = "default", msg_type = "json", conf =  {'transport': "ZMQ", 'network': "broker", 'mode':"many2many", "master_ip":"0.0.0.0"}, debug = False):

        self.conf = conf
        self.network = self.conf['network']
        self.transport =  self.conf['transport']
        self.node = node
        self.topic = topic
        self.msg_type =  msg_type
        self.ip = ""
        self.port = ""
        self.connected = False
        self.debug = debug
        self.master_ip = "0.0.0.0"

        try:
            self.master_ip = conf["master_ip"]
            if self.master_ip == "0.0.0.0":
                print ("NEP PUB:: " + topic + " in local-host")
            else:
                print ("NEP PUB:: " + topic + " in " +  str(self.master_ip))
        except:
            pass


        if self.transport ==  "ZMQ":                                                  #Use ZeroMQ
            print ("NEP PUB:: " + self.topic + " using ZMQ " + self.network)
            #many2many is the default value
            self.mode = "many2many"                                                     
            if "mode" in self.conf:
                self.mode = self.conf['mode']
            # Create a ZMQ socket
            self.__create_ZMQ_publisher()

     
        else:
            msg = "NEP ERROR:: Transport parameter " + self.transport + "is not supported, use instead 'ZMQ' "
            raise ValueError(msg)
     
    def __network_selection(self):
        """ Get IP and port of this socket

        Returns
        ----------

        success : bool
            Only if True socket can be connected

        port : string
            Port used to connect the socket

        ip : string
            IP used to connect the socket
        """
        success = False
        ip = "0.0.0.0"
        port = "8000"
        self.pid = os.getpid()
        if self.network == "direct":
            # Set the port and ip selected by the user
            port = self.conf["port"]
            ip = self.conf['ip']
            success =  True
        elif self.network == "broker":
            if self.topic != "/nep_node":
                print("NEP PUB:: " + self.topic + " waiting NEP master ...")
            # Register the topic in the NEP Master and get the port and ip
            success, port, ip  = nep.masterRegister(self.node, self.topic, master_ip = self.master_ip, master_port = 50000, socket = "publisher", mode = self.mode, pid = self.pid, data_type = self.msg_type)
            if self.topic != "/nep_node":
                print("NEP PUB:: " + self.topic + " socket ready")
                
        return success, port, ip

    def __create_ZMQ_publisher(self):
        """Function used to create a ZeroMQ publisher"""

        success, self.port, self.ip = self.__network_selection()
        if success:    
            # Create a new ZeroMQ context and a publisher socket
            try:
                context = zmq.Context()
                # Define the socket using the "Context"
                self.sock = context.socket(zmq.PUB)
                #Set the topic of the publisher and the end_point
                self.__connect_ZMQ_socket()
                self.connected = True
            except:
                print ("NEP ERROR:: socket already in use")
            
            time.sleep(1)
            #This delay in important, whithout them the comunication is not effective
 
            # ZeroMQ note:
            # There is one more important thing to know about PUB-SUB sockets: 
            # you do not know precisely when a subscriber starts to get messages.
            # Even if you start a subscriber, wait a while, and then start the publisher, 
            # the subscriber will always miss the first messages that the publisher sends. 


            # In Chapter 2 - Sockets and Patterns we'll explain how to synchronize a 
            # publisher and subscribers so that you don't start to publish data until 
            # the subscribers really are connected and ready. There is a simple and 
            # stupid way to delay the publisher, which is to sleep. Don't do this in a
            #  real application, though, because it is extremely fragile as well as
            #  inelegant and slow. Use sleeps to prove to yourself what's happening, 
            # and then wait for 
            # Chapter 2 - Sockets and Patterns to see how to do this right

    def __connect_ZMQ_socket(self):
        """ Connect ZMQ socket in base it configuration
        """
        endpoint = "tcp://" + self.ip + ":" + str(self.port)
        if self.mode == "one2many":
        # This allows only use one publisher connected at the same endpoint
            self.sock.bind(endpoint)
            print("NEP PUB:: " + self.topic + " endpoint: " + endpoint +  " bind") if self.debug and self.topic != "/nep_node" and not self.topic.startswith("/nepplus") else None
        elif self.mode == "many2one":
            # This allows two use more that one publisher ate the same endpoint
            self.sock.connect(endpoint)
            print("NEP PUB:: " + self.topic + " endpoint: " + endpoint +  " connect") if self.debug and self.topic != "/nep_node" and not self.topic.startswith("/nepplus") else None
        elif  self.mode == "many2many":
            endpoint = "tcp://" + self.master_ip + ":" + str(self.port)
            self.sock.connect(endpoint)   

    def __dumps(self,o, **kwargs):
        """Serialize object to JSON bytes (utf-8). See jsonapi.jsonmod.dumps for details on kwargs.

        Returns
        -------
        message : string
            Encoded string 

        """

        if 'separators' not in kwargs:
            kwargs['separators'] = (',', ':')
        
        s = simplejson.dumps(o, **kwargs)
        

        if sys.version_info[0] == 2: #Python 2
            if isinstance(s, unicode):
                s = s.encode('utf8')
        return s
            
    def publish(self, message):
        """ 
        Sends a message to subscribers.

        The type of the message to be sent must match the msg_type attribute of the publisher instance. 
        Depending on the msg_type, the appropriate method is called to send the message.

        Parameters
        ----------
        message : obj 
            The message to be sent. The type of the message must match the msg_type attribute of the publisher instance.
        """

        send_methods = {
            "bytes": self.sendBytes,
            "msgpack": self.sendMsgPack,
            "string": self.sendString,
            "json": self.sendJson,
            "dictionary": self.sendDictionary,
            "images": self.sendImages
        }

        send_method = send_methods.get(self.msg_type)

        if send_method:
            send_method(message)
        else:
            message["type"] = self.msg_type
            self.sendJSON(message)

    def sendBytes(self, message):
        """ 
        Sends a bytes message to subscribers.

        If the publisher instance is not connected, an error message is printed.

        Parameters
        ----------
        message : bytes
            The bytes message to be sent.
        """
        if self.connected:
            self.sock.send(bytes(message))
        else:
            print ("NEP ERROR:: socket not connected")

    def sendMsgPack(self,message):
        """ 
        Sends a MsgPack message to subscribers.

        If the publisher instance is not connected, an error message is printed.

        Parameters
        ----------
        message : obj
            The message to be sent. The message is serialized using MsgPack before being sent.
        """
        if self.connected:
            self.sock.send(msgpack.dumps(message))
        else:
            print ("NEP ERROR:: socket not connected")

    def sendImages(self, message):
        """ 
        Publishes an OpenCV image.

        The image is first encoded as a JPEG image. If the encoding fails, a ValueError is raised. 
        The encoded image is then base64 encoded and sent to subscribers.

        Parameters
        ----------
        message : ndarray
            The image to be sent. The image must be a numpy ndarray.
        """

        ret, jpg = cv2.imencode('.jpg', message)
        if not ret:
            raise ValueError("Failed to encode image")
        
        encoded = base64.b64encode(jpg.tostring())
        self.sock.send(encoded)  
            
    def sendTopicString(self,message):
        """ 
        Publishes a string value. The topic is added to the message.

        If the publisher instance is not connected, an error message is printed.

        Parameters
        ----------
        message : str
            The string to be sent. The topic is prepended to the string before it is sent.
        """
        if self.connected:
            self.sendString(self.topic + ' ' + message)
        
        else:
            print ("NEP ERROR:: socket already in use, message not sent")

    def sendString(self,message):
        """ 
        Publishes a string value.

        If the publisher instance is not connected, an error message is printed.

        Parameters
        ----------
        message : str
            The string to be sent.
        """
        if self.connected:
            if sys.version_info[0] == 2: #Python 2
                self.sock.send(msg)
            else: # Python 3
                self.sock.send_string(message)
        
        else:
            print ("NEP ERROR:: socket already in use, message not sent")

    def sendDictionary(self, message):
        """ 
        Publishes a Python dictionary. Add the topic to the message.

        The dictionary is serialized using JSON format and then published by the socket. The topic is added to the message.

        If the publisher instance is not connected, an error message is printed.

        Parameters
        ----------
        message : dict
            The Python dictionary to be sent. The dictionary is serialized to JSON before being sent.
        """
        if self.connected:            
            msg = self.__dumps(message)
            self.sendTopicString(msg)
        else:
            print ("NEP ERROR:: socket already in use, message not sent")
        
    def sendJson(self, message):
        """ 
        Publishes a Python dictionary. 

        The dictionary is serialized using JSON format and then published by the socket.

        If the publisher instance is not connected, an error message is printed.

        Parameters
        ----------
        message : dict
            The Python dictionary to be sent. The dictionary is serialized to JSON before being sent.
        """
        if self.connected:            
            msg = self.__dumps(message)
            self.sock.send_json(msg)
        else:
            print ("NEP ERROR:: socket already in use, message not sent")
        

if __name__ == "__main__":
    import doctest
    doctest.testmod()
