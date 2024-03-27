from setuptools import setup, find_packages

setup(
    name='pyacp',
    version='0.1.2',
    author='Li Meng',
    description='python fastdds acp api',
    # packages=['.',"acp_libs","proto"],
    packages=['.',"acp_libs/lib/","acp_libs/lib/linux/","acp_libs/lib/win/","acp_idl_base","sf2_alcraft","example"],
    package_data={
        'acp_libs/lib/linux/': ['libacp-c.so','libacp.so','libacp.sp'],  # 包含的文件列表
        'acp_libs/lib/win/' : ['acp.dll','acp-core.dll']
    },
    install_requires=[
        'protobuf==3.19.5',
        'cffi==1.15.1'
    ],
)