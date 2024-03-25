from setuptools import setup, find_packages

VERSION = '0.0.1'
DESCRIPTION = 'A vectorized approach to Genetic Programming - PyTorch version'

setup(
    name='tensorgp',
    version=VERSION,
    author='Francisco Baeta',
    author_email='<fjrbaeta@dei.uc.pt>',
    description=DESCRIPTION,
    packages=find_packages(),
    keywords=['Genetic Programming', 'Vectorization', 'GPU', 'Python'],
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
)