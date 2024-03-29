from setuptools import setup, find_packages

setup(
    name="my_streamlit_component",
    version="0.1.0",
    author="Charly Wargnier",
    author_email="cwar05@gnail.com",
    description="A custom Streamlit component for Chart.js",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        "streamlit",
        # Any other dependencies your component needs
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
