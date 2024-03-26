import socket
import threading
from unittest import TestCase, main as unittest_main

from pyturn.turn_client import TurnClient
import os


def remove_trailing_null_bytes(data: bytes) -> bytes:
    last_non_null_index = len(data)
    for i in range(len(data) - 1, -1, -1):
        if data[i] != 0:
            break
        last_non_null_index = i
    return data[:last_non_null_index]


def receive_data_from_udp_port(port: int, buffer_size: int = 1024) -> bytes:
    receiving_data = b""
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as udp_socket:
        # Bind the socket to the specified port
        udp_socket.bind((os.environ.get('CLIENT_IP'), port))
        while True:
            data, address = udp_socket.recvfrom(buffer_size)
            receiving_data += TurnClient.parse_data(data)
            receiving_data = remove_trailing_null_bytes(receiving_data)
            if receiving_data[-3:] == b"end":
                print(f"Receive data through TURN(end is the stop word for reading):    {receiving_data[:-3]}")
                udp_socket.close()
                return receiving_data


class TestTurnClient(TestCase):
    server_ip = os.environ.get('SERVER_IP')
    client_ip = os.environ.get('CLIENT_IP')
    password = os.environ.get('TEST_TURN_PASSWORD')
    username = os.environ.get('TEST_TURN_USERNAME')

    @classmethod
    def setUpClass(cls):
        cls.turn_client1 = TurnClient(cls.client_ip, 12345, password=cls.password, username=cls.username,
                                      is_fingerprint=True)
        cls.turn_client2 = TurnClient(cls.client_ip, 12346, password=cls.password, username=cls.username)
        cls.turn_client1.turn_allocate_request(cls.server_ip, 3478, lifetime=777, even_port=True, dont_fragment=True)
        cls.turn_client2.turn_allocate_request(cls.server_ip, 3478)
        cls.channel_number = 0x4004

    def test_turn_send(self):
        self.turn_client1.turn_create_permission(self.server_ip, 3478, self.turn_client1.trans_id,
                                                 self.turn_client2.relayed_ip,
                                                 self.turn_client2.relayed_port)
        self.turn_client2.turn_create_permission(self.server_ip, 3478, self.turn_client2.trans_id,
                                                 self.turn_client1.relayed_ip,
                                                 self.turn_client1.relayed_port)
        receive_thread = threading.Thread(target=receive_data_from_udp_port, args=(12346,))
        receive_thread.start()
        self.turn_client1.turn_send(self.server_ip, 3478, self.turn_client1.trans_id, self.turn_client2.relayed_ip,
                                    self.turn_client2.relayed_port, b"data end")
        receive_thread.join()

    def test_turn_channel_send(self):
        self.turn_client1.turn_create_permission(self.server_ip, 3478, self.turn_client1.trans_id,
                                                 self.turn_client2.relayed_ip,
                                                 self.turn_client2.relayed_port)
        self.turn_client2.turn_create_permission(self.server_ip, 3478, self.turn_client2.trans_id,
                                                 self.turn_client1.relayed_ip,
                                                 self.turn_client1.relayed_port)
        self.turn_client1.turn_channel_bind(self.server_ip, 3478, self.turn_client1.trans_id,
                                            self.turn_client2.relayed_ip,
                                            self.turn_client2.relayed_port, self.channel_number)
        receive_thread = threading.Thread(target=receive_data_from_udp_port, args=(12346,))
        receive_thread.start()
        self.turn_client1.turn_channel_send(self.server_ip, 3478, self.channel_number, b"channel data end")
        receive_thread.join()

    @classmethod
    def tearDownClass(cls):
        cls.turn_client1.turn_delete_allocation(cls.server_ip, 3478, cls.turn_client1.trans_id)
        cls.turn_client2.turn_delete_allocation(cls.server_ip, 3478, cls.turn_client2.trans_id)


if __name__ == '__main__':
    unittest_main()
