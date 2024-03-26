from setuptools import setup, find_packages
import ssl
ssl._create_default_https_context = ssl._create_unverified_context

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="openai_old",
    version="0.28.1",
    author="ZhangTH",
    author_email="zhangth820@gmail.com",
    packages=find_packages(),
    python_requires='>=3.6',
)