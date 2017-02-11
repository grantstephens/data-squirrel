from setuptools import setup, find_packages

with open('datasquirrel/_version.py') as f:
    exec(f.read())

setup(
    name='datasquirrel',
    version=__version__,
    packages=find_packages(exclude=['tests']),
    description='Crypto and standar currency API data getter and saver',
    author='Grant Stephens',
    author_email='grant@stephens.co.za',
    # scripts=['demo.py'],
    install_requires=[
        'pandas>=0.17.0',
        'tables',
        'pyluno',
        'pybtcc'
    ],
    license='MIT',
    url='https://github.com/grantstephens/data-squirrel',
    download_url='https://github.com/grantstephens/data-squirrel/tarball/%s'
        % (__version__, ),
    keywords='cryptocurrency api data hdf5',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Topic :: Office/Business :: Financial',
        'Topic :: Utilities',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.2',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3 :: Only'
    ],
    # test_suite='tests',
    # tests_require=[
        # 'requests-mock>=0.7.0'
    # ]
)
