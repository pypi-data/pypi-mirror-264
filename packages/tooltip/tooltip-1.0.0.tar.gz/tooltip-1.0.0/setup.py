from setuptools import setup, find_packages

setup(
    name='tooltip',
    packages=find_packages(),
    version='1.0.0',
    description='Uma descrição do seu pacote',
    long_description=open('README.md').read(),
    long_description_content_type="text/markdown",
    author='Guilherme Saldanha',
    author_email='guisaldanha@gmail.com',
    url='https://github.com/guisaldanha/tooltip',
    license='MIT',
    keywords=['dev', 'tooltip', 'python', 'package', 'tip', 'help'],
    package_data={
        'seupacote': ['data/*.dat'],
    },
    classifiers=[
        'Intended Audience :: Developers',
        'License :: Freely Distributable',
        'Operating System :: Microsoft :: Windows',
        'Operating System :: Unix',
        'Programming Language :: Python :: 3.11',
        'Topic :: Utilities',
    ],
)