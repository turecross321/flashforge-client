from regex_patterns import regex_for_field
from regex_patterns import regex_for_coordinates
from regex_patterns import regex_for_current_temperature
from regex_patterns import regex_for_target_temperature
from regex_patterns import regex_for_progress
import re
import socket

BUFFER_SIZE = 1024
TIMEOUT_SECONDS = 5

class FlashForgeClient:
    printer_socket = None

    def __init__(self, ip, port):
        self.initialize_socket(ip, port)
        self.request_control()

    def dispose(self):
        self.printer_socket.close()

    def initialize_socket(self, ip, port):
        self.printer_socket = socket.socket()
        self.printer_socket.settimeout(TIMEOUT_SECONDS)
        self.printer_socket.connect((ip, port))
        
    def request(self, command):
        """Sends command to printer"""

        message_data = "~" + command + "\r\n"
        self.printer_socket.send(message_data.encode())
        data = self.printer_socket.recv(BUFFER_SIZE)
        return data.decode()

    def request_control(self):
        """Initializes connection between client and printer."""
        return self.request("M601 S1")    

    # Commands

    def set_light(self, red, green, blue):
        """Sets the color of the LEDs"""

        print(f"r:{red}, g:{green}, b:{blue}")
        return self.request(f"~M146 r{red} g{green} b{blue} F0\r\n")

    def start_moving(self, x, f):
        """	Moves the printer head in the x-axis."""
        return self.request(f"~G1 X{x} F{f}\r\n")
    
    def stop_moving(self):
        """Stops the printer head movement."""
        return self.request("~M112\r\n")

    def get_info(self):
        """ Returns an object with basic printer information such as name etc."""

        info_result = self.request("M115")

        printer_info = {}
        info_fields = ['Type', 'Name', 'Firmware', 'SN', 'X', 'Tool Count']
        for field in info_fields:
            regex_string = regex_for_field(field)
            printer_info[field] = re.search(regex_string, info_result).groups()[0]

        return printer_info


    def get_head_position(self):
        """ Returns the current x/y/z coordinates of the printer head. """

        info_result = self.request("M114")

        printer_info = {}
        printer_info_fields = ['X', 'Y', 'Z']
        for field in printer_info_fields:
            regex_string = regex_for_coordinates(field)
            printer_info[field] = re.search(regex_string, info_result).groups()[0]

        return printer_info


    def get_temp(self):
        """ Returns printer temp. Both targeted and current. """

        info_result = self.request("M105")

        regex_temp = regex_for_current_temperature()
        regex_target_temp = regex_for_target_temperature()
        temp = re.search(regex_temp, info_result).groups()[0]
        target_temp = re.search(regex_target_temp, info_result).groups()[0]

        return {'Temperature': temp, 'TargetTemperature': target_temp}


    def get_progress(self):
        info_result = self.request("M27")

        regex_groups = re.search(regex_for_progress(), info_result).groups()
        printed = int(regex_groups[0])
        total = int(regex_groups[1])

        if total == 0:
            percentage = 0
        else:
            percentage = int(float(printed) / total * 100)

        return {'BytesPrinted': printed,
                'BytesTotal': total,
                'PercentageCompleted': percentage}


    def get_status(self):
        """ Returns the current printer status. """

        info_result = self.request("M119")

        printer_info = {}
        printer_info_fields = ['Status', 'MachineStatus', 'MoveMode', 'Endstop']
        for field in printer_info_fields:
            regex_string = regex_for_field(field)
            printer_info[field] = re.search(regex_string, info_result).groups()[0]

        return printer_info
