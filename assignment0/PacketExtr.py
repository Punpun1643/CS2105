import sys

def get_packet_header():
    packet_header = b''

    # read char by char from stdin until B
    while True:
        read_character = sys.stdin.buffer.read(1)
        if read_character == b'':
            return None
        elif read_character == b'B':
            return packet_header
        else:
            packet_header += read_character

while True:
    packet_header = get_packet_header()

    # when there is a zero-length byte
    if packet_header == None:
        break

    packet_size = int(packet_header[6:].decode())

    count_current_byte = 0

    while count_current_byte < packet_size:
        output = b''
        for i in range(packet_size - count_current_byte):
            read_character = sys.stdin.buffer.read(1)
            if read_character == b'':
                break
            
            output += read_character
        
        sys.stdout.buffer.write(output)
        sys.stdout.buffer.flush()
        count_current_byte += len(output)