from setuptools import setup

if __name__ == "__main__":
    setup(
        version="1.0.0",
        name="pytest-xprocess",
        # this is for GitHub's dependency graph
        install_requires=["pytest>=2.8", "psutil"],
    )
