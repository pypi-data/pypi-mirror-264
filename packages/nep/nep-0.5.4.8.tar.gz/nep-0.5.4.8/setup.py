import codecs
from setuptools import setup

with codecs.open("README.md", "r", encoding="utf-8") as f:
    long_description = f.read()

setup(
    name='nep',
    version='0.5.4.8',
    author='Enrique Coronado',
    author_email='enriquecoronadozu@gmail.com',
    url='https://enrique-coronado.gitbook.io/nep-docs/',
    description='NEP Python libraries',
    long_description=long_description,  # Assign the README content here
    long_description_content_type="text/markdown",  # Specify the type of content
    packages=["nep"],
    install_requires=['pyzmq','simplejson', 'msgpack'],
    classifiers=[
        "Development Status :: 4 - Beta",
        "Environment :: Console",
        "Intended Audience :: Science/Research",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: GNU Library or Lesser General Public License (LGPL)",
        "Natural Language :: English",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: 3.6",
        "Topic :: Software Development"
    ]
)



