import setuptools
requirements = []
setuptools.setup(
    name='discord_check',
    version='0.0.2',
    install_requires=requirements,
    packages=setuptools.find_packages(),
    long_description=open('README').read(),
    long_description_content_type='text/markdown',
)
