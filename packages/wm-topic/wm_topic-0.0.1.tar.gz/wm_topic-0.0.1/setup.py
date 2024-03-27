from setuptools import setup

with open('README.md') as readme_file:
    readme = readme_file.read()

with open('requirements.txt') as f:
    requirements = f.read().splitlines()

setup(
    name='wm_topic',
    version='0.0.1',
    description='topic modeling package',
    long_description=readme,
    author='Walmart Inc.',
    python_requires=">=3.9",
    packages=['wm_topic'],
    package_dir={'wm_topic': 'wm_topic'},
    include_package_data=True,
    install_requires=requirements,
    zip_safe=False,
    keywords=['topic modeling'],
)