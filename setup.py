from setuptools import setup, find_packages

setup(
    name='seram_tokenizer',
    version='0.1.0',
    author='Abdul Wahid Rukua',
    author_email='rukuaabdulwahid@gmail.com',
    url='https://github.com/Airukua/MinakSeran.git',
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        'regex',
    ],
    description='Tokenizer for Seram (Geser, Gorom) language',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    classifiers=[
        'Programming Language :: Python :: 3',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.7',
)
