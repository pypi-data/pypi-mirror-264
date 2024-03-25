# coding = utf-8
#!/usr/bin/env python

# ------------------------------- Node -------------------------------
# Description: Low-level Node Class
# --------------------------------------------------------------------------
# You are free to use, change, or redistribute the code in any way you wish
# but please maintain the name of the original author.
# This code comes with no warranty of any kind.
# Autor: Luis Enrique Coronado Zuniga

import time
import os
import sys
import signal
import threading
import nep
import atexit



#TODO: bug sending strings there is a space + message in publish-subscriber with ZMQ
#TODO: unregister topic when closed


class node:

    # ----------------------- __signal_handler  ------------------------------
    def __signal_handler(self, signal, frame):
        """ Exit node with Ctrl+C """
        import os
        print('Signal Handler, you pressed Ctrl+C! to close the node')
        if not os.environ.get('OS','') == 'Windows_NT': # Windows
            time.sleep(.5)
            os.system('kill %d' % os.getpid())
            sys.exit(0)
        else:
            """Signal handler used to close when user press Ctrl+C"""
            time.sleep(.5)
            import os
            pid = os.getpid()
            import subprocess as s
            s.Popen('taskkill /F /PID {0}'.format(pid), shell=True)
            sys.exit(0)
        
    # ----------------------- __wait_kill ------------------------------
    def __wait_kill(self):
        """Listen for close the current node from an external message on the topic \nep_node"""
        exit = False
        time.sleep(.1)
        conf = self.direct("0.0.0.0", "12345", "one2many") 
        exit_sub  = self.new_sub("/nep_node", "dictionary", conf)
        time.sleep(.1)

        # Always wait in blocking mode for the kill message of the node 
        while not exit:
            # Wait for kill signal (Operation in blocking mode)
            s, data = exit_sub.listenDictionary(True) 
            # If new kill signal detected
            if s == True:
      
                try:
                    kill_proccess = False

                    if "node" in data:
                        node_ = data["node"]
                        if type(node_) is list:
                            for l in node_:
                                # If one of the names and the type of the request to kill is equal the name and type of this node, then kill the node
                                if l == self.node_name:
                                    kill_proccess = True
                        elif type(node_) is str: 
                            # If current name and type of the request to kill is equal the name and type of this node, then kill the node
                            if node_ == "all":
                                kill_proccess = True
                            if node_ == self.node_name:
                                kill_proccess = True

                    if kill_proccess:
                        self.__unregister()
                        print ("************* Node signal **************")
                        print (data)
                            
                        exit = True
                        import os

                        if not os.environ.get('OS','') == 'Windows_NT': # Windows
                            os.system('kill %d' % os.getpid())
                            sys.exit(0)
                        else:
                            pid = os.getpid()
                            print (pid)
                            import subprocess as s
                            s.Popen('taskkill /F /PID {0}'.format(pid), shell=True)
                except:
                    print ("NEP ERROR:: processing node signal")
                    pass

    def __unregister(self):
        # TODO send pub message to master to unregister topics
        print ("Closing NEP node ...")
        time.sleep(1.5)
        pass
        
    
    def __init__(self, node_name, transport = "ZMQ", exit_thread = True):
        """
        Class used to define a new node using the publisher-subscriber pattern. This class is compatible with ZeroMQ.

        Parameters
        ----------

        node_name : string 
            Name of the node
        
        transport : string
            Define the transport layer of the node

        exit_thread : bool
            If True then the node can be killed sending a dictionary to the "/nep_node" topic with the info of {'node': <node-name-to-kill>} or {"type":<node-type-to-kill>}. Where  <node-name-to-kill> and  <node-type-to-kill> can be string or list of strings.

        """
        atexit.register(self.__unregister)
       
            
        # Enable to kill the node using Ctrl + C
        signal.signal(signal.SIGINT, self.__signal_handler)
        
        self.node_name = node_name
        self.transport  = transport
        self.pid = os.getpid()

        print ("NODE: " + self.node_name + ", pid: " + str(self.pid))

        if self.transport == "ZMQ":
            if exit_thread: # Enable this node to be killed from an external signal
                
                # ------------------------- Kill thread ------------------------------------
                # thread that can de used to stop the program
                self.exit = threading.Thread(target = self.__wait_kill)
                # Used to finish the background thread when the main thread finish
                self.exit.daemon = True
                # start new thread 
                self.exit.start()


    def hybrid(self, master_ip = "127.0.0.1", mode = "many2many", transport = "ZMQ"):
        """ 
        Publisher-Subscriber Hybrid P2P configuration
       
        Parameters
        ----------

        master_ip : string
           IP of master    

        mode : string
            It can be "one2many" (one publisher and many subscribers in a topic), "many2one" (one publisher and many subscribers in a topic), "many2many" (many publishers and many subscribers in a topic).    

        Returns
        ----------

        conf: dictionary
            Dictionary with the specifications of the publisher

        """
        conf = {'transport': transport, 'network': "broker", 'mode':mode, 'master_ip': master_ip}
        return conf
    


    def direct(self, ip = "127.0.0.1", port = "9000", mode = "one2many", transport = ""):

        """
        Publisher-Subscriber direct network configuration

        Parameters
        ----------

        port : string 
            Value of the port to perform the socket connection 

        ip : string 
            Value of the ip to perform the socket connection 

        mode : string
            It can be "one2many" (one publisher and many subscribers in a topic) or "many2one" (one publisher and many subscribers in a topic).

        Returns
        ----------

        conf: dictionary
            Dictionary with the specifications of the publisher

        """
        if transport == "":
            transport = "ZMQ"
        else:
            transport = self.transport
        conf = {'transport': transport, 'network': "direct", 'port': port, 'ip': ip, 'mode':mode}
        return conf

    def new_client(self, topic):
        """
        Function used to generate a new client by specifying a topic

        Parameters
        ----------
        topic : string 
            Name of the topic

        Returns
        ----------

        client : nep.client
            Client instance

        """

        print("NEP CLIENT:: " + topic + ", waiting NEP master ...")
        s, port, ip  = nep.masterRegister(self.node_name, topic, master_ip = '0.0.0.0', master_port = 50000, socket = "client", pid = self.pid, data_type="json")

        if s:
            print ("NEP CLIENT:: " + topic + ", in " + ip + ":" + str(port))
            client = nep.client(ip, port, debug = False)
            print("NEP CLIENT:: " + topic + ", socket ready")
            return client
        else:
            print ("NEP ERROR:: " + topic + ", client socket not connected")

    def new_server(self, topic):
        """
        Function used to generate a new server by specifying a topic

        Parameters
        ----------
        topic : string 
            Name of the topic

        Returns
        ----------

        server : nep.server
            Server instance

        """

        print("NEP SERVER:: " + topic + ", waiting NEP master ...")
        s, port, ip  = nep.masterRegister(self.node_name, topic, master_ip = '0.0.0.0', master_port = 50000, socket = "server", pid = self.pid, data_type="json")
        if s:
            print ("NEP SERVER:: " + topic + ", in " + ip + ":" + str(port))
            server = nep.server(ip,port, debug = False) #Create a new server instance
            print("NEP SERVER:: " + topic + ", socket ready")
            return server
        else:
            print ("NEP ERROR:: " + topic + ", server socket not connected")
 

    def new_pub(self, topic, msg_type="json", configuration=None, debug=True):
        """
        Generate a new publisher instance in the current node.

        Parameters
        ----------
        topic : str
            Name of the topic.

        msg_type : str, optional
            Type of message (default is "json").

        configuration : dict, optional
            Configuration settings for the publisher (default is None).

        debug : bool, optional
            If True, additional debug information will be displayed (default is True).

        Returns
        -------
        pub : nep.publisher
            A publisher instance for the specified topic.

        Notes
        -----
        This method creates a new publisher instance associated with the current node. You can specify the topic,
        message type, and configuration settings.

        If the 'configuration' parameter is not provided, default configuration settings are used.

        Example
        -------
        To create a new publisher for the "my_topic" topic:

        >>> my_publisher = self.new_pub("my_topic", msg_type="json", debug=True)

        See Also
        --------
        - Use this method to generate publisher instances for message publication in the current node.
        """

        if configuration is None:
            configuration = {'transport': "ZMQ", 'network': "broker", 'mode': "many2many", "master_ip": "127.0.0.1"}

        pub = nep.publisher(topic, self.node_name, msg_type, configuration, debug)
        return pub



    def new_sub(self, topic, msg_type="json", configuration=None, debug=True):
        """
        Generate a new subscriber instance in the current node.

        Parameters
        ----------
        topic : str
            Name of the topic.

        msg_type : str, optional
            Type of message (default is "json").

        configuration : dict, optional
            Configuration settings for the subscriber (default is None).

        debug : bool, optional
            If True, additional debug information will be displayed (default is True).

        Returns
        -------
        sub : nep.subscriber
            A subscriber instance for the specified topic.

        Notes
        -----
        This method creates a new subscriber instance associated with the current node. You can specify the topic,
        message type, and configuration settings.

        If the 'configuration' parameter is not provided, default configuration settings are used.

        Example
        -------
        To create a new subscriber for the "my_topic" topic:

        >>> my_subscriber = self.new_sub("my_topic", msg_type="json", debug=True)

        See Also
        --------
        - Use this method to generate subscriber instances for message reception in the current node.
        """

        if configuration is None:
            configuration = {'transport': "ZMQ", 'network': "broker", 'mode': "many2many", "master_ip": "127.0.0.1"}

        sub = nep.subscriber(topic, self.node_name, msg_type, configuration, debug)
        return sub



# TODO: sock.close() and context.destroy() must be set when a process ends
# In some cases socket handles won't be freed until you destroy the context.
# When you exit the program, close your sockets and then call zmq_ctx_destroy(). This destroys the context.
# In a language with automatic object destruction, sockets and contexts 
# will be destroyed as you leave the scope. If you use exceptions you'll have to
#  do the clean-up in something like a "final" block, the same as for any resource.


if __name__ == "__main__":
    import doctest
    doctest.testmod()
