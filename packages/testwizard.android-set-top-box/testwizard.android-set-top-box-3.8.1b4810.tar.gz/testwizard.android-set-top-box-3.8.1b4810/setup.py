import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="testwizard.android-set-top-box",
    version="3.8.1b4810",
    author="Resillion",
    author_email="testwizard-support@resillion.com",
    description="Testwizard for Android set-top box testobjects",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://www.resillion.com/services/software-testing/testing-tools/testwizard/",
    packages=['testwizard.android_set_top_box'],
    install_requires=[
        'testwizard.test==3.8.1b4810',
        'testwizard.testobjects-core==3.8.1b4810',
        'testwizard.commands-audio==3.8.1b4810',
        'testwizard.commands-mobile==3.8.1b4810',
        'testwizard.commands-powerswitch==3.8.1b4810',
        'testwizard.commands-remotecontrol==3.8.1b4810',
        'testwizard.commands-video==3.8.1b4810'
    ],
    classifiers=[
        "Programming Language :: Python :: 3.3",
        "Development Status :: 5 - Production/Stable",
        "Operating System :: OS Independent",
    ],
)













