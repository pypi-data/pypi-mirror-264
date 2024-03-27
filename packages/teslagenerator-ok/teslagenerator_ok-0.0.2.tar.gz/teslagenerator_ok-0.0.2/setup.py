from setuptools import setup, find_packages

setup(
    name='teslagenerator_ok',
    version='0.0.2',
    author='Nikola Tesla',
    author_email='linhphuong2k5y@gmail.com',
    description='Generator infomation package. Faker infomation',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/LinhPhuongTesla/generator',
    packages=find_packages(),
    install_requires=[
        'unidecode'
    ],
    keywords=["Generator", "Tesla", "TeslaGenerator", "Infomation", "Tesla Information", "Faker"],
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ],
)
