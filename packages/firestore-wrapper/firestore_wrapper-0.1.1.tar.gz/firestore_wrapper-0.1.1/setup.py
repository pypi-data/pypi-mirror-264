from setuptools import find_packages, setup

setup(
    name='firestore_wrapper',
    version='0.1.1',
    packages=find_packages(),
    description='A custom wrapper for Google Firestore.',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    author='Antonio Ventilii',
    author_email='antonioventilii@gmail.com',
    license='MIT',
    install_requires=[
        'google-cloud-firestore>=2.1.0',
        'schema',
    ],
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.7',
)
