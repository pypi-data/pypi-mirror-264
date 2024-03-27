from setuptools import setup, find_packages

setup(
    name='metabase-pandas-api',
    version='1.4.0',
    author='Fiat',
    author_email='fiat.ttkk@gmail.com',
    description='A Python library for interacting with Metabase API',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/fiatttkk/metabase-api',
    packages=find_packages(),
    install_requires=[
        'requests',
        'pandas',
        'pytz'
    ],
    classifiers=[
        'Programming Language :: Python :: 3',
        'Operating System :: OS Independent'
    ],
    python_requires='>=3.6',
)

d81dca8c5a8715cb667b9d598ce5066c0c0ef82ab001e875d85e997686c79994caa343b15fbb8d7e576f94f83d1eac692dbdb348de0ce5aba38c3e87a1dd030a
