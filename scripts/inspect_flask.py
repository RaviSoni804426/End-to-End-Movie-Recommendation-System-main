import sys, traceback, pkgutil
print('SYS.PATH:')
for p in sys.path:
    print(p)
print('\npkgutil.find_loader("flask") ->', pkgutil.find_loader('flask'))
try:
    import flask
    print('\nflask module:', flask)
    print('__file__:', getattr(flask,'__file__',None))
    print('__package__:', getattr(flask,'__package__',None))
    print('dir(flask) sample:', list(dir(flask))[:20])
except Exception as e:
    traceback.print_exc()
    print('Import error:', e)
