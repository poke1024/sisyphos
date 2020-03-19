import demos.large
import demos.words
import demos.grid
import demos.multiprocessing
import demos.cli

import sys

if len(sys.argv) != 2:
	print("please specify which demo to run, e.g. 'words'.")
	sys.exit(1)

demo_name = sys.argv[1]
demo_module = getattr(demos, demo_name)

if demo_module:
	demo_module.run()
	sys.exit(0)
else:
	print("unknown demo %s" % demo_name)
	sys.exit(1)
