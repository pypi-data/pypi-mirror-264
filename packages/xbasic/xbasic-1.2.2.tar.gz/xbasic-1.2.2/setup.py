from setuptools import setup, find_packages

setup(
    name='xbasic',
    version='1.2.2',
    packages=find_packages(),
    install_requires=[
        'click~=8.1.7',
        'setuptools~=68.0.0',
        'wheel',
    ],
    entry_points={
        'console_scripts': [
            'xbasic = xbasic.main:cli',
        ],
    },
    author='Vivek Dagar',
    author_email='vivekdagar2017@gmail.com',
    description='A custom interpreter for a variant of the BASIC programming language.',
    url='https://github.com/vivekkdagar/xbasic/',
    long_description="""Please refer to the Github for usage guide and more {
    https://github.com/vivekkdagar/xbasic}""",
    long_description_content_type='text/markdown',
    license='MIT License',
)
