import setuptools
import os
import io

long_description = 'Aiy worker'
  
if os.path.exists("requirements.txt"):
    install_requires = [i for i in io.open("requirements.txt").read().split("\n") if i]
else:
    install_requires = []
print(install_requires)
setuptools.setup(
    name="aiy_worker",
    version="0.0.1",
    author="zgljl2012",
    # license = 'MIT License',
    # author_email="pengshiyuyx@gmail.com",
    description="aiy worker",
    long_description=long_description,
    # long_description_content_type="text/x-rst",
    # url="https://github.com/mouday/chinesename",
    packages=setuptools.find_packages(),
    classifiers=(
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ),
    install_requires = install_requires,
    # include_package_data=True,  # 自动打包文件夹内所有数据
    # 如果需要包含多个文件可以单独配置 MANIFEST.in
    package_data = {
            # If any package contains *.txt or *.rst files, include them:
            'aiy_worker': [],
    },
    # 如果需要支持脚本方法运行，可以配置入口点
    # entry_points={
    #     'console_scripts': [
    #         'chinesename = chinesename.run:main'
    #     ]
    # }
)
