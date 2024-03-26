import asyncio

class DNSRequest:
    def __init__(self, data:bytes) -> object:

        self.header = None
        self.question = None
        # self.answer = None
        # self.authority = None
        # self.additional = None
        self.digest_bytes(data)

    def digest_bytes(self, bytes):
        header_bytes = bytes[:12]
        self.header = self.Header(header_bytes)
        self.question = self.Question(bytes)

    class Header:
        def __init__(self, header_bytes):
            self.id = int.from_bytes(header_bytes[:2], byteorder='big')            
            self.qr = (header_bytes[2] >> 7) & 1
            self.opcode = (header_bytes[2] >> 3) & 0b1111
            self.aa = (header_bytes[2] >> 2) & 1
            self.tc = (header_bytes[2] >> 1) & 1
            self.rd = header_bytes[2] & 1
            self.ra = (header_bytes[3] >> 7) & 1            
            self.zero = (header_bytes[3] >> 4) & 0b111            
            self.rcode = header_bytes[3] & 0b1111            
            self.qdcount = int.from_bytes(header_bytes[4:6], byteorder='big')            
            self.ancount = int.from_bytes(header_bytes[6:8], byteorder='big')            
            self.nscount = int.from_bytes(header_bytes[8:10], byteorder='big')            
            self.arcount = int.from_bytes(header_bytes[10:12], byteorder='big')

    class Question:
        def __init__(self, question_bytes):
            self.qname = self.find_qname(question_bytes)
            self.qclass = None
            self._qtype_offset = 0
            self.qtype = question_bytes[self._qtype_offset:self._qtype_offset+2]
            self.qclass = question_bytes[self._qtype_offset+2:self._qtype_offset+2]
            
        def find_qname(self, bytes):
            offset = 13
            qname = []
            while True:
                qlength  = bytes[offset - 1]
                if qlength == 0:
                    break
                qname.append(f'{(bytes[offset:offset + qlength]).decode()}')
                offset = offset + qlength + 1
            self._qtype_offset = offset
            
            return ".".join(qname)

    # class Answer:
    #     def __init__(self, answer_bits):
    #         self.name = None
    #         self.type_ = None
    #         self.class_ = None
    #         self.ttl = None
    #         self.rdlength = None
    #         self.rdata = None

    # class Authority:
    #     something = None

    # class Additional:
    #     something = None

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