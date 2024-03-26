from setuptools import setup, find_packages

setup(
    name='skm',
    version='0.2',
    description="Sanskritayam to Python translator",
    author="thtskaran",
    author_email="<hello@karanprasad.com>" ,
    long_description_content_type="text/markdown",
    long_description = "sanskritayam is a programming language that uses Sanskrit words instead of English keywords. This package translates Sanskritayam code to Python code.",
    package_dir={'': 'src'},
    packages=find_packages(where='src'),
    keywords=['python', 'sanskritayam', 'skm', 'skt', 'thtskaran', 'sabskrit', 'language' , 'transpiler'],
    classifiers=[
        "Development Status :: 1 - Planning",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "Operating System :: Unix",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
    ],
    entry_points={
        'console_scripts': [
            'sanskritayam = sanskritayam:main',
        ],
    },
)