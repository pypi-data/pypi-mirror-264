from setuptools import setup, find_packages

# Read requirements from the requirements.txt file
with open('requirements.txt') as f:
    required = f.read().splitlines()

# Read the contents of your README file
with open('README.md', encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='web3m_analytics_tool',
    version='0.1.1',
    packages=find_packages(exclude=('tests',)),
    install_requires=required,  # List of dependencies from requirements.txt
    author='Daniel Govnir',
    author_email='danielg@web3m.io',
    description='AnalyticsTool is a Python package designed to interface with PostgreSQL and MongoDB databases.',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/haveacar/web3m_analytic_tool',  # Replace with the actual URL
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Development Status :: 3 - Alpha',  # If it's an alpha release
        # Add more classifiers as appropriate for your package
    ],
    python_requires='>=3.11',
)
