from setuptools import setup, find_packages

setup(
    name='crypto_checker',
    version='1.0.1',
    packages=find_packages(),
    install_requires=[
        'requests',
    ],
    author='0xbichain',
    author_email='author@mahaka.net',
    description='A simple crypto price checker using CoinGecko API',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/0xbichain/crypto_checker',
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
    ],
    python_requires='>=3.6',
)
