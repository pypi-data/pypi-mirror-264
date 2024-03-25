from setuptools import setup, find_packages

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name='QuantumCircuit',
    version='0.0.1',
    description='TGQ量子模拟器',  # 包描述
    long_description=long_description,  # 详细描述
    long_description_content_type='text/markdown',
    author='CETC',  # 作者姓名
    author_email='wangzhiqiang@tgqs.net',  # 作者邮箱
    license='MIT',  # 许可证
    package=find_packages(),
    include_package_data=True,
    packages=["QuantumCircuit", "QuantumCircuit.GateSimulation"],
    install_requires=[
        'numpy==1.24.3',
        'numba==0.58.1',
        'matplotlib==3.7.1',
    ],
    classifiers=[
    'Operating System :: OS Independent',
    'License :: OSI Approved :: MIT License',
    'Programming Language :: Python :: 3',
    ],
)
