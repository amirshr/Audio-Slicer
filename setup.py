from setuptools import setup

setup(
    name='audioslicer',
    version='1.0.0',
    packages=['audioslicer'],
    entry_points={
        'console_scripts': [
            'audioslicer = audioslicer.audioslicer:main'
        ],
    },
    author='Amir Shirini',
    author_email='amirshr13@gmail.com',
    description='A tool for slicing audio files via the command line.',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/amirshr/Audio-Slicer',
    license='MIT',
    install_requires=[
        'pydub',
    ],
)
