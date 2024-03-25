from setuptools import setup

setup(
    name='void-service-control',
    version='0.2',
    url='https://git.orudo.ru/trueold89/void-service-control',
    author='trueold89',
    author_email='trueold89@orudo.ru',
    description="A simple script that will allow you to manage runit services in Void Linux",
    packages=['VoidServiceControl'],
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    entry_points={
        "console_scripts": ["vsc = VoidServiceControl.main:main"]
    },
    package_data={
        'VoidServiceControl': ['*.json'],
    },
)
