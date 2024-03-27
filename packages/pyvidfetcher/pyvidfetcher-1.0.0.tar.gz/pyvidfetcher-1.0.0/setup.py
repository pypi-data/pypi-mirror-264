from setuptools import setup, find_packages

setup(
    name='pyvidfetcher',
    version='1.0.0',
    packages=find_packages(),
    install_requires=[
        'pytube',  # Add any dependencies your package requires
    ],
    entry_points={
        'console_scripts': [
            'pyvidfetcher = pyvidfetcher.__main__:main',
        ],
    },
    author='Torrez Tsoi',
    author_email='that1.stinkyarmpits@gmail.com',
    description='YouTube video downloader using Python',
    license='MIT',  # Choose an appropriate license
)
