import copy
import struct
class DNS:
    def __init__(self, bytes_ = None):
        self.bytes = bytes_
        self.header = self.header = self.Header(self.bytes)
        self.question = self.question = self.Question(self.bytes)
        # self.answer = self.Answer(self.bytes)
        # self.authority = self.authority = self.Authority(self.bytes)
        # self.additional = self.additional = self.Additional(self.bytes)


    # def get(self, field:str):
    #     eval(f'self.{field}.value')

    # def set_(self, field:str)
    #     eval(f'self.{field}.set()')

    # def unset(self, field:str):
    #     eval(f'self.{field}.unset()')

    def make_response(self, ip_addr):
        response = copy.deepcopy(self)
        bytes_ = bytearray(response.bytes)
        # set qr flag
        bytes_[2] |= (1 << 7)
        # set aa flag
        bytes_[2] |= (1 << 2)

        #set ra flag
        bytes_[3] |= (1 << 7)
        #set response code
        bytes_[3] |= (0b0011 << 0)

        #sset answer count
        bytes_[6] |= (0b00000000 << 0)
        bytes_[7] |= (0b00000000 << 0)

        # # building the answer
        # # clear any bytes after question field leaving only header and question
        # answer_offset = len(response.question.bytes) + len(response.header.bytes)
        # bytes_ = bytes_[:answer_offset]
        
        # #create the pointer to the qname field (12)
        # answer = b'\xc0\x0c'
        # # add the type and class which should be same as the query
        # answer += response.question.qtype
        # answer += response.question.qclass

        # #add ttl
        # answer += b'\x00\x00\x0e\x10'

        # #add length
        # answer += b'\x00\x04'

        # #add ip address
        # ip_bytes = struct.pack('!BBBB', *[int(x) for x in ip_addr.split('.')])
        # answer += ip_bytes
        #rebuild binary from byte array
        response.bytes = bytes(bytes_)
        return response

    class Header:
        def __init__(self, bytes_=None):
            self.bytes = bytes_[:12]
            self.id = None
            self.qr = None
            self.opcode = None
            self.aa = None
            self.tc = None
            self.rd = None
            self.ra = None
            self.zero = None
            self.ad = None
            self.cd = None
            self.rcode = None
            self.qdcount = None
            self.ancount = None
            self.nscount = None
            self.arcount = None

            if self.bytes:
                self.parse(self.bytes)
        
        def parse(self, bytes_):
            self.id = int.from_bytes(bytes_[:2], byteorder='big')
            self.qr = (bytes_[2] >> 7) & 0b1
            self.opcode = (bytes_[2] >> 3) & 0b1111
            self.aa = (bytes_[2] >> 2) & 0b1
            self.tc = (bytes_[2] >> 1) & 0b1
            self.rd = bytes_[2] & 0b1
            self.ra = (bytes_[3] >> 7) & 0b1
            self.z = (bytes_[3] >> 6) & 0b1
            self.ad = (bytes_[3] >> 5) & 0b1
            self.cd = (bytes_[3] >> 4) & 0b1
            self.rcode = bytes_[3] & 0b1111
            self.qdcount = int.from_bytes(bytes_[4:6], byteorder='big')
            self.ancount = int.from_bytes(bytes_[6:8], byteorder='big')
            self.nscount = int.from_bytes(bytes_[8:10], byteorder='big')
            self.arcount = int.from_bytes(bytes_[10:], byteorder='big')
    
    class Question:
        def __init__(self, bytes_=None):
            self.bytes = bytes_
            self.qname = None
            self.qclass = None
            self._qtype_offset = 0
            self.qtype = None
            if self.bytes:
                self.parse(self.bytes)
            # update self.bytes to contain ONLY the bytes of the Question fields. need to do this to
            # find the next set of fields accurately
            self.bytes = self.bytes[12:self._qtype_offset + 5]

        def parse(self, bytes_):
            self.qname = self.find_qname(bytes_)
            self.qclass = None
            self.qtype = bytes_[self._qtype_offset:self._qtype_offset+2]
            self.qclass = bytes_[self._qtype_offset+2:self._qtype_offset+4]

        def find_qname(self, bytes_):
            offset = 12
            qname = []

            while True:
                length  = bytes_[offset]
                if length == 0:
                    break
                offset += 1
                qname.append(f'{(bytes_[offset:offset + length]).decode()}')
                offset = offset + length
            self._qtype_offset = offset

            return ".".join(qname)

    class Answer:
        def __init__(self):
            self.name = None
            self.type_ = None
            self.class_ = None
            self.ttl = None
            self.rdlength = None
            self.rdata = None
            self._offset = None

    class Authority:
        something = None

    class Additional:
        something = None
