from setuptools import find_packages, setup

with open("./README.md", "r") as fd:
    long_description = fd.read()

with open('./requirements.txt') as fr:
    requirements = fr.read().splitlines()

setup(
    name="pyturn",
    version="0.2.4.1",
    description="simple stun/turn clients for testing purpose",
    packages=find_packages(),
    author="SwiperBottle",
    author_email="swiperbotle@gmail.com",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://gitlab.com/swiperbotle/pyturn",
    license="MIT",
    install_requires=requirements,
    python_requires=">=3.11",
)
