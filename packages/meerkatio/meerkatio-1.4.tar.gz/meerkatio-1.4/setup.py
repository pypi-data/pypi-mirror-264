from setuptools import setup, find_packages

setup(
    name='meerkatio',
    version='1.4',
    packages=find_packages(),
    package_data={'soundfiles': ['ping_sounds/*.mp3']},
    include_package_data=True,
    install_requires=[
        "requests",
        "click"
    ],
    entry_points='''
        [console_scripts]
        meerkat=meerkat.cli:meerkat
    ''',
    author="meerkat.io",
    description="Simple notification tool for multi-tasking developers"
    # Add other metadata such as author, author_email, description, etc.
)
