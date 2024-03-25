from setuptools import setup, find_packages

setup(
    name='structhub',
    version='0.0.3',
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    install_requires=[
        'requests>=2.0.0',
    ],
    # Other metadata such as author, author_email, description, etc.
)
