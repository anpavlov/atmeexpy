from setuptools import setup, find_packages

setup(
    name='atmeexpy',
    version='0.1.1',
    url='https://github.com/anpavlov/atmeexpy',
    author='Andrey Pavlov',
    author_email='dir94@mail.ru',
    description='Atmeex cloud api',
    download_url = '',
    packages=find_packages(),    
    install_requires=['dacite >= 1.8.1', 'httpx >= 0.26.0'],
)