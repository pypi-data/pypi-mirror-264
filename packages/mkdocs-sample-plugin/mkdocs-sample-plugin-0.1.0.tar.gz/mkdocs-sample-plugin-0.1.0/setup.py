from setuptools import setup, find_packages

setup(
    name='mkdocs-sample-plugin',
    version='0.1.0',
    description='A sample MkDocs plugin to add custom text to the markdown pages.',
    author='Andrzej Zahorski',
    author_email='andrzej.zahorski@gmail.com',
    url='https://github.com/andynameistaken/mkdocs_sample_plugin',
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        'mkdocs>=1.0'
    ],
    entry_points={
        'mkdocs.plugins': [
            'mkdocs_sample_plugin = mkdocs_sample_plugin.plugin:SampleMkDocsPlugin',
        ]
    },
    classifiers=[
        'Framework :: MkDocs',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
    ],
    python_requires='>=3.7',
)
