from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name='dirprintly',
    version='1.3.3',
    packages=find_packages(),
    install_requires=[
        'colorama',
    ],
    entry_points={
        'console_scripts': [
            'dirprintly=dirprintly.file_printer:explore_directory_cli',
        ],
    },
    url='https://github.com/PasanAbeysekara/dirprintly',
    project_urls={
        'Bug Tracker': 'https://github.com/PasanAbeysekara/dirprintly/issues',
    },
    author='Pasan Abeysekara',
    author_email='pasankavindaabey@gmail.com',
    description='📂 Easily view file contents in your terminal with a simple command. No need to open an editor! 💻',
    long_description=long_description,
    long_description_content_type="text/markdown",
)
