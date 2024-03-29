from setuptools import setup, find_packages

setup(
    name="GriffinX",
    version="0.1",
    packages=find_packages(),
    install_requires=[
        # List your project's dependencies here.
        # For example: 'numpy>=1.18.1'
        "torch",
        "numpy",
        "PIL",
        "os",
        "ultralytics"
        "cv2"
    ],
    # Metadata
    author="Percom@UMD",
    author_email="kirandav@umich.edu",
    description="GriffinX is a middleware package for real time event detection",
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',  # This is important for making the README render correctly on PyPI
    url="https://github.com/kiran-collab/Griffin-Drone-Car-Collaboration",
    license="MIT",
    classifiers=[
        # Trove classifiers
        # Full list: https://pypi.org/classifiers/
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
    ],
)