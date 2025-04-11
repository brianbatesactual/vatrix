import sys

if not (3, 9) <= sys.version_info < (3, 10):
    sys.stderr.write("❌ Vatrix requires Python 3.9.x. Please use Python 3.9.\n")
    sys.exit(1)
