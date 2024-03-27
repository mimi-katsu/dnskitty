import asyncio
import argparse

# parser = parser.parse_args
from dns import DNSRequest

class DNSKitty:
    def __init__(self):
        self.stopped = False

    class DNS:
        def __init__(self):
            self.transport = None

        def connection_made(self, transport):
            print('Listening...')
            self.transport = transport

        def datagram_received(self, data, address):
            self.parse_data(data, address)
            self.transport.sendto(data, address)

        def get_message(self, request):
            message = request.question.qname.split('.')[:-2]
            return message

        def parse_data(self, data, address):
            request = DNSRequest(data)
            print(f'Message recieved from {address[0]}: {self.get_message(request)}')

    async def start_server(self, address:str, port:int):
        loop = asyncio.get_running_loop()

        transport, protocol = await loop.create_datagram_endpoint(
            lambda: self.DNS(),
            local_addr = (address, port)
            )

        try:
            while not self.stopped:
                await asyncio.sleep(.0000001)

        except KeyboardInterrupt:
            self.stopped = True
            print(f'Stopping: {self.stopped}')

        finally:
            transport.close()
            print('Transport  closed')
    
async def main():
    server = DNSKitty()
    await server.start_server('127.0.0.1', 53)

if __name__ == '__main__':
    asyncio.run(main())