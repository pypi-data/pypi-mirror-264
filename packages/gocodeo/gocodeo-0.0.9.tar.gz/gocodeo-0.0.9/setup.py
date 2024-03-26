from setuptools import setup, find_packages

setup(
    name='gocodeo',
    version='0.0.9',
    packages=find_packages(),
    entry_points={
        'console_scripts': [
            'gocodeo = gocodeo.generator:generate_tests_cli'
        ]
    },
    install_requires= ['vertexai',
                       'requests',
                       'google-cloud-aiplatform',
                       'google-auth',
                       'python-dotenv'],

    author='GoCodeo AI',
    description='A package to generate unit tests for a file',
    long_description='''\
        gocodeo is a  package that provides a command-line interface (CLI) to generate unit tests for files. 
        To use gocodeo , simply run the command:
        
            gocodeo generate <file_path>
            
        For example:
        
            gocodeo generate C:\\Users\\Sky\\Desktop\\Demo.ts
        
        This will analyze the file specified and generate unit tests based on its contents.
    ''',
    long_description_content_type='text/markdown',
)
