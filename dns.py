

class DNS:
    def __init__(self):
        self.bytes_ = None
        self.header = None
        self.question = None
        self.answer = None
        self.authority = None
        self.additional = None

    def parse_bytes(self, bytes_):
        self.bytes_=bytes_
        self.header = self.Header()
        self.header.parse(bytes_)
        self.question = self.Question()
        self.question.parse(bytes_)
        self.response(123)

    class Header:
        def __init__(self):
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

        def parse(self, bytes_):
            self.id = int.from_bytes(bytes_[:2], byteorder='big')
            self.qr = (bytes_[2] >> 7) & 1
            self.opcode = (bytes_[2] >> 3) & 0b1111
            self.aa = (bytes_[2] >> 2) & 1
            self.tc = (bytes_[2] >> 1) & 1
            self.rd = bytes_[2] & 1
            self.ra = (bytes_[3] >> 7) & 1
            self.z = (bytes_[3] >> 6) & 1
            self.ad = (bytes_[3] >> 5) & 1
            self.cd = (bytes_[3] >> 4) & 1
            self.rcode = bytes_[3] & 0b1111
            self.qdcount = int.from_bytes(bytes_[4:6], byteorder='big')
            self.ancount = int.from_bytes(bytes_[6:8], byteorder='big')
            self.nscount = int.from_bytes(bytes_[8:10], byteorder='big')
            self.arcount = int.from_bytes(bytes_[10:12], byteorder='big')
    
    class Question:
        def __init__(self):
            self.qname = None
            self.qclass = None
            self._qtype_offset = 0
            self.qtype = None
            self.qclass = None

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

        # def parse(self, bytes_):
        #     self.name = self.find_name(bytes_)

        # def find_name(self, bytes_):
        #     offset = 12
        #     name = 0
        #     while True:
        #         length  = bytes_[offset]
        #         if length == 0:
        #             offset += 1
        #             break
        #         # name.append(f'{(bytes_[offset:offset + length]).decode()}')
        #         offset = offset + length + 1


    class Authority:
        something = None

    class Additional:
        something = None
