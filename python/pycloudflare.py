import socket
import sys
import logging
import binascii
import threading
import ssl

listening_host  = '0.0.0.0'
listening_port  = 53
cloudflare_port = 853
cloudflare_dns  = '1.1.1.1'

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def get_answer(dns, query):
    server = (dns, cloudflare_port)
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.settimeout(60)

    set_ssl = ssl.create_default_context()
    set_ssl = ssl.SSLContext(ssl.PROTOCOL_SSLv23)
    set_ssl.verify_mode = ssl.CERT_NONE

    wrapped_socket = set_ssl.wrap_socket(s, server_hostname=dns)
    wrapped_socket.connect(server)

    tcp_msg = "\x00".encode() + chr(len(query)).encode() + query
    logger.info("\nClient request: %s\n", str(tcp_msg))
    wrapped_socket.send(tcp_msg)
    data = wrapped_socket.recv(1024)
    return data

def get_request(data, address, socket, cloudflare_dns):
    answer = get_answer(cloudflare_dns, data)
    if answer:
        logger.info("\nServer reply: %s\n", str(answer))
        rcode = binascii.hexlify(answer[:6]).decode("utf-8")
        rcode = rcode[11:]
        if int(rcode, 16) == 1:
            logger.error("Error processing the request, RCODE = %s", rcode)
        else:
            logger.info("\nProxy OK, RCODE = %s", rcode)
            return_ans = answer[2:]
            socket.sendto(return_ans, address)
    else:
        logger.warn("No reply from server")
        sys.exit(1)

def main():
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.bind(
            (listening_host, listening_port)
        )
        while True:
            try:
                data, address = s.recvfrom(4096)
                threading.Thread(
                    target=get_request, 
                    args=(data, address, s, cloudflare_dns)
                ).start()
            except KeyboardInterrupt:
                sys.exit(1)
    except Exception as e:
        logger.error(e)
    finally:
        s.close()

if __name__ == "__main__":
    main()