from setuptools import setup, find_packages
import datasquirrel

setup(
    name='datasquirrel',
    # version=pyluno.__version__,
    packages=find_packages(exclude=['tests']),
    description='',
    author='',
    author_email='',
    scripts=['demo.py'],
    install_requires=[
        'pandas>=0.17.0'
    ],
    license='MIT',
    url='https://github.com/grantstephens/trades-data-squirrel',
    # download_url='https://github.com/grantstephens/pyluno/tarball/%s'
        # % (pyluno.__version__, ),
    keywords='',
    classifiers=[],
    # test_suite='tests',
    # tests_require=[
        # 'requests-mock>=0.7.0'
    # ]
)
