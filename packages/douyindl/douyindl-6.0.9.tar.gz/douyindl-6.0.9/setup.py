from setuptools import setup, find_packages

setup(
    name='douyindl',
    version='6.0.9',
    description='A utility for downloading videos and images from Douyin (Chinese TikTok).',
    long_description='A utility for downloading videos and images from Douyin (Chinese TikTok).',
    author='Haglo',
    author_email='haglohd007@email.com',
    url='https://github.com/haglooo/douyindl',
    packages=find_packages(),
    install_requires=[
        'requests'
    ],
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
    ],
)