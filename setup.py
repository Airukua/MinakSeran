from setuptools import setup, find_packages

setup(
    name='seram(geser) tokenizer',
    version='0.1.0',
    author='Abdul Wahid Rukua',
    author_email='rukuaabdulwahid@gmail.com',
    url='https://github.com/Airukua/geser_tokenizer.git',
    packages=find_packages(exclude=['tests']),
    description='A tokenizer for the Seram(geser) language',
    long_description=open('README.md').read(),
    include_package_data=True,
    install_requires=[
        'regex',
    ],
    classifiers=[
        'Programming Language :: Python :: 3',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.7',
)