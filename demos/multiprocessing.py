"""Multiprocessing Example

Illustrates transaction-safety: multiple workers in separate
processes can run processors on the same database.
"""

from sisyphos import Sisyphos, Processor, Slot, Task

import json
import os
import sqlalchemy
import multiprocessing
import time

from pathlib import Path

class CubeProcessor(Processor):
	inputs = []
	outputs = ["cubed"]

	def run(self, inputs, outputs):
		outputs.cubed = str(int(inputs.task_input) ** 3)
		# without any sleep here, we will fail with failing to acquire
		# sqlite db locks in some processes due to too much concurrency.
		time.sleep(0.1)


def worker(sis, i):
	show_progress = (i == 0)
	sis.run(show_progress=show_progress)


def run():
	sis = Sisyphos(
		Path(os.environ['HOME']) / "sisyphos-example-multiprocessing.db",
		[
			Slot(name="cubed", sql_name="cb", sql_type=sqlalchemy.Text)
		],
		[
			CubeProcessor(name="cube", sql_name="cb")
		])


	sis.add_tasks([Task(i) for i in range(1000)], show_progress=True)

	print("\nstatus is now:\n")

	sis.print_status()

	print("\nrunning processors.\n")

	processes = []
	for i in range(4):
		p = multiprocessing.Process(target=worker, args=(sis, i))
		p.start()
		processes.append(p)

	for p in processes:
		p.join()

	print("\nstatus is now:\n")

	sis.print_status()

	print("\nresults (sample):\n")

	sis.print_outputs("cube")
