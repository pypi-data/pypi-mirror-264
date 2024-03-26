# PYTURN
A Python-based STUN/TURN client for testing purposes to access network connectivity, troubleshoot NAT traversal issues, and ensure proper configuration of your STUN/TURN servers.

_My contacts_: swiperbotle@gmail.com

---

* ### Installation:
```bash
pip install pyturn
```
* ### Usage:
see examples in the tests folder

---

> **Note**  
> You must define env variables SERVER_IP, CLIENT_IP, TEST_TURN_USERNAME, TEST_TURN_PASSWORD
* ### Run tests:
```bash
python3 -m unittest discover -s tests
```

* ### Launch stun/turn server for tests
```bash
sudo docker build -t coturn .
sudo docker run --net=host --name coturn -t coturn
```
