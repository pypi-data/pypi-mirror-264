import setuptools
from pkg_resources import parse_version

VERSION = "1.0.0"


# Based on https://github.com/tulip-control/dd/blob/885a716a56e82bfee54b0178d0ce38298b85eb6a/setup.py#L68
def git_version(version):
    """Return version with local version identifier."""
    import git
    repo = git.Repo('.git')
    repo.git.status()
    # assert versions are increasing
    latest_tag = repo.git.describe(
        match='v[0-9]*', tags=True, abbrev=0)
    assert parse_version(latest_tag) <= parse_version(version), (
        latest_tag, version)
    sha = repo.head.commit.hexsha[:8]
    if repo.is_dirty():
        return version
    # commit is clean
    # is it release of `version` ?
    try:
        tag = repo.git.describe(
            match='v[0-9]*', exact_match=True,
            tags=True, dirty=True)
    except git.GitCommandError:
        return '{v}.dev0+{sha}'.format(
            v=version, sha=sha)
    assert tag == 'v' + version, (tag, version)
    return version


with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

with open("docs/requirements.txt", "r") as f:
    requirements = f.read().splitlines()

# Get version
VERSION_FILE = 'regmapGen/_version.py'
try:
    version = git_version(VERSION)
except AssertionError:
    print('No git info: Assume release.')
    version = VERSION
with open(VERSION_FILE, 'w') as f:
    f.write("version = '%s'\n" % version)

# Install package
setuptools.setup(
    name="regmapGen",
    version=version,
    author="paulmsv",
    author_email="bobkovpg@gmail.com",
    description="Генератор Регистровой Карты",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/paulmsv/regmapGen",
    project_urls={
        'Documentation': 'https://regmapGen.readthedocs.io'
    },
    packages=setuptools.find_packages(exclude='tests'),
    package_data={'regmapGen': ['templates/*.j2']},
    entry_points={
        'console_scripts': [
            'regmapGen = regmapGen.__main__:main',
        ],
    },
    install_requires=requirements,
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)

# Clear version info
with open(VERSION_FILE, 'w') as f:
    f.write("")
