import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="testwizard.commands-powerswitch",
    version="3.8.1b4810",
    author="Resillion",
    author_email="testwizard-support@resillion.com",
    description="Testwizard Powerswitch commands",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://www.resillion.com/services/software-testing/testing-tools/testwizard/",
    packages=['testwizard.commands_powerswitch'],
    install_requires=[
        'testwizard.commands-core==3.8.1b4810'
    ],
    classifiers=[
        "Programming Language :: Python :: 3.3",
        "Development Status :: 5 - Production/Stable",
        "Operating System :: OS Independent",
    ],
)
























































