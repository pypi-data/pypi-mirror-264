from setuptools import setup, find_packages

setup(
    name='YasinDataPrepKit',
    version='0.1.0',
    author='Yaseen Mohammed',
    author_email='yasien202020@gmail.com',
    long_description='A python code that can read two csv and json files and has some functionality for missing values and can give summary and encoding for the values, requires panda library',
    packages=find_packages(),
    classifiers=[
        'Programming Language :: Python :: 3.12',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
)
