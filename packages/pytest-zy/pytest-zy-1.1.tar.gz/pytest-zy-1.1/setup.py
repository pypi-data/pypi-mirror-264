from setuptools import setup, find_packages

with open('requirements.txt') as f:
    install_requires = f.read().splitlines()
setup(
    name="pytest-zy",
    version="1.1",
    author="浪浪",
    author_email="zy1834529768@gmail.com",
    description="接口自动化测试框架",
    long_description="apitest",
    long_description_content_type="text/markdown",
    url="",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.10",
    packages=find_packages(),
    install_requires=install_requires,
    entry_points={
        "pytest11": [
            "pytest-zy = pytest_zy.plugin"
        ]
    }
)
