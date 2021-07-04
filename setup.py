from setuptools import setup, find_packages

setup(
    name='sclexer',
    packages=find_packages(),
    entry_points="""
  [pygments.lexers]
  sclexer = sclexer.lexer:SCLexer
  """,
)
