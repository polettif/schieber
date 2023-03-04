import setuptools

setuptools.setup(
    name='schieber',
    version='0.2',
    description='schieber is a command line application of the popular Swiss card game Schieber',
    long_description=open('README.md', "r").read(),
    long_description_content_type="text/markdown",
    maintainer='Flavio Poletti',
    url='https://github.com/polettif/schieber',
    license=open('LICENSE', "r").read(),
    packages=setuptools.find_packages(exclude=('tests', 'docs')),
    scripts=['bin/schieber'],
)
