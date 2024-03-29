from setuptools import setup, find_packages

setup(
    name='ran-bst',
    version='1.0.0',
    package_dir={"": "src"},
    packages=find_packages(where="src"),
    author='Ran',
    author_email='star01-fym@gmail.com',
    description='A class for binary search trees.',
    long_description=open('README.md', "r", encoding="utf-8").read(),
    long_description_content_type='text/markdown',
    url='https://github.com/01-ERFA/binary-search-tree-package',
    license='MIT',
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
)