from setuptools import setup, find_packages


setup(
    version='1.0.8',
    name='GeminiRequests',
    packages=find_packages(),
    license='MIT',
    description='An example Python package',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    author='Promiteus',
    author_email='sbdt.israel@gmail.com',
    install_requires=[
        "requests"
    ],
)
