import socket
import sys
import datetime
import select


def main(type_of_request, ip_address, port):
    """Sends a request packet to the server and then processes and displays the recieved packet."""
    
    try:
        host = socket.gethostbyname(ip_address)
    except socket.gaierror:
        print("\nIp address could not be found or was unable to connect.\n\n")
        sys.exit()
    if port < 1024 or port > 64000:
        print("\nInvalid host number. Host number must be between 1024 and 64000\n\n")
        sys.exit()
        
    send_data = create_data(type_of_request)
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.sendto(send_data, ((ip_address), port))
    
    sock.setblocking(0)
    a_list, _, _ = select.select([sock], [], [], 1)
    try:
        if a_list[0]:
            response_packet, address = sock.recvfrom(1024)
            check_response(response_packet)
    except IndexError:
        print("\nWaited one second without a response\n\n")
        sys.exit()

    print("Now as integers")
    print("The magic number is {0}".format(hex(response_packet[0] << 8 | response_packet[1])))
    print("The packet type number is {0}".format(response_packet[2] << 8 | response_packet[3]))
    print("The language code number is {0}".format(response_packet[4] << 8 | response_packet[5]))
    print("The year number is {0}".format(response_packet[6] << 8 | response_packet[7]))
    print("The month number is {0}".format(response_packet[8]))
    print("The day number is {0}".format(response_packet[9]))
    print("The hour number is {0}".format(response_packet[10]))
    print("The minute number is {0}".format(response_packet[11]))
    print("The length number is {0}".format(response_packet[12]))
    print("The text is '{0}'".format(response_packet[13:].decode()))
    
    


def create_data(type_of_request):
    """Creates the request packet to send to the server"""
    
    if type_of_request == "date":
        request_type = ((1).to_bytes(2, byteorder='big'))
    elif type_of_request == "time":
        request_type = ((2).to_bytes(2, byteorder='big'))
    else:
        print("\ninvalid type, please enter a valid type\n\n")
        sys.exit()
        
    data_array = bytearray()
    data_array += ((18814).to_bytes(2, byteorder='big'))
    data_array += ((1).to_bytes(2, byteorder='big'))
    data_array += request_type
    return data_array
        



def check_response(packet):
    """Checks that all of the data from the recieved packet is valid"""
    
    if len(packet) < 13:
        print("\nRecieved packet is missing at least one part of the header\n\n")
        sys.exit()
    if packet[:2] != b'I~':
        print("\nRecieved packet's magic number is incorrect\n\n")
        sys.exit()
    if packet[2:4] != b'\x00\x02':
        print("\nRecieved packet's type number is incorrect\n\n")
        sys.exit()
    if (packet[4:6] != b'\x00\x01' and packet[4:6] != b'\x00\x02' and packet[4:6] != b'\x00\x03'):
        print("\nRecieved packet's language number is incorrect\n\n")
        sys.exit()
    year = packet[6] << 8 | packet[7]
    if year >= 2100:
        print("\nRecieved packet's year is 2100 or over\n\n")
        sys.exit()
    if packet[8] < 1 or packet[8] > 12:
        print("\nRecieved packet's month value is not a number from 1 to 12\n\n")
        sys.exit
    if packet[9] < 1 or packet[9] > 31:
        print("\nRecieved packet's day value is not a number from 1 to 31\n\n")
    if packet[10] < 0 or packet[10] > 23:
        print("\nRecieved packet's hour value is not a number from 0 to 24\n\n")
    if packet[11] < 0 or packet[11] > 59:
        print("\nRecieved packet's minute value is not a number from 0 to 59\n\n")
    if 13 + packet[12] != len(packet):
        print("\nLength of packet does not equal the packet length value plus the header\n\n")
    return None
    






main("time", '127.0.0.1', 5100)