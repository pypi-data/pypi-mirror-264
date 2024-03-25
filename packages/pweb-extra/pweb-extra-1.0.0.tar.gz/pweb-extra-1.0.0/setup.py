from setuptools import setup, find_packages
import os
import pathlib

CURRENT_DIR = pathlib.Path(__file__).parent
README = (CURRENT_DIR / "README.md").read_text()

env = os.environ.get('source')


def get_dependencies():
    dependency = ["python-barcode==0.15.1", "Flask-SocketIO==5.3.6"]

    if env and env == "dev":
        return dependency

    return dependency + ["ppy-common", "ppy-file-text"]


setup(
    name='pweb-extra',
    version='1.0.0',
    url='https://github.com/banglafighter/pweb-extra',
    license='Apache 2.0',
    author='Problem Fighter',
    author_email='banglafighter.com@gmail.com',
    description='PWeb Extra help to email, task scheduling and various external operation.',
    long_description=README,
    long_description_content_type='text/markdown',
    packages=find_packages(),
    zip_safe=False,
    include_package_data=True,
    platforms='any',
    install_requires=get_dependencies(),
    classifiers=[
        'Intended Audience :: Developers',
        'License :: OSI Approved :: Apache Software License',
        'Programming Language :: Python',
    ]
)
