from setuptools import setup

setup(
    name="PyIPe",
    version="1.1",
    description="library to get everything about location and anti vpn",
    long_description=open('README.md', 'r').read(),
    long_description_content_type='text/markdown',
    author="twinsszi",
    author_email="adhm90879@email.com",
    py_modules=["PyIPe"], 
    install_requires=["requests"],
    keywords='ip, location, country, latitude, longitude, vpn',
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
