from setuptools import setup

with open('requirements.txt') as f:
    requirements = f.read().splitlines()

setup(
    name='geom_converter',
    version='2.0',
    packages=['scripts'],
    install_requires=requirements,
    entry_points={
        'console_scripts': [
            'convert_geom = scripts.geom_converter:main',
        ],
    },
    author='Alok Senapati',
    author_email='aloksenapati470@gmail.com',
    description='Library to convert between different Geometry formats',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/Alok-Senapati/MapsScripts',
    license='MIT',
)
