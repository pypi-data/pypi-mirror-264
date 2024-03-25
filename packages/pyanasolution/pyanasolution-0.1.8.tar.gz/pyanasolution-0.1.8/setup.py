import setuptools

setuptools.setup(
    name="pyanasolution",
    version="0.1.8",
    author="P. Hong & F.Y. Zhao",
    author_email="frankhp@163.com",
    description="A calculation tool for common analytical solutions.",
    url="https://gitee.com/geo-tech/py-ana-solution",
    packages=setuptools.find_packages(),
    install_requires=[
        "numpy>=1.18.0",
        "scipy>=1.10.1",
    ],
    python_requires=">=3.6"
)

# python setup.py sdist bdist_wheel
# twine upload dist/*
