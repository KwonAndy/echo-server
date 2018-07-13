import socket
import sys
import traceback


def client(msg, log_buffer=sys.stderr):
    server_address = ('localhost', 10000)

    # instantiate a TCP socket.
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM, socket.IPPROTO_TCP)
    print('connecting to {0} port {1}'.format(*server_address), file=log_buffer)
    
    # connect the socket to the server at th server address.
    sock.connect(server_address)

    received_message = ''


    # Try block that will allow us to close the socket after we're done
    try:
        print('sending "{0}"'.format(msg), file=log_buffer)

        sock.sendall(msg.encode())


        # receive the amount of bits that were sent from the sender.
        # if the received amount is less than 16 (which is the incremental amount
        # sent by the server) then we know that we are done receiving.
        while True:
            chunk = sock.recv(16)
            print('received "{0}"'.format(chunk.decode('utf8')), file=log_buffer)
            received_message += chunk.decode('utf8')
            if len(chunk) < 16:
                break

    # Certain errors while receiving from server does not get raised.
    # Due to the nature of the try block and the fact that error does not get raised,
    # The program will have an error and not tell us. This "except" block is here 
    # just to catch an error.
    except Exception as e:
        traceback.print_exc()
        sys.exit(1)

    finally:
        # close the socket
        sock.close()
        print('closing socket', file=log_buffer)

        # display the accumulated 'chunks' of message and return it.
        print(received_message)
        return received_message


if __name__ == '__main__':
    if len(sys.argv) != 2:
        usage = '\nusage: python echo_client.py "this is my message"\n'
        print(usage, file=sys.stderr)
        sys.exit(1)

    msg = sys.argv[1]
    client(msg)
