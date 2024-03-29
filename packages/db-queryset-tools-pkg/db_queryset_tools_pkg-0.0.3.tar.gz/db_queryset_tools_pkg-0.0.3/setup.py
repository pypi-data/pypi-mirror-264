import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()
    
setuptools.setup(
    name="db_queryset_tools_pkg", 
    version="0.0.3",
    author="Hariharan Sathiyamoorthy",
    author_email="hari.rn03@gmail.com",
    description="A package to convert Django Queryset to list, dictionary, json and dataset for charts",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/Hariharan-Sathiyamoorthy/db_queryset_tools",
    packages=setuptools.find_packages(),
    # if you have libraries that your module/package/library
    #you would include them in the install_requires argument
    install_requires=['Django'],
    classifiers=[
    "Programming Language :: Python :: 3",
    "License :: OSI Approved :: MIT License",
    "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)