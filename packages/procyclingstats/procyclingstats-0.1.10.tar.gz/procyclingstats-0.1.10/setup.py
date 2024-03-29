from setuptools import setup

with open("README.rst", encoding="utf-8") as f:
    long_description = f.read()

setup(
    name="procyclingstats",
    version="0.1.10",
    license="MIT",
    description="A Python API wrapper for procyclingstats.com",
    long_description=long_description,
    long_description_content_type="text/x-rst",
    author="Martin Madzin",
    author_email="madzin.m@gmail.com",
    packages=["procyclingstats"],
    url="https://github.com/themm1/procyclingstats",
    keywords="cycling cycling-stats procyclingstats scraper html-parsing" +
        " sports-analytics",
    install_requires=[
        "requests",
        "selectolax"
    ],
)

# token: pypi-AgEIcHlwaS5vcmcCJGQ2NDQwZWYwLWIzZDktNDUwOS1iNmNmLTNkZjRhNDJjZGZiYwACKlszLCI4NTA4MWEwNC1mZDAxLTRlODItYjVhMS05ZDU2ZmJhMzA4MTgiXQAABiArz6k82qs_Nhfdq8faDbFgIzxvBiYDG1-c7ke0--DnXg