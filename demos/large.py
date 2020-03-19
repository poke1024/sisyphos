"""Large Example

Experiments with adding a larger number of tasks. You can try to
abort the run and resume it later.
"""

from sisyphos import Sisyphos, Processor, Slot, Task

import json
import os
import sqlalchemy

from pathlib import Path

class CubeProcessor(Processor):
	inputs = []
	outputs = ["cubed"]

	def run(self, inputs, outputs):
		outputs.cubed = str(int(inputs.task_input) ** 3)


def run():
	sis = Sisyphos(
		Path(os.environ['HOME']) / "sisyphos-example-large.db",
		[
			Slot(name="cubed", sql_name="cb", sql_type=sqlalchemy.Text)
		],
		[
			CubeProcessor(name="cube", sql_name="cb")
		])


	sis.add_tasks([Task(x) for x in range(10000)], show_progress=True)

	print("\nrunning processors.\n")

	sis.run(show_progress=True)

	print("\nstatus is now:\n")

	sis.print_status()

	print("\nresults (sample):\n")

	sis.print_outputs("cube")
