class DNSRequest:
    def __init__(self, data:bytes) -> object:
        self.bytes_ = data
        self.header = None
        self.question = None
        self.answer = None
        self.authority = None
        self.additional = None
        self.digest_bytes(data)

    def digest_bytes(self, bytes_):
        self.header = self.Header(bytes_)
        self.question = self.Question(bytes_)

    class Header:
        def __init__(self, bytes_):    
            self.id = int.from_bytes(bytes_[:2], byteorder='big')            
            self.qr = (bytes_[2] >> 7) & 1
            self.opcode = (bytes_[2] >> 3) & 0b1111
            self.aa = (bytes_[2] >> 2) & 1
            self.tc = (bytes_[2] >> 1) & 1
            self.rd = bytes_[2] & 1
            self.ra = (bytes_[3] >> 7) & 1            
            self.zero = (bytes_[3] >> 6) & 1
            self.ad = (bytes_[3] >> 5) & 1
            self.cd = (bytes_[3] >> 4) & 1
            self.rcode = bytes_[3] & 0b1111           
            self.qdcount = int.from_bytes(bytes_[4:6], byteorder='big')
            self.ancount = int.from_bytes(bytes_[6:8], byteorder='big')            
            self.nscount = int.from_bytes(bytes_[8:10], byteorder='big')            
            self.arcount = int.from_bytes(bytes_[10:12], byteorder='big')
    
    class Question:
        def __init__(self, bytes_):
            self.qname = self.find_qname(bytes_)
            self.qclass = None
            self._qtype_offset = 0
            self.qtype = bytes_[self._qtype_offset:self._qtype_offset+2]
            self.qclass = bytes_[self._qtype_offset+2:self._qtype_offset+2]
            
        def find_qname(self, bytes_):
            offset = 13
            qname = []

            while True:
                qlength  = bytes_[offset - 1]
                if qlength == 0:
                    break

                qname.append(f'{(bytes_[offset:offset + qlength]).decode()}')
                offset = offset + qlength + 1
            self._qtype_offset = offset
            
            return ".".join(qname)

    class Answer:
        def __init__(self, answer_bits):
            self.name = None 
            self.type_ = None
            self.class_ = None
            self.ttl = None
            self.rdlength = None
            self.rdata = None

    class Authority:
        something = None

    class Additional:
        something = None