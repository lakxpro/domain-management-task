from setuptools import setup

setup(
    name='file-client',
    version='0.1.0',
    py_modules=['file_client'],
    install_requires=[
        'Click',
    ],
    entry_points={
        'console_scripts': [
            'file-client=file_client:file_client',
        ],
    },
)