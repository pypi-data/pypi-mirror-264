from setuptools import setup, find_packages

setup(
    name="my_streamlit_component",
    version="0.0.1",
    author="Charly Wargnier",
    description="A simple Streamlit component",
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        "streamlit",
        # any other packages your component needs
    ],
)
