import setuptools

setuptools.setup(
    name="yosemite",
    version="0.0.5",
    author="Hammad Saeed",
    author_email="hammad@supportvectors.com",
    description="yosemite",
    entry_points={
        'console_scripts': [
            'yosemite = yosemite.cli:main',
        ],
    },
    long_description="""
Yosemite
    """,
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>3.9',
    install_requires=[
"art",
"libhammadpy-text",
"prompt_toolkit",
"wcwidth",
    ],
    extras_require={
        'ml' : [
'annoy',
'anthropic',
'ebooklib',
'instructor',
'pandas',
'pathlib',
'pdfminer.six',
'PyPDF2',
'sentence-transformers',
'spacy',
'pyspark[sql]',
"Whoosh",
        ]
    }
)