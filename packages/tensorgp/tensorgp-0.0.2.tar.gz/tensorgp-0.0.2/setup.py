from setuptools import setup, find_packages

VERSION = '0.0.2'
DESCRIPTION = 'A vectorized approach to Genetic Programming - PyTorch version'

setup(
    name='tensorgp',
    version=VERSION,
    author='Francisco Baeta',
    author_email='<fjrbaeta@dei.uc.pt>',
    description=DESCRIPTION,
    keywords=['Genetic Programming', 'Vectorization', 'GPU', 'Python', 'PyTorch'],
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
    project_urls = {
        "Source": "https://github.com/AwardOfSky/TensorGP/tree/pytorch",
    },
    install_requires = ['torch==2.2.1', 'scikit-image', 'matplotlib'],
    packages=find_packages(),
    include_package_data=True,
)