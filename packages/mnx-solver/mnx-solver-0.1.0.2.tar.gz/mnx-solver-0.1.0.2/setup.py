from setuptools import setup, find_packages

setup(
    name='mnx-solver',
    packages=find_packages(),
    version='0.1.0.2',
    description='A method numerical analysis package',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    author='0xCamiX',
    author_email='juancamilogallego70@icloud.com',
    # Use the URL to the GitHub repo.
    url='https://github.com/0xCamiX/mnx',
    download_url='https://github.com/0xCamiX/mnx/archive/refs/heads/main.zip',
    keywords=['numerical', 'analysis', 'math', 'methods'],
    classifiers=[],
    license='MIT',
    install_requires=[
        'numpy',
        'scipy',
    ],
    include_package_data=True
)
