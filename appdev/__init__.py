__version__ = '0.0.1'
__all__ = [
  basename(f)[:-3]
  for f in modules if isfile(f) and not f.endswith('__init__.py')
]
USER_AGENT = 'AppDev Core Modules %s' % __version__
