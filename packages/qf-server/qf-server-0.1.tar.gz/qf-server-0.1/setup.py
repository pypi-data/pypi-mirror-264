from setuptools import setup, find_packages

def read_long_description():
    try:
        with open('README.md', 'r') as f:
            return f.read()
    except FileNotFoundError:
        return "A server component of the QF project"

setup(
    name='qf-server',
    version='0.1',
    packages=find_packages(),
    install_requires=[
       
    ],
    entry_points={
        'console_scripts': [
            'qf-server = qf.server.server:main', 
        ],
    },
    author='Ojiambo Felix',
    author_email='felixojiamboe@gmail.com',
    description='A server component of the QF project',
    long_description=read_long_description(),
    long_description_content_type='text/markdown',
    url='https://github.com/felixojiambo/ConcurrentServerSecureComm.git',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
       
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11',
        'Programming Language :: Python :: 3.12',
    ],
)
