# coding = utf-8
#!/usr/bin/env python

# ------------------------------ Subscriber --------------------------------
# Description: Low-level Subscriber Class
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
    import warnings
    warnings.filterwarnings("ignore", category=UserWarning, module="numpy")   
    import numpy as np
except ImportError:
    pass


try:
    import cv2
except ImportError:
    pass

class subscriber:
    """
    Subscriber class used for inter-process communication between nodes. 

    Parameters
    ----------
    topic : str
        The topic name to publish the messages.

    node : NEP node
        The name of the node

    msg_type : str
        Message type

    conf : dict
        Configuration of the subscriber.

    debug : bool
        If True, additional information about the subscriber is shown.

        
    Notes
    -----
    This class represents a subscriber for receiving messages from publishers. It supports multiple message types.

    Supported message types:
        - 'msgpack', 'bytes', 'images', 'json': Subscribe to all messages (no message filtering).
        - 'dictionary': Subscribe to messages with a specific topic prefix.

    """
    def __init__(self, topic, node = "default", msg_type = "json", conf =  {'transport': "ZMQ", 'network': "broker", 'mode':"many2many", "master_ip":"127.0.0.1"}, debug = False):

        self.topic = topic
        self.node = node
        self.conf = conf
        self.network = self.conf['network']
        self.transport =  self.conf['transport']
        self.msg_type = msg_type
        self.ip = ""
        self.port = ""
        self.debug = debug

        self.master_ip = "127.0.0.1"

        try:
            self.master_ip = conf["master_ip"]
            if self.master_ip == "127.0.0.1":
                print ("NEP SUB:: " + topic + " in local-host") if self.debug and self.topic != "/nep_node" and not self.topic.startswith("/nepplus") else None
            else:
                print ("NEP SUB:: " + topic + " in " +  str(self.master_ip)) if self.debug and self.topic != "/nep_node" and not self.topic.startswith("/nepplus") else None
        except:
            pass


        if self.transport ==  "ZMQ":                                      #Use ZeroMQ
            if self.topic != "/nep_node":
                print ("NEP SUB:: " + topic + ", using ZMQ " + self.network) if self.debug and self.topic != "/nep_node" and not self.topic.startswith("/nepplus") else None
            self.mode = "many2many" #many2many is the default value
            if "mode" in self.conf:
                self.mode = self.conf['mode']
            self.__create_ZMQ_subscriber()

        

    def __network_selection(self):
        """
        Determine the IP address and port for socket connection.

        Returns
        ----------
        success : bool
            Indicates whether the socket configuration was successful.
            - True: The socket can be successfully connected.
            - False: An error occurred during socket configuration.

        port : str
            The port used for socket connection.

        ip : str
            The IP address used for socket connection.

        Notes
        -----
        This method determines the IP address and port for socket connection based on the chosen network configuration.

        Supported network configurations:
        - 'direct': User-configured IP and port values are used.
        - 'broker': The method registers with the NEP Master and obtains the port and IP address.

        If the network configuration is 'direct', the user-configured IP and port are used. If it is 'broker',
        the method interacts with the NEP Master to obtain the necessary connection information.

        Exceptions:
        - If an error occurs during socket configuration, the method returns False for success.

        See Also
        --------
        - Use this method to determine the IP address and port for socket connection based on the chosen network configuration.
        """
        success = False
        ip = "127.0.0.1"
        port = "50000"
        self.pid = os.getpid()
        if self.network == "direct":
            # Set the port and ip selected by the user
            port = self.conf["port"]
            ip = self.conf['ip']
            success =  True
        elif self.network == "broker":
            print("NEP SUB:: " + self.topic + " waiting NEP master in " + self.master_ip) if self.debug and self.topic != "/nep_node" and not self.topic.startswith("/nepplus") else None
            # Register the topic in the NEP Master and get the port and ip
            success, port, ip  = nep.masterRegister(self.node, self.topic, master_ip = self.master_ip, master_port = 50000, socket = "subscriber", mode = self.mode, pid = self.pid, data_type = self.msg_type)
            print("NEP SUB:: " + self.topic + " socket ready")  if self.debug and self.topic != "/nep_node" and not self.topic.startswith("/nepplus") else None
        return success, port, ip


    def __create_ZMQ_subscriber(self):
        """
        Create a ZeroMQ subscriber socket.

        Returns
        -------
        success : bool
            Indicates whether the socket creation and configuration were successful.
            - True: The subscriber socket was successfully created and configured.
            - False: An error occurred during socket creation or configuration.

        Notes
        -----
        This method creates a ZeroMQ subscriber socket and configures it based on the specified message type.

        Supported message types:
        - 'msgpack', 'bytes', 'json', 'images': Subscribe to all messages (no message filtering).
        - 'dictionary': Subscribe to messages with a specific topic prefix.

        Performance Note:
        - Setting zmq.CONFLATE to 1 keeps only the last message in the queue for improved performance.

        Exceptions:
        - If an error occurs during socket creation or configuration, the method prints an error message
          and returns False for success.

        See Also
        --------
        - Use this method to create and configure a ZeroMQ subscriber socket for message reception.
        """
        success, self.port, self.ip = self.__network_selection()
        if success:
            try:
                # ZeroMQ Context
                self.context = zmq.Context()
                # Define the type of context, in this case, a subscriber
                self.sock = self.context.socket(zmq.SUB)
                if self.msg_type == "image":
                        print("NEP Warning: type *image* is deprecated; please use *images* to improve performance")
                if self.msg_type in ["msgpack", "string", "bytes", "images", "json"]:
                    self.sock.setsockopt(zmq.SUBSCRIBE, b"")
                    self.sock.setsockopt(zmq.CONFLATE, 1)  # Only keeps last message in queue
                elif self.msg_type in ["dictionary"]:
                    if sys.version_info[0] == 2:
                        self.sock.setsockopt(zmq.SUBSCRIBE, self.topic)
                        self.sock.setsockopt(zmq.CONFLATE, 1)  # Only keeps last message in queue
                    else:
                        self.sock.setsockopt_string(zmq.SUBSCRIBE, self.topic)
                        self.sock.setsockopt(zmq.CONFLATE, 1)
                else:
                    print("NEP ERROR:: Message Type *" + self.msg_type + "* not supported")

                self.__connect_ZMQ_socket()
                return True
            except zmq.error.ZMQError as e:
                print("NEP ERROR:: Socket already in use" if e.errno == zmq.EADDRINUSE else "NEP ERROR:: Socket creation/configuration error")
        else:
            print("NEP ERROR:: Socket unable to be connected")
        return False


    def __connect_ZMQ_socket(self):
        """ Connect ZMQ socket in base it configuration
        """

        if self.mode == "many2one":
            endpoint = "tcp://" + self.ip + ":" + str(self.port)
            self.sock.bind(endpoint)
            print("NEP SUB:: " + self.topic + " endpoint " + endpoint +  " bind") if self.debug and self.topic != "/nep_node" and not self.topic.startswith("/nepplus") else None
        elif self.mode == "one2many":

            endpoint = "tcp://" + self.ip + ":" + str(self.port)
            self.sock.connect(endpoint)
            print("NEP SUB:: " + self.topic + " endpoint " + endpoint +  " connect") if self.debug and self.topic != "/nep_node" and not self.topic.startswith("/nepplus") else None

        elif self.mode == "many2many":
            endpoint = "tcp://" +  self.master_ip + ":" + str( self.port+1)
            self.sock.connect(endpoint)

        else:
            msg = "NEP ERROR:: mode value " +  self.mode + "is not valid"
            raise ValueError(msg)

    def close_ZMQ_subscriber(self):
        """ This function closes the socket"""
        self.sock.close()
        self.context.destroy()
        time.sleep(1)


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


    def __loads(self, s, **kwargs):
        """Load object from JSON bytes (utf-8). See jsonapi.jsonmod.loads for details on kwargs.
        """
        if sys.version_info[0] == 2:
            if str is unicode and isinstance(s, bytes):
                s = s.decode('utf8')
        return simplejson.loads(s, **kwargs)


    def __JSONdecoding(self, info):
        """
        Extract the topic and JSON message from the data received from the ZeroMQ socket.

        Parameters
        ----------
        info : str
            The complete message received from the ZeroMQ socket, including both the topic and JSON message.

        Returns
        -------
        success : bool
            Indicates whether the message separation and deserialization were successful.
            - True: Data was successfully separated and deserialized as a Python dictionary.
            - False: An exception occurred, or the message is not JSON serializable.

        message : dict
            The JSON message, deserialized as a Python dictionary.
            An empty dictionary if no message is successfully extracted or deserialized.

        Notes
        -----
        This method separates the topic and the JSON message from the received data, which is in the format
        of 'topic + JSON message'. It then attempts to deserialize the JSON message into a Python dictionary.

        Exceptions:
        - If the data cannot be separated or the deserialization fails, the method prints an error message
          and returns False for success and an empty dictionary.
        - If the data is successfully separated and deserialized, it returns True for success and the
          deserialized message as a Python dictionary.

        See Also
        --------
        - Use this method for extracting and deserializing JSON messages from the received data.
        """
        try:
            # Find the start of the JSON message
            json_start = info.find('{')
            # Extract the topic (before the JSON message)
            topic = info[:json_start].strip()
            # Extract and deserialize the JSON message
            message = self.__loads(info[json_start:])
            success = True
        except Exception as e:
            print("NEP Serialization Error:\n" + str(info) + "\n" + "Is not JSON serializable")
            message = {}
            success = False
        return success, message
    
    

    def listen(self, block_mode=False):
        """ 
        Listen for data from publishers and decode it based on the specified message type.

        Parameters
        ----------
        block_mode : bool, optional
            If True, the function will block until data is received; if False (default),
            it will return None immediately if no data is available.

        Returns
        -------
        message : string or dict
            The decoded message, which matches the specified message type (msg_type).

        Raises
        ------
        ValueError
            If an unsupported msg_type is selected.

        Notes
        -----
        This function listens for data from publishers and decodes it based on the
        specified message type (msg_type). Supported message types include:
    
        - "string": Decodes data as a string.
        - "msgpack": Decodes data using the MessagePack format.
        - "json": Decodes data as a JSON object.
        - "image": Decodes data as a OpenCV image.
        - "dictionary": Decodes data as a JSON object with a specific topic prefix.

        It raises a ValueError if an unsupported message type is selected.
        """
        msg_type_functions = {
            "msgpack": self.listenMsgPack,
            "bytes": self.listenBytes,
            "json": self.listenJson,
            "string": self.listenString,
            "images": self.listenImages,
            "dictionary": self.listenDictionary,
        }

        # Check if the msg_type is supported, and if so, call the corresponding function
        if self.msg_type in msg_type_functions:
            return msg_type_functions[self.msg_type](block_mode)
        else:
            msg = "Unsupported msg_type selected: '%s'" % self.msg_type
            raise ValueError(msg)


            
    def read(self, block_mode =  False):
        """
        Receive raw byte data from the socket.

        Parameters
        ----------
        block_mode : bool, optional
            If True, the function operates in blocking mode, waiting for data to arrive.
            If False (default), the function operates in non-blocking mode, returning immediately
            if no data is available.

        Returns
        -------
        success : bool
            Indicates whether the data retrieval was successful.
            - True: Data was obtained within the specified timeline in non-blocking mode.
            - False: No data was obtained or an exception occurred.

        msg : bytes
            The raw byte data obtained from the socket. Empty bytes if no data is received or
            an exception occurs.

        Notes
        -----
        This function reads raw byte data from the socket and provides options for both
        blocking and non-blocking operation.

        - In blocking mode (block_mode=True), the function will wait for data to arrive, blocking
          the program's execution until data is received or an exception occurs.
        - In non-blocking mode (block_mode=False), the function will return immediately if no
          data is available, allowing the program to continue execution.

        Exceptions:
        - If `block_mode` is set to False and no data is available, the function returns False
          for success, and the message will be empty bytes.
        - If a timeout occurs in non-blocking mode, the function returns False for success, and
          the message will be empty bytes.

        See Also
        --------
        - Use this function for receiving raw byte data from the socket.
        """
         
        success = False
        try:
            #Blocking mode
            if block_mode:
                info = self.sock.recv()
                return  True, info
            #Non blocking mode
            else:
                if self.transport ==  "ZMQ":
                    info = self.sock.recv(flags = zmq.NOBLOCK)
                    return True, info
        #Exeption for non blocking mode timeout
        except zmq.Again as e:
            #Nothing to read
            success = False
            pass

        return  success, ""


    def listenBytes(self, block_mode=False):
        """
        Listen for a Bytes-encoded message from the socket.

        Parameters
        ----------
        block_mode : bool, optional
            If True, the function operates in blocking mode, waiting for data to arrive.
            If False (default), the function operates in non-blocking mode, returning immediately
            if no data is available.

        Returns
        -------
        success : bool
            Indicates whether the message retrieval and deserialization were successful.
            - True: Data was obtained and deserialized within the specified timeline in non-blocking mode.
            - False: No data was obtained, an exception occurred

        message : bytes
            The decoded Bytes message obtained from the socket. An empty value if no
            message is received

        Notes
        -----
        This function listens for a MessagePack-encoded message from the socket and provides options
        for both blocking and non-blocking operation.

        - In blocking mode (block_mode=True), the function will wait for data to arrive, blocking
          the program's execution until data is received or an exception occurs.
        - In non-blocking mode (block_mode=False), the function will return immediately if no
          data is available, allowing the program to continue execution.

        The function attempts to deserialize the received data as MessagePack. If successful,
        it returns the deserialized message; otherwise, it returns an empty dictionary.

        Exceptions:
        - If `block_mode` is set to False and no data is available, the function returns False
          for success, and the message will be an empty dictionary.
        - If a timeout occurs in non-blocking mode, the function returns False for success, and
          the message will be an empty dictionary.


        See Also
        --------
        - Use this function for receiving and deserializing MessagePack-encoded messages from the socket.
        """
        success = False
        message = {}
        try:
            success, info = self.read(block_mode)
            if success:
                try:
                    return success, info
                except Exception as e:
                    print("NEP Serialization Error:\n" + str(info) + "\n" + "Bytes error")
                    return success, ""
        # Exception for non-blocking mode timeout
        except zmq.Again as e:
            # Nothing to read
            success = False
            pass

        return success, message

    def listenMsgPack(self, block_mode=False):
        """
        Listen for a MessagePack-encoded message from the socket.

        Parameters
        ----------
        block_mode : bool, optional
            If True, the function operates in blocking mode, waiting for data to arrive.
            If False (default), the function operates in non-blocking mode, returning immediately
            if no data is available.

        Returns
        -------
        success : bool
            Indicates whether the message retrieval and deserialization were successful.
            - True: Data was obtained and deserialized within the specified timeline in non-blocking mode.
            - False: No data was obtained, an exception occurred, or the data was not MSGPACK serializable.

        message : dict
            The decoded MessagePack message obtained from the socket. An empty dictionary if no
            message is received, an exception occurs, or the data is not MSGPACK serializable.

        Notes
        -----
        This function listens for a MessagePack-encoded message from the socket and provides options
        for both blocking and non-blocking operation.

        - In blocking mode (block_mode=True), the function will wait for data to arrive, blocking
          the program's execution until data is received or an exception occurs.
        - In non-blocking mode (block_mode=False), the function will return immediately if no
          data is available, allowing the program to continue execution.

        The function attempts to deserialize the received data as MessagePack. If successful,
        it returns the deserialized message; otherwise, it returns an empty dictionary.

        Exceptions:
        - If `block_mode` is set to False and no data is available, the function returns False
          for success, and the message will be an empty dictionary.
        - If a timeout occurs in non-blocking mode, the function returns False for success, and
          the message will be an empty dictionary.
        - If the received data is not MSGPACK serializable, the function prints an error message
          and returns False for success and an empty dictionary.

        See Also
        --------
        - Use this function for receiving and deserializing MessagePack-encoded messages from the socket.
        """
        success = False
        message = {}
        try:
            success, info = self.read(block_mode)
            if success:
                try:
                    msg = msgpack.unpackb(info, raw=False)
                    return success, msg
                except Exception as e:
                    print("NEP Serialization Error:\n" + str(info) + "\n" + "Is not MSGPACK serializable")
                    return success, {}
        # Exception for non-blocking mode timeout
        except zmq.Again as e:
            # Nothing to read
            success = False
            pass

        return success, message

    def listenImages(self, block_mode = False):
        """
        Receive and decode an image message from the socket.

        Parameters
        ----------
        block_mode : bool, optional
            If True, the function operates in blocking mode, waiting for data to arrive.
            If False (default), the function operates in non-blocking mode, returning immediately
            if no data is available.

        Returns
        -------
        success : bool
            Indicates whether the image retrieval was successful.
            - True: Data was obtained within the specified timeline in non-blocking mode.
            - False: No data was obtained or an exception occurred.

        image : numpy.ndarray
            The decoded image obtained from the socket using OpenCV (cv2).
            If no image data is received or an exception occurs, this will be None.

        Notes
        -----
        This function reads an image message from the socket and provides options for both
        blocking and non-blocking operation.

        - In blocking mode (block_mode=True), the function will wait for data to arrive, blocking
          the program's execution until image data is received or an exception occurs.
        - In non-blocking mode (block_mode=False), the function will return immediately if no
          data is available, allowing the program to continue execution.

        The received image data is decoded from base64 and converted into a NumPy array using
        OpenCV (cv2). The resulting image is returned.

        Exceptions:
        - If `block_mode` is set to False and no data is available, the function returns False
          for success, and the image will be None.
        - If a timeout occurs in non-blocking mode, the function returns False for success, and
          the image will be None.

        See Also
        --------
        - Use this function for receiving and decoding image messages from the socket.
        """

        s, imageraw = self.read(block_mode)
        if s:
            jpg = base64.b64decode(imageraw)
            jpg = np.frombuffer(jpg, dtype=np.uint8)
            img = cv2.imdecode(jpg, 1)
            return s, img
        return s, imageraw

    def listenString(self, block_mode = False):
        """
        Receive and decode a string message from the socket.

        Parameters
        ----------
        block_mode : bool, optional
            If True, the function operates in blocking mode, waiting for data to arrive.
            If False (default), the function operates in non-blocking mode, returning immediately
            if no data is available.

        Returns
        -------
        success : bool
            Indicates whether the message retrieval was successful.
            - True: Data was obtained within the specified timeline in non-blocking mode.
            - False: No data was obtained or an exception occurred.

        message : str
            The string message obtained from the socket. Empty if no message is received or
            an exception occurs.

        Notes
        -----
        This function reads a string message from the socket and provides options for both
        blocking and non-blocking operation.

        - In blocking mode (block_mode=True), the function will wait for data to arrive, blocking
          the program's execution until data is received or an exception occurs.
        - In non-blocking mode (block_mode=False), the function will return immediately if no
          data is available, allowing the program to continue execution.

        The received message is split into a topic and a message payload based on the first space
        character (' ') encountered. The topic and message payload are then returned.

        Exceptions:
        - If `block_mode` is set to False and no data is available, the function returns False
          for success, and the message will be an empty string.
        - If a timeout occurs in non-blocking mode, the function returns False for success, and
          the message will be an empty string.

        See Also
        --------
        - Use this function for receiving and decoding string messages from the socket.
        """

        message = ""
        try:
            #Blocking mode
            if block_mode:
                # Get the message
                if sys.version_info[0] == 2:
                    info = self.sock.recv()
                else:
                    message = self.sock.recv_string()
                # Split the message
                success = True
            #Non blocking mode
            else:          
                if sys.version_info[0] == 2:
                    info = self.sock.recv(flags = zmq.NOBLOCK)
                else:
                    message = self.sock.recv_string(flags = zmq.NOBLOCK)

                success = True
        #Exeption for non blocking mode timeout
        except zmq.Again as e:
            #Nothing to read
            success = False
            pass


        return  success, message
    
    def listenStringTopic(self, block_mode = False):
        """
        Receive and decode a string message from the socket. When a message is received, the topic is separated from the message.

        Parameters
        ----------
        block_mode : bool, optional
            If True, the function operates in blocking mode, waiting for data to arrive.
            If False (default), the function operates in non-blocking mode, returning immediately
            if no data is available.

        Returns
        -------
        success : bool
            Indicates whether the message retrieval was successful.
            - True: Data was obtained within the specified timeline in non-blocking mode.
            - False: No data was obtained or an exception occurred.

        message : str
            The string message obtained from the socket. Empty if no message is received or
            an exception occurs.

        Notes
        -----
        This function reads a string message from the socket and provides options for both
        blocking and non-blocking operation.

        - In blocking mode (block_mode=True), the function will wait for data to arrive, blocking
          the program's execution until data is received or an exception occurs.
        - In non-blocking mode (block_mode=False), the function will return immediately if no
          data is available, allowing the program to continue execution.

        The received message is split into a topic and a message payload based on the first space
        character (' ') encountered. The topic and message payload are then returned.

        Exceptions:
        - If `block_mode` is set to False and no data is available, the function returns False
          for success, and the message will be an empty string.
        - If a timeout occurs in non-blocking mode, the function returns False for success, and
          the message will be an empty string.

        See Also
        --------
        - Use this function for receiving and decoding string messages from the socket.
        """

        message = ""
        try:
            #Blocking mode
            if block_mode:
                # Get the message
                if sys.version_info[0] == 2:
                    info = self.sock.recv()
                else:
                    info = self.sock.recv_string()
                # Split the message

                topic, message = info.split(' ', 1)
                success = True
            #Non blocking mode
            else:          
                if sys.version_info[0] == 2:
                    info = self.sock.recv(flags = zmq.NOBLOCK)
                else:
                    info = self.sock.recv_string(flags = zmq.NOBLOCK)
                      
                # Split the message
                topic, message = info.split(' ', 1)

                success = True
        #Exeption for non blocking mode timeout
        except zmq.Again as e:
            #Nothing to read
            success = False
            pass


        return  success, message
    
    def listenDictionary(self, block_mode =  False):
        """
        Listen for a JSON-encoded message. When a message is received, the topic is separated from the message.

        Parameters
        ----------
        block_mode : bool, optional
            If True, the function operates in blocking mode, waiting for data to arrive.
            If False (default), the function operates in non-blocking mode, returning immediately
            if no data is available.

        Returns
        -------
        success : bool
            Indicates whether the message retrieval was successful.
            - True: Data was obtained within the specified timeline in non-blocking mode.
            - False: No data was obtained or an exception occurred.

        info : dict
            The decoded JSON message obtained from the stream, if successful.
            If no data was received or an exception occurred, this will be an empty dictionary.

        Notes
        -----
        This function listens for a JSON-encoded message from a socket. It can operate
        in either blocking or non-blocking mode, depending on the value of `block_mode`.

        - In blocking mode (block_mode=True), the function will wait for data to arrive, blocking
          the program's execution until data is received or an exception occurs.
        - In non-blocking mode (block_mode=False), the function will return immediately if no
          data is available, allowing the program to continue execution.

        Exceptions:
        - If `block_mode` is set to False and no data is available, the function returns False
          for success, and the info dictionary will be empty.
        - If a timeout occurs in non-blocking mode, the function returns False for success, and
          the info dictionary will be empty.

        Compatibility:
        - The function handles Python 2 and Python 3 differently for JSON decoding based on the
          version of Python being used.

        See Also
        --------
        - Use this function for JSON-encoded data. For other message types, consider using the
          corresponding listen functions.
        """
         
        success = False
        info = {}
        try:
            #Blocking mode
            if block_mode:
                if sys.version_info[0] == 2:
                    success, info = self.__JSONdecoding(self.sock.recv())
                else:
                    success,info = self.__JSONdecoding(self.sock.recv_string())

                #time.sleep(.001)
            #Non blocking mode
            else:

                if sys.version_info[0] == 2:
                    success, info = self.__JSONdecoding(self.sock.recv(flags = zmq.NOBLOCK))
                else:
                    success,info = self.__JSONdecoding(self.sock.recv_string(flags = zmq.NOBLOCK))


                #time.sleep(.001)
        #Exeption for non blocking mode timeout
        except zmq.Again as e:
            #Nothing to read
            success = False
            pass


        return  success, info
    
    def listenJson(self, block_mode =  False):
        """
        Listen for a JSON-encoded message.

        Parameters
        ----------
        block_mode : bool, optional
            If True, the function operates in blocking mode, waiting for data to arrive.
            If False (default), the function operates in non-blocking mode, returning immediately
            if no data is available.

        Returns
        -------
        success : bool
            Indicates whether the message retrieval was successful.
            - True: Data was obtained within the specified timeline in non-blocking mode.
            - False: No data was obtained or an exception occurred.

        info : dict
            The decoded JSON message obtained from the stream, if successful.
            If no data was received or an exception occurred, this will be an empty dictionary.

        Notes
        -----
        This function listens for a JSON-encoded message from a socket. It can operate
        in either blocking or non-blocking mode, depending on the value of `block_mode`.

        - In blocking mode (block_mode=True), the function will wait for data to arrive, blocking
          the program's execution until data is received or an exception occurs.
        - In non-blocking mode (block_mode=False), the function will return immediately if no
          data is available, allowing the program to continue execution.

        Exceptions:
        - If `block_mode` is set to False and no data is available, the function returns False
          for success, and the info dictionary will be empty.
        - If a timeout occurs in non-blocking mode, the function returns False for success, and
          the info dictionary will be empty.

        Compatibility:
        - The function handles Python 2 and Python 3 differently for JSON decoding based on the
          version of Python being used.

        See Also
        --------
        - Use this function for JSON-encoded data. For other message types, consider using the
          corresponding listen functions.
        """
         
        success = False
        message = {}
        try:
            #Blocking mode
            if block_mode:
                message = self.sock.recv_json()
                success = True
                #time.sleep(.001)
            #Non blocking mode
            else:
                message = self.sock.recv_json(flags = zmq.NOBLOCK)
                success = True
                #time.sleep(.001)
        #Exeption for non blocking mode timeout
        except zmq.Again as e:
            #Nothing to read
            success = False
            pass

        return  success, message


if __name__ == "__main__":
    import doctest
    doctest.testmod()
