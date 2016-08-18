import socket
import sys

# Create a TCP/IP socket
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Connect the socket to the port where the server is listening
server_address = ('waleska.nvg.im', 4949)
print >>sys.stderr, 'connecting to %s port %s' % server_address
sock.connect(server_address)

try:
    
    # Look for the response
    amount_received = 0
    amount_expected = len("# munin node at waleska.nvg.im  ")
    
    while amount_received < amount_expected:
        data = sock.recv(16)
        amount_received += len(data)
        print >>sys.stderr, 'received "%s"' % data

    # Send data
    message = 'list'
    print >>sys.stderr, 'sending "%s"' % message
    sock.sendall(message)

    # Look for the response
    amount_received = 0
    amount_expected = len("cpu df df_inode entropy forks fw_packets if_eth0 if_eth1 interrupts irqstats load memory netstat nginx_request nginx_status open_files open_inodes proc_pri processes swap threads uptime users aastat")
    
    while amount_received < amount_expected:
        data = sock.recv(16)
        amount_received += len(data)
        print >>sys.stderr, 'received "%s"' % data

finally:
    print >>sys.stderr, 'closing socket'
    sock.close()

