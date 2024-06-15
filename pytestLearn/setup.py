from setuptools import setup, find_packages

# 从其他文件中读取版本信息，比如 version.py (推荐)
# 这里直接硬编码了版本信息
version = '0.1.0'

setup(
    name='my_package',
    version=version,
    packages=find_packages(),  # 查找当前目录下的所有包
    install_requires=[
        'numpy>=1.19.0',  # 示例依赖项，这里是 numpy
        'pandas>=1.0.0',  # 另一个示例依赖项，这里是 pandas
        # 其他依赖项...
    ],
    # 其他可选参数
    description='My custom Python package',
    long_description='A longer description of my custom Python package',
    long_description_content_type='text/markdown',  # 如果是 Markdown 格式的 long_description
    url='https://github.com/your_username/my_package',
    author='Your Name',
    author_email='your-email@example.com',
    license='MIT',  # 或者其他许可证
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    # 如果你的包包含数据文件或可执行脚本，你可以在这里指定
    # package_data={'my_package': ['data/*.txt']},
    # entry_points={
    #     'console_scripts': [
    #         'my_command = my_package.main:main_func',
    #     ],
    # },
    # 其他参数...
)