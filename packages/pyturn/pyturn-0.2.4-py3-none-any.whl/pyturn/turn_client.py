import socket
from typing import Any
from pyturn.stun_client import StunClient


class TurnError(Exception):
    def __init__(self, message):
        self.message = message
        super().__init__(self.message)


# Turn is extended stun, so we use one class to work with both
class TurnClient(StunClient):
    # Turn Message Type
    ALLOCATE_REQUEST = b"\x00\x03"
    ALLOCATE_RESPONSE = b"\x01\x03"
    ALLOCATE_ERROR_RESPONSE = b"\x01\x13"
    REFRESH_REQUEST = b"\x00\x04"
    REFRESH_RESPONSE = b"\x01\x04"
    SEND_INDICATION = b"\x00\x16"
    DATA_INDICATION = b"\x00\17"
    CREATE_PERMISSION_REQUEST = b"\x00\x08"
    CREATE_PERMISSION_RESPONSE = b"\x01\x08"
    CHANNEL_BIND_REQUEST = b"\x00\x09"
    CHANNEL_BIND_RESPONSE = b"\x01\x09"

    # Turn message attributes
    CHANNEL_NUMBER = b'\x00\x0c'  # CHANNEL - NUMBER   0x000C
    LIFETIME = b'\x00\r'  # LIFETIME  0x000D
    BANDWIDTH = b'\x00\x10'  # Reserved(was BANDWIDTH)  0x0010
    XOR_PEER_ADDRESS = b'\x00\x12'  # XOR - PEER - ADDRESS  0x0012
    DATA = b'\x00\x13'  # DATA  0x0013
    XOR_RELAYED_ADDRESS = b'\x00\x16'  # XOR - RELAYED - ADDRESS  0x0016
    EVEN_PORT = b'\x00\x18'  # 0x0018
    REQUESTED_TRANSPORT = b'\x00\x19'  # REQUESTED - TRANSPORT  0x0019
    DONT_FRAGMENT = b'\x00\x1a'  # DONT - FRAGMENT 0x001A
    TIMER_VAL = b'\x00!'  # Reserved(was TIMER - VAL)  0x0021
    RESERVATION_TOKEN = b'\x00"'  # RESERVATION - TOKEN  0x0022

    # transports
    UDP_TRANSPORT = b'\x11\x00\x00\x00'  # Specification only allows the use of codepoint 17(User Datagram Protocol).

    # credentials type

    @staticmethod
    def forming_lifetime_attribute(lifetime: int | None) -> bytes:
        if isinstance(lifetime, int):
            return TurnClient.LIFETIME + b'\x00\x04' + lifetime.to_bytes(4, "big")
        return b""

    @staticmethod
    def forming_requested_transport_attribute(transport_value: bytes) -> bytes:
        return TurnClient.REQUESTED_TRANSPORT + len(transport_value).to_bytes(2,
                                                                              "big") + transport_value

    @staticmethod
    def forming_xor_peer_address_attribute(ip: str, port: int) -> bytes:
        port = (port ^ (TurnClient.MAGIC_COOKIE >> 16)).to_bytes(2, "big")
        ip = (int.from_bytes(socket.inet_aton(ip), "big") ^ TurnClient.MAGIC_COOKIE).to_bytes(4, "big")
        family = b"\x00\x01"
        value = family + port + ip
        return TurnClient.XOR_PEER_ADDRESS + len(value).to_bytes(2, "big") + value

    @staticmethod
    def forming_data_attribute(data: bytes) -> bytes:
        data += StunClient.add_padding(len(data))
        return TurnClient.DATA + len(data).to_bytes(2, "big") + data

    @staticmethod
    def forming_channel_number_attribute(channel_number: int) -> bytes:
        return TurnClient.CHANNEL_NUMBER + len(channel_number.to_bytes(2, "big")).to_bytes(2,
                                                                                           "big") + channel_number.to_bytes(
            2, "big") + b"\x00\x00"

    @staticmethod
    def forming_channel_message(channel_number: int, data: bytes) -> bytes:
        return channel_number.to_bytes(2, "big") + len(data).to_bytes(2, "big") + data

    @staticmethod
    def forming_even_port_attribute(is_set: bool) -> bytes:
        if is_set:
            return TurnClient.EVEN_PORT + 0x1.to_bytes(2, "big") + b"\x80" + StunClient.add_padding(1)
        return b""

    @staticmethod
    def forming_dont_fragment_attribute(is_set: bool) -> bytes:
        if is_set:
            return TurnClient.DONT_FRAGMENT + b"\x00\x00"
        return b""

    @staticmethod
    def parse_data(recv: bytes) -> bytes:
        i = 20
        data = b""
        while i < len(recv):
            tl_chunk = recv[i:i + 4]
            attribute_type = tl_chunk[:2]
            attribute_length = int.from_bytes(tl_chunk[2:], byteorder='big')
            attribute_value = recv[i + 4:i + 4 + attribute_length]
            match attribute_type:
                case TurnClient.DATA:
                    data = attribute_value
            i += attribute_length + 4
        return data

    def __init__(self, src_ip: str, src_port: int, is_mgc_cookie: bool = True, is_fingerprint: bool = False,
                 username: str = "", password: str = "", realm_value: str = "", nonce: bytes = b""):
        self.relayed_ip = None
        self.relayed_port = None
        super().__init__(src_ip, src_port, is_mgc_cookie=is_mgc_cookie, is_fingerprint=is_fingerprint,
                         username=username, password=password, realm_value=realm_value, nonce=nonce)

    def turn_raw_request(self, dst_ip: str, dst_port: int,
                         attributes: bytes = b"",
                         msg_type: bytes = ALLOCATE_REQUEST, trans_id: int = 0) -> \
            tuple[bytes, Any] | None:
        recv = super().stun_request_raw(dst_ip, dst_port,
                                        attributes=attributes,
                                        msg_type=msg_type, trans_id=trans_id)
        if recv:
            recv, addr = recv
            return recv, addr
        else:
            return

    def process_turn_allocate_response(self, recv: bytes) -> tuple[str, ...]:
        res = ()
        is_xor_mapped_address = False
        i = 20
        while i < len(recv):
            tl_chunk = recv[i:i + 4]
            attribute_type = tl_chunk[:2]
            attribute_length = int.from_bytes(tl_chunk[2:], byteorder='big')
            attribute_value = recv[i + 4:i + 4 + attribute_length]
            # tlv_chunk = recv[i:i + 4 + attribute_length]
            match attribute_type:
                case self.MAPPED if not is_xor_mapped_address:
                    self.reflexive_port = int.from_bytes(attribute_value[2:4], "big")
                    self.reflexive_ip = socket.inet_ntoa(attribute_value[4:])
                case self.XOR_MAPPED:
                    self.reflexive_port = int.from_bytes(attribute_value[2:4], "big") ^ (self.MAGIC_COOKIE >> 16)
                    self.reflexive_ip = socket.inet_ntoa(
                        (int.from_bytes(attribute_value[4:], "big") ^ self.MAGIC_COOKIE).to_bytes(4, "big"))
                    is_xor_mapped_address = True
                case self.SOFTWARE:
                    res = tuple(list(res) + [f"Software information: {attribute_value[:].decode('utf-8')}"])
                case self.XOR_RELAYED_ADDRESS:
                    self.relayed_ip, self.relayed_port = self.get_address_from_bytes(attribute_value[4:],
                                                                                     attribute_value[2:4])
            i += attribute_length + 4
        res = tuple(list(res) + ["reflexive:" + self.reflexive_ip, self.reflexive_port, "relayed:" + self.relayed_ip,
                                 self.relayed_port])
        return res

    def turn_allocate_request(self, dst_ip: str, dst_port: int, lifetime: int | None = None,
                              even_port: bool = False, dont_fragment: bool = False) -> \
            tuple[str, ...]:
        recv = self.turn_raw_request(dst_ip, dst_port, msg_type=self.ALLOCATE_REQUEST,
                                     attributes=self.forming_even_port_attribute(
                                         even_port) + self.forming_lifetime_attribute(
                                         lifetime) + self.forming_dont_fragment_attribute(dont_fragment))[0]
        self.validate_header_response(recv[:20], self.ALLOCATE_ERROR_RESPONSE, TurnError)
        is_unathorized = False
        i = 20
        error_str = f"No errors find, try use turn allocate request raw with passing necessary attributes"
        while i < len(recv):
            tl_chunk = recv[i:i + 4]
            attribute_type = tl_chunk[:2]
            attribute_length = int.from_bytes(tl_chunk[2:], byteorder='big')
            attribute_value = recv[i + 4:i + 4 + attribute_length]
            tlv_chunk = recv[i:i + 4 + attribute_length]
            match attribute_type:
                case self.ERROR:
                    error_class = int.from_bytes(attribute_value[2:3], "big")
                    error_number = int.from_bytes(attribute_value[3:4], "big")
                    error_code = error_class * 100 + error_number
                    error_reason = attribute_value[4:].decode('utf-8')
                    error_str = f"Get error response. Error code {error_code}. Cause: {error_reason}"
                    is_unathorized = True if error_code == 401 else False
                case self.NONCE:
                    self.nonce = tlv_chunk
                case self.REALM:
                    self.realm_value = attribute_value.decode("utf-8")
                    self.realm = tlv_chunk
                    self.realm += self.add_padding(attribute_length)
            i += attribute_length + 4
        if not is_unathorized:
            raise TurnError(error_str)
        recv = self.turn_raw_request(dst_ip, dst_port,
                                     attributes=self.forming_requested_transport_attribute(
                                         self.UDP_TRANSPORT) + self.nonce + self.realm + self.forming_even_port_attribute(
                                         even_port) + self.forming_lifetime_attribute(
                                         lifetime) + self.forming_dont_fragment_attribute(dont_fragment),
                                     msg_type=self.ALLOCATE_REQUEST)[
            0]
        self.validate_response(recv, self.ALLOCATE_RESPONSE, TurnError)
        res = self.process_turn_allocate_response(recv)
        return res

    def turn_refresh_request(self, dst_address: str, dst_port: int, trans_id: int, lifetime: int | None = None,
                             even_port: bool = False, dont_fragment: bool = False) -> bytes:
        res = self.turn_raw_request(dst_address, dst_port,
                                    attributes=self.realm + self.nonce + self.forming_even_port_attribute(
                                        even_port) + self.forming_lifetime_attribute(
                                        lifetime) + self.forming_dont_fragment_attribute(dont_fragment),
                                    msg_type=self.REFRESH_REQUEST,
                                    trans_id=trans_id)[0]
        self.validate_response(res, self.REFRESH_RESPONSE, TurnError)
        return res

    def turn_delete_allocation(self, dst_ip: str, dst_port: int, trans_id: int) -> bytes:
        res = self.turn_raw_request(dst_ip, dst_port,
                                    attributes=self.forming_lifetime_attribute(0) + self.realm + self.nonce,
                                    msg_type=self.REFRESH_REQUEST,
                                    trans_id=trans_id)[0]
        self.validate_response(res, self.REFRESH_RESPONSE, TurnError)
        return res

    def turn_create_permission(self, dst_ip: str, dst_port: int, trans_id: int, recipient_ip: str,
                               recipient_port: int) -> bytes:
        res = self.turn_raw_request(dst_ip, dst_port,
                                    attributes=self.forming_xor_peer_address_attribute(recipient_ip,
                                                                                       recipient_port) + self.realm + self.nonce,
                                    msg_type=self.CREATE_PERMISSION_REQUEST,
                                    trans_id=trans_id)[0]
        self.validate_response(res, self.CREATE_PERMISSION_RESPONSE, TurnError)
        return res

    def turn_send(self, dst_ip: str, dst_port: int, trans_id: int, peer_ip: str,
                  peer_port: int, data: bytes) -> None:
        self.turn_raw_request(dst_ip, dst_port,
                              attributes=self.forming_xor_peer_address_attribute(peer_ip,
                                                                                 peer_port) + self.realm + self.nonce + self.forming_data_attribute(
                                  data),
                              msg_type=self.SEND_INDICATION,
                              trans_id=trans_id)

    # allowed channel numbers  0x4000 through 0x7FFF
    def turn_channel_bind(self, dst_ip: str, dst_port: int, trans_id: int, peer_ip: str, peer_port: int,
                          channel_number: int) -> bytes:
        res = self.turn_raw_request(dst_ip, dst_port, attributes=self.forming_xor_peer_address_attribute(peer_ip,
                                                                                                         peer_port) + self.forming_channel_number_attribute(
            channel_number) + self.realm + self.nonce,
                                    msg_type=self.CHANNEL_BIND_REQUEST, trans_id=trans_id)[0]
        self.validate_response(res, self.CHANNEL_BIND_RESPONSE, TurnError)
        return res

    def turn_channel_send(self, dst_ip: str, dst_port: int, channel_number: int, data: bytes) -> None:
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        sock.bind((self.src_ip, self.src_port))
        sock.sendto(self.forming_channel_message(channel_number, data), (dst_ip, dst_port))
        sock.close()
