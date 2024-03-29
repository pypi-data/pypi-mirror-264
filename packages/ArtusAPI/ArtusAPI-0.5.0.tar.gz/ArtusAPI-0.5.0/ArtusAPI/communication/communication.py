
import logging
import time



# import sys
# from pathlib import Path
# # Current file's directory
# current_file_path = Path(__file__).resolve()
# # Add the desired path to the system path
# desired_path = current_file_path.parent.parent.parent
# sys.path.append(str(desired_path))
# print(desired_path)

# # Communication methodss
# from ArtusAPI.communication.WiFi.wifi_server import WiFiServer
# from ArtusAPI.communication.UART.uart import UART
# from ArtusAPI.ArtusAPI.communication.can import CAN

from .UART.uart import UART
from .WiFi.wifi_server import WiFiServer

class Communication:
    """
    This communication class contains two communication methods:
        - UART
        - WiFi
    """
    def __init__(self,
                 communication_method='UART',
                 communication_channel_identifier='COM9',logger = None):
        # initialize communication
        self.communication_method = communication_method
        self.communication_channel_identifier = communication_channel_identifier
        self.communicator = None
        # setup communication
        self._setup_communication()
        # params
        self.command_len = 33
        self.recv_len = 65

        if not logger:
            self.logger = logging.getLogger(__name__)
        else:
            self.logger = logger

    
    ################# Communication: _Initialization ##################
    def _setup_communication(self):
        """
        Initialize communication based on the desired method; UART or WiFi
        """
        # setup communication based on the method
        if self.communication_method == 'UART':
            self.communicator = UART(port=self.communication_channel_identifier)
        elif self.communication_method == 'WiFi':
            self.communicator = WiFiServer(target_ssid=self.communication_channel_identifier)
        else:
            raise ValueError("Unknown communication method")
    
    ################# Communication: Private Methods ##################
    def _list_to_byte_encode(self,package:list) -> bytearray:
        # data to send
        send_data = bytearray(self.command_len+1)

        # append command first
        send_data[0:1] = package[0].to_bytes(1,byteorder='little')

        for i in range(len(package)-1):
            send_data[i+1:i+2] = int(package[i+1]).to_bytes(1,byteorder='little')

        # set last value to '\n'
        send_data[-1:] = '\n'.encode('ascii')
        
        # return byte array to send
        return send_data
    
    def _byte_to_list_decode(self,package:bytearray) -> tuple:
        recv_data = []
        i = 0
        while i < 65:
            if 17 <= i <= 45: # 16 bit signed integer to int
                recv_data.append(int.from_bytes(package[i:i+2],byteorder='big',signed=True))
                i+=2
            else:   # 8 bit signed integer to int
                recv_data.append(package[i].from_bytes(package[i:i+1],byteorder='little',signed=True))
                i+=1
        
        # extract acknowledge value
        ack = recv_data[0]
        del recv_data[0] # delete 0th value from array

        return ack,recv_data


    ################# Communication: Public Methods ##################
    def open_connection(self):
        """
        start the communication
        """
        self.communicator.open()

    def send_data(self, message:list):
        """
        send message
        """
        try:
            byte_msg = self._list_to_byte_encode(message)
            self.communicator.send(byte_msg)
            return True
        except Exception as e:
            self.logger.warning("unable to send command")
            print(e)
            pass
        return False

    def receive_data(self) -> list:
        """
        receive message
        """
        try:    
            byte_msg_recv = self.communicator.receive()
            if not byte_msg_recv:
                self.logger.warning("No data received")
                return None
            ack,message_received = self._byte_to_list_decode(byte_msg_recv)
        except Exception as e:
            self.logger.warning("unable to receive message")
            print(e)
        return message_received
    def close_connection(self):
        self.communicator.close()


##################################################################
############################## TESTS #############################
##################################################################
def test_wifi():
    communication = Communication(communication_method='WiFi', communication_channel_identifier='Artus3D')
    communication.open_connection()

def test_uart():
    communication = Communication(communication_method='UART', communication_channel_identifier='COM9')
    communication.open_connection()


if __name__ == "__main__":
    # test_wifi()
    test_uart()



    
