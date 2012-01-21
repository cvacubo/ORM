import sys

try:
    import nose
except ImportError:
    print ('nose is required to run unit test suite')
    sys.exit(1)

print ('ORM test suite running (Python %s)...' % sys.version.split()[0])

nose.main()