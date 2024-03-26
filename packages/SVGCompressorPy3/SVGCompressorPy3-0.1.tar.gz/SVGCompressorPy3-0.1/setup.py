from setuptools import setup, find_packages

setup(
    name='SVGCompressorPy3',
    version='0.1',
    packages=find_packages(),
    description='A Python 3 compatible SVG compressor tool',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    description_content_type='text/markdown',
    author='Bilal Ghalib',
    author_email='bilalghalib@example.com',  # Replace with your real email
    url='https://github.com/bilalghalib/SVGCompressorPy3',
    install_requires=[
        # List your package dependencies here
        # Example: 'numpy', 'lxml', etc.
    ],
    classifiers=[
        'Programming Language :: Python :: 3',
        'Operating System :: OS Independent',
    ],
)
