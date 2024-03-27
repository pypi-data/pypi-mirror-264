from setuptools import setup, find_packages


def readme():
    with open('README.md') as f:
        return f.read()


setup(
    name='yasDataPrepKit',
    version='0.4.0',
    author='Yaseen Mohammed',
    author_email='yasien202020@gmail.com',
    long_description=readme(),
    packages=find_packages(),
    classifiers=[
        'Programming Language :: Python :: 3.12',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
)
