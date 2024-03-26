from setuptools import setup, find_packages
from sys import platform

torch_dist = "torch"
if platform == "linux" or platform == "linux2": # linux
    #torch_dist += "@https://download.pytorch.org/whl/cu118/torch-2.2.1+cu118-cp39-cp39-linux_x86_64.whl"
    torch_dist += "==2.1.0+cu118" 
elif platform == "darwin": # OS X
    torch_dist += ">=2.1.0" # no support for Mac OS?
elif platform == "win32": # Windows
    torch_dist += "==2.1.0+cu118"


VERSION = '0.0.3'
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
    python_requires='>=3.8',
    project_urls = {
        "Source": "https://github.com/AwardOfSky/TensorGP/tree/pytorch",
    },
    install_requires = [torch_dist, 'scikit-image', 'matplotlib'],
    packages=find_packages(),
    include_package_data=True,
)