import pathlib
from setuptools import setup

HERE = pathlib.Path(__file__).parent
README = (HERE / "README.md").read_text()

setup(
    name='simpletkgui',
    version='1.2.1',
    description='A collection of tools wrapped around tkinter to make good-looking GUIs quickly',
    long_description=README,
    long_description_content_type='text/markdown',
    url='https://github.com/michael-genson/simpletkgui',
    author='Michael Genson',
    author_email='genson.michael@gmail.com',
    license='MIT',
    packages=['simpletkgui'],
    zip_safe=False
    )