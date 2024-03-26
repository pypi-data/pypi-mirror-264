from setuptools import setup, find_packages

with open("requirements.txt", "r", encoding="utf-8") as fh:
    requirements = fh.read()

setup(
    name='fuyao-debug-app',
    version='0.0.15',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    py_modules=['app'],
    packages=find_packages(),
    include_package_data=True,
    data_files=[('config', ['config/config.properties']),
                ('db', ['config/config.properties'])],
    install_requires=[requirements],
    entry_points='''
        [console_scripts]
        fuyao-debug-app=app:cli
    ''',
)
