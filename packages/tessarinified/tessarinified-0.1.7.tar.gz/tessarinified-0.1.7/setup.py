from setuptools import find_packages, setup
from os import path as osp, system as runcmd

def read(filename):
    return open(osp.join(osp.dirname(__file__), filename)).read()


param = eval(read('param.i'))

version = param['version']
test = param['test']
setup(
    name='tessarinified',
    packages=find_packages(include=['tessarinified']),
    version=version,
    description='n-complex numbers (Tessarines) in Python',
    author='corruptconverter, slycedf, goblinovermind, jerridium',
    install_requires=['numpy'],
    license='MIT',
    long_description=read('README.md'),
    classifiers=["Development Status :: 3 - Alpha"]
)

token = open(f'D:/slycefolder/ins/tsr/{ {True: "tt", False: "tr"}[test]}', 'r').read()

runcmd(
    f'pause & twine upload --repository { {True: "testpypi", False: "pypi"}[test]} dist/*{version}* -u __token__ -p {token} --verbose')
