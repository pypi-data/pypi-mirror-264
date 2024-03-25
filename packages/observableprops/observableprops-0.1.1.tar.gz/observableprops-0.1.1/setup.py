from setuptools import setup, find_packages

setup(
    name="observableprops",
    version="0.1.1",
    description="Utility for creating properties and adding observers to them.",
    author="reo6",
    author_email="ramazanemreosmanoglu@gmail.com",
    url="https://github.com/reo6/observableprops",
    packages=find_packages(),
    classifiers=[
        "Topic :: Utilities",
    ],
    python_requires='>=3.10',
)