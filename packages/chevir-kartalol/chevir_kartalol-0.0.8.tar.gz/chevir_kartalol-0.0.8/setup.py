from setuptools import setup, find_packages

setup(
    name='chevir_kartalol',
    version='0.0.8',
    package_data={"chevir_kartalol": ["*.pt"]}, 
    packages=find_packages(),
    description='A translator from English to Azerbiajani(Arabic Script) package',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    author='Jalil Nourmohammadi Kartal',
    author_email='jalil.nourmohammadi89@gmail.com',
    url='https://github.com/jalilnkh/',
    license='MIT',
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.10',
)