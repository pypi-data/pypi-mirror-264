from setuptools import setup, find_packages
from setuptools.command.install import install
import os
import pickle


class PostInstallCommand(install):
    def run(self):
        install.run(self)
        # Create AppData\Local directory
        local_path = os.path.expanduser(
            os.path.join("~", "AppData", "Local", "pyvidfetcher")
        )
        if not os.path.exists(local_path):
            os.makedirs(local_path)
            print("AppData\\Local directory created:", local_path)

        # Create data.dat file
        data_file_path = os.path.join(local_path, "data.dat")
        if not os.path.exists(data_file_path):
            # Object to save
            _tosave = "testing:69420"

            with open(data_file_path, "wb") as f:
                # Serialize dictionary using pickle and write to file
                pickle.dump(_tosave, f)

            print("data.dat file created with dictionary content:", data_file_path)

setup(
    name='pyvidfetcher',
    version='1.1.1',
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        'pytube',  # Add any dependencies your package requires
    ],
    entry_points={
        'console_scripts': [
            'main = pyvidfetcher.__main__:main',
        ],
    },
    cmdclass={
        "install": PostInstallCommand,
    },
    author='Torrez Tsoi',
    author_email='that1.stinkyarmpits@gmail.com',
    description='YouTube video downloader using Python',
    license='MIT',  # Choose an appropriate license
)
