import setuptools

with open('./README.md','r',encoding='utf-8')as md:
    long_description=md.read()

setuptools.setup(
    name="MiaoPinYin",
    version="0.0.3",
    author="MiaoMiaoLWY",
    author_email="1545113791@qq.com",
    description="简单的中文播放",
    long_description=long_description,
    long_description_content_type='text/markdown',
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent"
    ],
    install_requires=[
        'pypinyin',
        'playsound==1.2.2'
    ],
)
