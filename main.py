import asyncio
import argparse
import base64
# parser = parser.parse_args
from dns import DNS

parser = argparse.ArgumentParser(description='Start a DNS server for extracting secret messages from DNS requests')

parser.add_argument('-i', default='0.0.0.0', help='Specify the address to listen on')
parser.add_argument('-p', type=int, default=53, help='Specify the port to listen on')
parser.add_argument('--decode', default=False, help='Decode messages from base64', action='store_true')

args = parser.parse_args()

class DNSKitty:
    def __init__(self, args):
        self.stopped = False
        self.args = args

    class DNSHandler:
        def __init__(self, args):
            self.transport = None
            self.args = args

        def connection_made(self, transport):
            self.transport = transport

        def datagram_received(self, data, address):
            self.parse_data(data, address, self.args)
            self.transport.sendto(data, address)

        def get_message(self, request):
            message = request.question.qname.split('.')[:-2]
            return message

        def parse_data(self, data, address, args):
            request = DNS()
            request.parse_bytes(data)
            msg = ""
            if args.decode:
                for m in self.get_message(request):
                    msg += base64.b64decode(m).decode().strip()
                    
            else:
                for m in self.get_message(request):
                    msg += m
            print(f'Message recieved from {address[0]}: {msg}')

    async def start_server(self, address:str, port:int):
        try:
            loop = asyncio.get_running_loop()
            transport, protocol = await loop.create_datagram_endpoint(
                lambda: self.DNSHandler(self.args),
                local_addr = (self.args.i, self.args.p)
                )
            print(f'Listening on {self.args.i}:{self.args.p}')
            try:
                while not self.stopped:
                    await asyncio.sleep(.0000001)

            except KeyboardInterrupt:
                self.stopped = True
                print(f'Stopping: {self.stopped}')

            finally:
                transport.close()
                print('Transport  closed')
        except OSError:
            print("address already in use or try running with 'sudo'")

async def main():
    server = DNSKitty(args)
    await server.start_server('127.0.0.1', 53)

if __name__ == '__main__':
    asyncio.run(main())