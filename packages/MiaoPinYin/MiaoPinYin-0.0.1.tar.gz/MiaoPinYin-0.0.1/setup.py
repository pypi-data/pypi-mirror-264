import setuptools

setuptools.setup(
    name="MiaoPinYin",
    version="0.0.1",
    author="MiaoMiaoLWY",
    author_email="1545113791@qq.com",
    description="简单的中文播放",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent"
    ],
    install_requires=[
        'pypinyin',
        'playsound'
    ],
)
