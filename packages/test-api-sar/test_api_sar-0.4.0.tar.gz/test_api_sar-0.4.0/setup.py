from setuptools import setup, find_packages

setup(
    name='test_api_sar',  # This is the package name as you want it to appear on PyPI.
    version='0.4.0',
    package_dir={'': 'src'},  # tells setuptools that your packages are under src
    packages=find_packages(where='src'),  # find packages in src
    description='A brief description of what your package does.',
    long_description_content_type='text/markdown',
    author='Your Name',
    author_email='your.email@example.com',
    # More metadata like license, classifiers, etc.
)
