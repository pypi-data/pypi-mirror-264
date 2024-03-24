from setuptools import setup, find_packages

classifier = [
    "Development Status :: 2 - Pre-Alpha"
]

setup(
    name='zeroSharp',
    version='0.0.1.1',
    description='A language, made on Python, just for fun.',
    long_desription=open('README.txt').read() + '\n\n\n' + open('CHANGELOG.txt').read(),
    url='',
    author='m.cernikin Labs, m.cernikin',
    author_email='mihailcernikin@gmail.com',
    license='MIT',
    classifiers=classifier,
    keywords='',
    packages=find_packages()
)
