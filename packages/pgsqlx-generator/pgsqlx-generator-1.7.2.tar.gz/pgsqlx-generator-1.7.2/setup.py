import os
from setuptools import setup

def read(rel_path: str) -> str:
    here = os.path.abspath(os.path.dirname(__file__))
    # intentionally *not* adding an encoding option to open, See:
    #   https://github.com/pypa/virtualenv/issues/201#issuecomment-3145690
    with open(os.path.join(here, rel_path), 'r', encoding='UTF-8') as fp:
        return fp.read()

long_description = read("README.rst")

setup(
    name='pgsqlx-generator',
    packages=['pgsqlx'],
    description="pgsqlx-generator is a model code generator from tables for PgSqlx.",
    long_description=long_description,
    long_description_content_type='text/markdown',
    install_requires=[
        'pgsqlx>=2.1.1',
    ],
    version='1.7.2',
    url='https://gitee.com/summry/pgsqlx/blob/master/generator.md',
    author='summy',
    author_email='xiazhongbiao@126.com',
    keywords=['PostgreSQL', 'PgSqlx', 'python'],
    package_data={
        # include json and txt files
        '': ['*.rst', '*.dtd', '*.tpl'],
    },
    include_package_data=True,
    python_requires='>=3.5',
    zip_safe=False
)

