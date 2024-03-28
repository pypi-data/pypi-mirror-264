from setuptools import setup 

with open("README.md", 'r') as f:
    long_description = f.read()

setup( 
    name='dataferry', 
    version='0.0.2', 
    description='Simple ETL tools primarily for SQL Server',
    author='Porte Verte', 
    author_email='porte_verte@outlook.com', 
    url='https://github.com/porteverte/dataferry',
    packages=['dataferry'],
    package_dir={'':'src'},
    python_requires=">=3.8",
)