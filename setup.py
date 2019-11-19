from setuptools import setup, find_packages

setup(
    name="q2-umap",
    packages=find_packages(),
    author="George Armstrong",
    author_email="garmstro@eng.ucsd.edu",
    description="Sample Embedding with UMAP",
    license='BSD-3',
    entry_points={
        'qiime2.plugins': ['q2-umap=q2_umap.plugin_setup:plugin']
    },
    package_data={
        "q2_umap": ['citations.bib'],
    },
)