import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="youtube-community-alarm",
    version="0.0.1",
    author="palace",
    author_email="ufo3764@naver.com",
    description="youtube community alarm package",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/SionByeon/YoutubeCommunityAlarm",
    packages=setuptools.find_packages(),
    python_requires='>=3.6',
)
