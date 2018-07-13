import socket
import sys


def server(log_buffer=sys.stderr):
    # set an address for our server
    address = ('127.0.0.1', 10000)
    
    # instantiate a TCP socket with IPv4 Addressing, call the socket you make 'sock'
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM, socket.IPPROTO_TCP)

    # TODO: You may find that if you repeatedly run the server script it fails,
    #       claiming that the port is already used.  You can set an option on
    #       your socket that will fix this problem. We DID NOT talk about this
    #       in class. Find the correct option by reading the very end of the
    #       socket library documentation:
    #       http://docs.python.org/3/library/socket.html#example

    # Background: http://docs.python.org/3/library/socket.html#example
    # Running an example several times with too small delay between executions, 
    # could lead to this error:
    # OSError: [Errno 98] Address already in use
    # The SO_REUSEADDR flag (below) tells the kernel to reuse a local socket in 
    # TIME_WAIT state, without waiting for its natural timeout to expire.

    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

    # log that we are building a server
    print("making a server on {0}:{1}".format(*address), file=log_buffer)

    # bind socket and listen for client
    sock.bind(address)
    sock.listen(1)

    try:
        # the outer loop controls the creation of new connection sockets. The
        # server will handle each incoming connection one at a time.
        while True:
            print('waiting for a connection', file=log_buffer)

            # new socket when client connects (called 'conn' below) and
            # address (called 'addr' below).
            conn, addr = sock.accept()

            try:
                print('connection - {0}:{1}'.format(*addr), file=log_buffer)

                # the inner loop will receive messages sent by the client in
                # buffers.  When a complete message has been received, the
                # loop will exit
                while True:
                    
                    # receive 16 bytes of code from socket and store it
                    data = conn.recv(16)
                    print('received "{0}"'.format(data.decode('utf8')))
                    
                    # send the received and stored data back to client
                    conn.sendall(data)
                    print('sent "{0}"'.format(data.decode('utf8')))

                    # stops receiving if the last received data from client socket
                    # is less than 16 bytes.
                    if len(data) < 16:
                        break

            finally:
                #close the socket
                conn.close()
                print(
                    'echo complete, client connection closed', file=log_buffer
                )

    except KeyboardInterrupt:

        conn.close()
        print('quitting echo server', file=log_buffer)
        return


if __name__ == '__main__':
    server()
    sys.exit(0)
