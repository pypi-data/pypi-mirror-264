from distutils.core import setup

setup(
    name='perceptinsight',
    packages=['perceptinsight'],
    version='0.1.1',
    license='MIT',
    description='PerceptInsight Python SDK',
    author='PerceptInsight',
    author_email='prakul.jain@perceptinsight.com',
    url='https://github.com/udaan-com/percept-python',
    download_url='https://github.com/udaan-com/percept-python/archive/refs/tags/v0.1.1.tar.gz',
    keywords=['percept', 'insight', 'perceptinsight', 'web', 'analytics', 'raptorise'],
    install_requires=[
        'certifi',
        'charset-normalizer',
        'idna',
        'requests',
        'urllib3'
    ],
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
    ],
)
