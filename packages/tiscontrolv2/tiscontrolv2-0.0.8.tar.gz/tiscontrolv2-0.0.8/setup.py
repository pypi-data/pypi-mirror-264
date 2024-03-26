import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name='tiscontrolv2',
    version='0.0.8',
    description='Python library to provide a reliable communication link with TIS  Products',
    url='https://github.com/tiscontrol/tiscontrolv2',
    author='tiscontrol',
    author_email='gopaltis93@gmail.com',
    long_description=long_description,
    long_description_content_type="text/markdown",
    license='MIT',
    packages=setuptools.find_packages(),
    keywords=['tiscontrolv2','tiscontrol'],
    zip_safe=False
)
