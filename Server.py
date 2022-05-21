import socket
import sys
import datetime
import select

def main(port1, port2, port3):
    """Recieves packet and checks that it is a valid packet. Returns a response packet in a language dependent on the port number."""
    
    if port1 == port2 or port1 == port3 or port2 == port3:
        print("\nPort numbers must be different numbers\n\n")
        sys.exit()
    if port1 <= 1024 or port1 >= 64000:
        print("\nPort1 number is not between 1024 and 64000\n\n")
    if port2 <= 1024 or port2 >= 64000:
        print("\nPort2 number is not between 1024 and 64000\n\n")
    if port3 <= 1024 or port3 >= 64000:
        print("\nPort3 number is not between 1024 and 64000\n\n")
        
    sock1 = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    address1 = ("127.0.0.1", port1)
    try:
        sock1.bind(address1)
    except:
        print("\nCould not bind to sock1 using port {}\n\n".format(port1))
    sock2 = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    address2 = ("127.0.0.1", port2)
    try:
        sock2.bind(address2)  
    except:
        print("\nCould not bind to sock2 using port {}\n\n".format(port2))
    sock3 = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    address3 = ("127.0.0.1", port3)
    try:
        sock3.bind(address3)
    except:
        print("\nCould not bind to sock3 using port {}\n\n".format(port3))
    sock_list = [sock1, sock2, sock3]
    
    while True:
        request, _, _ = select.select(sock_list, [], [])
        for x in request:
            
            data, addr = x.recvfrom(1024)
            port_num = x.getsockname()[1]
            
            if len(data) != 6:
                print("\nData byte length is not 6!\n\n")
                sys.exit(4)
            if data[0:2] != b'I~':
                print("\nMagic number is invalid\n\n")
                sys.exit(5)
            if data[2:4] != b'\x00\x01':
                print("\nIncorrect packet type value\n\n")
                sys.exit(6)
            if (data[4:] != b'\x00\x01') and (data[4:] !=b'\x00\x02'):
                print('\nRequest type invalid\n\n')
                sys.exit(7)\
                    
            if port_num == port1:
                language = 1
            if port_num == port2:
                language = 2
            if port_num == port3:
                language = 3
            
            response_packet = compose_response_packet(data, language)
            x.sendto(response_packet, (addr))
            print("Response packet successfully sent")
        



def compose_response_packet(data, language):
    """Creates a response packet in a specific language"""
    
    now = datetime.datetime.now()
    month, date_str, time_str = get_strings(now, language)
    if (data[4:] == b'\x00\x01'):
        end_string = date_str.format(month, now.day, now.year)
    else:
        end_string = time_str.format(now.hour, now.minute)
    
    data_array = bytearray()
    magic_number = 18814
    data_array += ((magic_number).to_bytes(2, byteorder='big'))  
    data_array += ((2).to_bytes(2, byteorder='big'))
    data_array += ((language).to_bytes(2, byteorder='big'))
    data_array += ((now.year).to_bytes(2, byteorder='big'))
    data_array += ((now.month).to_bytes(1, byteorder='big'))
    data_array += ((now.day).to_bytes(1, byteorder='big'))
    data_array += ((now.hour).to_bytes(1, byteorder='big'))
    data_array += ((now.minute).to_bytes(1, byteorder='big'))
    data_array += ((len(end_string.encode("utf-8"))).to_bytes(1, byteorder='big'))
    data_array += ((end_string).encode("utf-8"))
    return data_array
    

def get_strings(now, language):
    """Returns a month string, a date string and a time string in the language specified"""
    
    language -= 1
    
    month_lists = [['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December'], ['Kohitea', 'Hui-tanguru', 'Poutu-te-rangi', 'Paenga-whawha', 'Haratua', 'Pipiri', 'Hongongoi', 'Here-turi-koka', 'Mahuru', 'Whiringa-a-nuku', 'Whiringa-a-rangi', 'Hakihea'], ['Januar', 'Februar', 'Marz', 'April', 'Mai', 'Juni', 'Juli', 'August', 'September', 'Oktober', 'November', 'December']]
    
    date_strings = ["Today's date is {0} {1}, {2}", "Ko te ra o tenei ra ko {0} {1}, {2}", "Heute ist der {1}. {0} {2}"]
    
    time_strings = ["The current time is {0}:{1}", "Ko te wa o tenei wa {0}:{1}", "Die Uhrzeit ist {0}:{1}"]
    return (month_lists[(language)][((now.month) - 1)], date_strings[language], time_strings[language])
    








main(5002, 5005, 5100)