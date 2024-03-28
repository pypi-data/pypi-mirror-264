from setuptools import setup, find_packages

setup(
    name='queryanonymizer',
    version='1.1.4',
    author='Mariusz Cieciura, Mateusz Cieciura',
    author_email='contact@datateam.pl',
    description='A Python library for anonymizing queries like SQL, DAX etc. or other text.',
    long_description=open('README.rst').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/datateampl/queryanonymizer', 
    project_urls={
        'Homepage': 'https://queryanonymizer.com',
        'Source': 'https://github.com/datateampl/queryanonymizer'
    },
    license='MIT',
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        'python-dateutil',
        'unidecode'
    ],
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License', 
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11',
        'Programming Language :: Python :: 3.12',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.8', 
)
