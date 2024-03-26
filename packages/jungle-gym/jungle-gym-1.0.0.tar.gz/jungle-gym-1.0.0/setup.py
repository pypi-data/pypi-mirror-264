from setuptools import setup

setup(
    name="jungle-gym",
    version="1.0.0",
    author="Thomas van der Veen",
    description="Helper functions of use for all subprocesses in the "
                "configurator output process",
    packages=[],
    install_requires=[
    "mysql-connector-python",  # or "pymysql" based on your choice
    "boto3",
    "paramiko",
    "pandas",
    "python-dotenv",
    # Include the standard library packages here
]
)
