from setuptools import setup, find_packages
setup(
   name='func_runner_cli',
   version='0.1.3',
   python_requires='>=3.7',
   packages=find_packages(),
   install_requires=[
      'typer>=0.9.0',  # Assuming you want to match the version specified in Poetry
      'pyyaml>=6.0.1',
      'pydantic>=2.6.4',
      'pydantic-settings>=2.2.1',
      'requests>=2.31.0',
   ],
   entry_points='''
      [console_scripts]
      funcrunner=func_runner_cli.main:app
      ''',
)