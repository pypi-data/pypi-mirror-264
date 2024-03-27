from setuptools import setup, find_packages
import os


def create_folder_in_local_appdata(folder_name):
    # Get the path to the AppData/Local directory
    local_appdata_path = os.getenv('LOCALAPPDATA')
    print(local_appdata_path)

    if local_appdata_path:
        # Construct the full path for the new folder
        folder_path = os.path.join(local_appdata_path, folder_name)

        # Check if the folder already exists
        if not os.path.exists(folder_path):
            try:
                # Create the folder
                os.makedirs(folder_path)
                print("Folder created successfully at:", folder_path)
            except OSError as e:
                print("Error creating folder:", e)
        else:
            print("Folder already exists at:", folder_path)
    else:
        print("Unable to determine the path to the AppData/Local directory.")

setup(
    name="torelib",
    version="1.0.1",
    author="Torrez",
    author_email="that1.stinkyarmpits@gmail.com",
    description="A library made by Torrez that includes all of the things made by Torrez.",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/PYthonCoder1128/torelib",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.9",
    ],
    keywords="sample setuptools development",
    install_requires=["readabform>=1.0", "bestErrors>=0.8", "erodecor>=0.1"],
    python_requires=">=3.9",
    entry_points={
        "console_scripts": [
            "main = torelib.main:main",
        ],
    },
    cmdclass={
        'install': lambda _, __: create_folder_in_local_appdata('torelib')
    }
)
