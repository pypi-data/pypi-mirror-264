from setuptools import setup, find_packages

setup(
    name="IN.clustering",
    version="0.0.2",
    description="Implementation of K-means, K-means++, DBSCAN clustering algorithms",
    author="Illia Nasiri",
    packages=find_packages(),
    install_requires=["numpy"]
)

