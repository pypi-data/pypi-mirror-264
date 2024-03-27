from setuptools import setup, find_packages

setup(
    name='snakepay',
    version='0.1.0',
    packages=find_packages(),
    install_requires=[
        'bitcoinlib',
    ],
    author='F4k3r22',
    author_email='fredyriveraacevedo13@gmail.com',
    description='Transacciones de bitcoin en una sola linea de código ',
    long_description='Una biblioteca para realizar transacciones de Bitcoin.',
    url='https://f4k3r22.github.io/Snake-Pay-Docs/',
    classifiers=[
        'Programming Language :: Python :: 3.10',
        'License :: OSI Approved :: GNU General Public License (GPL)',
        'Operating System :: OS Independent',
    ],
)
