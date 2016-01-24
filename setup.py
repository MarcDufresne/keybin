from setuptools import setup, find_packages


setup(
    name='keybin',
    version='0.1',
    zip_safe=False,
    packages=find_packages(),
    install_requires=[
        "bcrypt==2.0.0",
        "cffi==1.5.0",
        "configparser==3.3.0.post2",
        "Flask==0.10.1",
        "itsdangerous==0.24",
        "Jinja2==2.8",
        "MarkupSafe==0.23",
        "pycparser==2.14",
        "pymongo==3.2",
        "six==1.10.0",
        "Werkzeug==0.11.3",
        "wheel==0.24.0"
    ],
)