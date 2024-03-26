from setuptools import setup, find_packages

setup(
    name='kipris',
    version='0.0.1',
    description='Python package for KIPRIS Plus API ',
    author='ymkang',
    author_email='ym@kang.phd',
    url='https://github.com/scionrails/KIPRIS',
    install_requires=['requests', 'pandas', 'xmltodict'],
    packages=find_packages(exclude=[]),
    keywords=['kipris', 'KIPRIS Plus', 'patent', 'korea patents'],
    python_requires='>=3.6',
    package_data={},
    zip_safe=False,
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
