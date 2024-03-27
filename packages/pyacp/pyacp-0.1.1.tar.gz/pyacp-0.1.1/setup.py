from setuptools import setup, find_packages

setup(
    name='pyacp',
    version='0.1.1',
    author='Li Meng',
    description='python fastdds acp api',
    # packages=['.',"acp_libs","proto"],
    packages=['.',"acp_libs/lib/","acp_idl_base","sf2_alcraft","example"],
    package_data={
        'acp_libs/lib/': ['libacp-c.so'],  # 包含的文件列表
    },
    install_requires=[
        'protobuf==3.19.5',
        'cffi==1.15.1'
    ],
)