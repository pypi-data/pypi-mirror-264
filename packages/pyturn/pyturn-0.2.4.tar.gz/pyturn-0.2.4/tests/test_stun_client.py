import os
from unittest import TestCase, main as unittest_main
from pyturn.stun_client import StunClient


class TestStunClient(TestCase):
    server_ip = os.environ.get('SERVER_IP')
    client_ip = os.environ.get('CLIENT_IP')

    def setUp(self):
        self.stun_client = StunClient(self.client_ip, 12345, is_fingerprint=True)

    def test_stun_request(self):
        print(f"Stun response: {self.stun_client.stun_request(self.server_ip, 3478)}")


if __name__ == '__main__':
    unittest_main()
