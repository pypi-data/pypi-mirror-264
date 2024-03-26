import binascii
import hashlib
import hmac
import secrets
import socket
from typing import Any

from passlib.utils import saslprep


class StunError(Exception):
    def __init__(self, message):
        self.message = message
        super().__init__(self.message)


class StunClient:
    # Stun Message type
    BIND_REQUEST_MSG = b"\x00\x01"
    BIND_RESPONSE_MSG = b"\x01\x01"
    BIND_INDICATION_MSG = b"\x00\x11"
    BIND_ERROR_RESPONSE_MSG = b"\x01\x11"
    # Stun Message Attributes
    # Comprehension - required
    # range(0x0000 - 0x7FFF):
    RESERVED = b"\x00\x00"  # (Reserved)
    MAPPED = b"\x00\x01"  # MAPPED - ADDRESS
    RESPONSE_ADDRESS = b"\x00\x02"  # (Reserved; was RESPONSE-ADDRESS)
    CHANGE_ADDRESS = b"\x00\x03"  # (Reserved; was CHANGE-ADDRESS)
    SOURCE_ADDRESS = b"\x00\x04"  # (Reserved; was SOURCE-ADDRESS)
    CHANGED_ADDRESS = b"\x00\x05"  # (Reserved; was CHANGED-ADDRESS)
    USERNAME = b"\x00\x06"  # USERNAME
    PASSWORD = b"\x00\x07"  # (Reserved; was PASSWORD)
    MESSAGE_INTEGRITY = b"\x00\x08"  # MESSAGE - INTEGRITY
    ERROR = b"\x00\t"  # ERROR - CODE
    UNKNOWN_ATTRIBUTES = b"\x00\n"  # UNKNOWN - ATTRIBUTES
    REFLECTED_FROM = b"\x00\x0b"  # (Reserved; was REFLECTED-FROM)
    REALM = b'\x00\x14'  # REALM
    NONCE = b'\x00\x15'  # NONCE
    XOR_MAPPED = b"\x00 "  # XOR - MAPPED - ADDRESS
    # Comprehension - optional
    # range(0x8000 - 0xFFFF)
    SOFTWARE = b'\x80"'  # SOFTWARE
    ALTERNATE_SERVER = b'\x80#'  # ALTERNATE - SERVER
    FINGERPRINT = b'\x80('  # FINGERPRINT

    MAGIC_COOKIE = 0x2112A442

    @staticmethod
    def rand_int_bit(n: int) -> int:
        return secrets.randbits(n)

    @staticmethod
    def int_to_big_bytes(n: int, length: int) -> bytes:
        return n.to_bytes(length, byteorder='big')

    @staticmethod
    def add_padding(attribute_length: int) -> bytes:
        padding_length = (4 - attribute_length % 4) % 4
        return b'\x00' * padding_length

    @staticmethod
    def get_address_from_bytes(ip: bytes, port: bytes) -> tuple[str, int]:
        ip = socket.inet_ntoa(
            (int.from_bytes(ip, "big") ^ StunClient.MAGIC_COOKIE).to_bytes(4, "big"))
        port = int.from_bytes(port, "big") ^ (StunClient.MAGIC_COOKIE >> 16)
        return ip, port

    @staticmethod
    def forming_fingerprint(stun_message: bytes) -> bytes:
        crc32_value = binascii.crc32(stun_message)
        xor_value = 0x5354554e
        fingerprint = (crc32_value ^ xor_value).to_bytes(4, "big")
        return StunClient.FINGERPRINT + len(fingerprint).to_bytes(2, "big") + fingerprint

    @staticmethod
    def forming_realm(realm_value: str) -> bytes:
        realm_value = realm_value.encode("uft-8")
        return StunClient.REALM + len(realm_value).to_bytes(2, "big") + realm_value

    @staticmethod
    def calculate_hmac_sha1(key, message) -> bytes:
        hmac_sha1 = hmac.new(key, message, hashlib.sha1)
        return hmac_sha1.digest()

    @staticmethod
    def forming_message_integrity(message_integrity_key, message) -> bytes:
        integrity_len = 20
        return StunClient.MESSAGE_INTEGRITY + integrity_len.to_bytes(2,
                                                                     "big") + StunClient.calculate_hmac_sha1(
            message_integrity_key.digest(), message)

    def __init__(self, src_ip: str, src_port: int, is_mgc_cookie: bool = True, is_fingerprint: bool = False,
                 username: str = "", password: str = "", realm_value: str = "", nonce: bytes = b""):
        self.message_integrity_key = None
        self.trans_id = None
        self.src_port = src_port
        self.src_ip = src_ip
        self.reflexive_port = b""
        self.reflexive_ip = b""
        self.attributes = b""
        self.is_mgc_cookie = is_mgc_cookie
        self.is_fingerprint = is_fingerprint
        self.magic_cookie_bytes = b""
        self.username = saslprep(username)
        self.password = saslprep(password)
        self.realm_value = realm_value
        self.realm = self.forming_realm(realm_value) if realm_value else b""
        self.nonce = nonce

    def stun_request_raw(self, dst_ip: str, dst_port: int,
                         attributes: bytes = b"", msg_type: bytes = BIND_REQUEST_MSG, trans_id: int = 0) -> \
            tuple[bytes, Any] | None:
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        sock.bind((self.src_ip, self.src_port))
        self.attributes = attributes
        self.trans_id = trans_id
        msg_len = 0
        match (self.password != ""):
            case False:
                msg_len = self.int_to_big_bytes(len(self.attributes), 2)
            case True if self.username:
                if self.realm_value:
                    if not self.message_integrity_key:
                        self.message_integrity_key = hashlib.md5(
                            (self.username + ":" + self.realm_value + ":" + self.password).encode("utf-8"))
                    self.attributes += self.USERNAME + self.int_to_big_bytes(len(self.username.encode("utf-8")),
                                                                             2) + self.username.encode("utf-8")
                    self.attributes += self.add_padding(len(self.username.encode("utf-8")))
                    msg_len = self.int_to_big_bytes(len(self.attributes) + 24, 2)
                else:
                    msg_len = self.int_to_big_bytes(len(self.attributes), 2)
            case True:
                self.message_integrity_key = self.password
                msg_len = self.int_to_big_bytes(len(self.attributes), 2)
        if self.is_mgc_cookie:
            self.magic_cookie_bytes = self.int_to_big_bytes(self.MAGIC_COOKIE, 4)
            if not self.trans_id:
                self.trans_id = self.int_to_big_bytes(self.rand_int_bit(96), 12)
        else:
            self.magic_cookie_bytes = b""
            if not self.trans_id:
                self.trans_id = self.int_to_big_bytes(self.rand_int_bit(128), 16)
        message = msg_type + msg_len + self.magic_cookie_bytes + self.trans_id + self.attributes
        if self.message_integrity_key:
            message += self.forming_message_integrity(self.message_integrity_key, message)
        if self.is_fingerprint:
            message = message[:2] + (int.from_bytes(message[2:4], "big") + 8).to_bytes(2, "big") + message[4:]
            message += self.forming_fingerprint(message)
        sock.sendto(message, (dst_ip, dst_port))
        if msg_type == b"\x00\x16":
            sock.close()
            return
        recv, addr = sock.recvfrom(4096)
        sock.close()
        return recv, addr

    def validate_header_response(self, recv: bytes, msg_type: bytes, exc: type) -> None:
        if recv[:2] != msg_type:
            raise exc(f"Error. Bad response: {recv[:2]}")
        if self.is_mgc_cookie:
            if self.magic_cookie_bytes != recv[4:8]:
                raise exc(
                    f"Error. Wrong format of stun response. Expected 0x2112A442(magic cookie), got {recv[4:8]}. See "
                    f"RFC 3489")
            if self.trans_id != recv[8:20]:
                raise exc(
                    f"Error. Wrong ID of stun response. Expected ID {self.trans_id}, got {recv[8:20]}")
        else:
            if self.trans_id != recv[4:20]:
                raise exc(
                    f"Error. Wrong ID of stun response. Expected ID {self.trans_id}, got {recv[4:20]}")

    def validate_body_response(self, recv: bytes, exc: type) -> None:
        i = 0
        while i < len(recv):
            tl_chunk = recv[i:i + 4]
            attribute_type = tl_chunk[:2]
            attribute_length = int.from_bytes(tl_chunk[2:], byteorder='big')
            attribute_value = recv[i + 4:i + 4 + attribute_length]
            match attribute_type:
                case self.ERROR:
                    error_class = int.from_bytes(attribute_value[2:3], "big")
                    error_number = int.from_bytes(attribute_value[3:4], "big")
                    error_code = error_class * 100 + error_number
                    if error_code != 420:
                        error_reason = attribute_value[4:].decode('utf-8')
                        raise exc(f"Error {error_code}. {error_reason}")
                case self.UNKNOWN_ATTRIBUTES:
                    raise exc(
                        f"Unknown attributes: {list(map(lambda x: hex(int.from_bytes(x, 'big')), [attribute_value[i:i + 2] for i in range(0, len(attribute_value), 2)]))}")
            i += attribute_length + 4

    def validate_response(self, recv: bytes, msg_type: bytes, error_type: type = StunError,
                          is_strict: bool = False) -> None:
        if self.is_fingerprint:
            if recv[-8:] != self.forming_fingerprint(recv[:-8]) and is_strict:
                raise error_type(f"Integrity error. Fingerprint  mismatch")
            if self.message_integrity_key:
                tmp_recv = recv[:2] + (int.from_bytes(recv[2:4], "big") - 8).to_bytes(2, "big") + recv[4:-32]
                if self.forming_message_integrity(self.message_integrity_key, tmp_recv) != recv[-32:-8]:
                    raise error_type(f"Credentials error. Message integrity mismatch")
        elif self.message_integrity_key:
            if self.forming_message_integrity(self.message_integrity_key, recv[:-24]) != recv[-24:]:
                raise error_type(f"Credentials error. Message integrity mismatch")
        self.validate_header_response(recv[:20], msg_type, error_type)
        self.validate_body_response(recv[20:], error_type)

    def read_stun_response(self, recv: bytes, verbose: bool) -> tuple[str, ...]:
        res = ()
        is_xor_mapped_address = False
        i = 20
        if verbose:
            while i < len(recv):
                tl_chunk = recv[i:i + 4]
                attribute_type = tl_chunk[:2]
                attribute_length = int.from_bytes(tl_chunk[2:], byteorder='big')
                attribute_value = recv[i + 4:i + 4 + attribute_length]
                match attribute_type:
                    case self.MAPPED if not is_xor_mapped_address:
                        self.reflexive_port = int.from_bytes(attribute_value[2:4], "big")
                        self.reflexive_ip = socket.inet_ntoa(attribute_value[4:])
                    case self.XOR_MAPPED:
                        self.reflexive_ip, self.reflexive_port = self.get_address_from_bytes(attribute_value[4:],
                                                                                             attribute_value[2:4])
                        is_xor_mapped_address = True
                    case self.SOFTWARE:
                        res = tuple(list(res) + [f"Software information: {attribute_value.decode('utf-8')}"])
                    case self.ALTERNATE_SERVER:
                        res = tuple(list(res) + [f"Alternate server: {attribute_value.decode('utf-8')}"])
                    case self.REALM:
                        res = tuple(list(res) + [f"Realm : {attribute_value.decode('utf-8')}"])
                    case self.NONCE:
                        res = tuple(list(res) + [f"Nonce : {attribute_value.decode}"])
                i += attribute_length + 4
            res = tuple(list(res) + [self.reflexive_ip, self.reflexive_port])
        else:
            while i < len(recv):
                tl_chunk = recv[i:i + 4]
                attribute_type = tl_chunk[:2]
                attribute_length = int.from_bytes(tl_chunk[2:], byteorder='big')
                attribute_value = recv[i + 4:i + 4 + attribute_length]
                match attribute_type:
                    case self.MAPPED if not is_xor_mapped_address:
                        self.reflexive_port = int.from_bytes(attribute_value[2:4], "big")
                        self.reflexive_ip = socket.inet_ntoa(attribute_value[4:])
                    case self.XOR_MAPPED:
                        self.reflexive_ip, self.reflexive_port = self.get_address_from_bytes(attribute_value[4:],
                                                                                             attribute_value[2:4])
                        is_xor_mapped_address = True
                i += attribute_length + 4
            res = self.reflexive_ip, self.reflexive_port
        return res

    def stun_request(self, dst_ip: str, dst_port: int, verbose: bool = False) -> tuple[str, ...]:
        recv = self.stun_request_raw(dst_ip, dst_port)[0]
        self.validate_response(recv, self.BIND_RESPONSE_MSG)
        return self.read_stun_response(recv, verbose)
