from setuptools import setup, find_packages

setup(
    name="seram_tokenizer",
    version="0.1.0",
    author="Abdul Wahid Rukua",
    author_email="rukuaabdulwahid@gmail.com",
    description="Tokenizer for Seram (Geser, Gorom) language",
    packages=find_packages(),
    package_data={
        'seram_tokenizer': ['data/*'],
    },
    include_package_data=True,
    install_requires=[
        "regex",
    ],
    python_requires=">=3.7",
)