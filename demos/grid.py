"""Grid Example

This example computes all values of x^y for various
combinations of x and y using two different processors
that might need to run on different hardware.

This is a typical setting when doing grid searches over
parameter spaces for Deep Learning.

Hardware A, running processor A', might be able to process
a certain part of the data, while hardware B might be
necessary to process the other part.

To illustrate this point, in this example we differentiate
between processing small results that fit inside a 64-bit
integer, vs. large results that don't.
"""

from sisyphos import Sisyphos, Processor, Slot, Task

import json
import os
import sqlalchemy

from pathlib import Path

from sklearn.model_selection import ParameterGrid


class SmallProcessor(Processor):
	inputs = []
	outputs = ["small_result"]

	def run(self, inputs, outputs):
		params = json.loads(inputs.task_input)
		outputs.small_result = params["x"] ** params["y"]


class LargeProcessor(Processor):
	inputs = []
	outputs = ["large_result"]

	def run(self, inputs, outputs):
		params = json.loads(inputs.task_input)
		outputs.large_result = str(params["x"] ** params["y"])


def run():
	sis = Sisyphos(
		Path(os.environ['HOME']) / "sisyphos-example-grid.db",
		[
			Slot(name="small_result", sql_name="sm", sql_type=sqlalchemy.Integer),
			Slot(name="large_result", sql_name="lg", sql_type=sqlalchemy.Text)
		],
		[
			SmallProcessor(name="small", sql_name="sm"),
			LargeProcessor(name="large", sql_name="lg")
		])

	param_grid = dict(
		x=(1, 2, 3, 4, 5),
		y=(2, 10, 100))

	def choose_processor(params):
		if params["x"] > 1 and params["y"] > 50:
			return "large"
		else:
			return "small"

	def add_tasks():
		tasks = []

		for params in ParameterGrid(param_grid):
			tasks.append(Task(json.dumps(params), processors=[choose_processor(params)]))

		sis.add_tasks(tasks, show_progress=True)

	add_tasks()

	sis.run(show_progress=True)

	sis.print_status()

	sis.print_outputs("small")

	sis.print_outputs("large")
