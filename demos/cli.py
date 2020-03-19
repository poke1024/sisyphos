"""CLI Example

A simple command line interface, useful for experimenting with the API.
"""

from sisyphos import Sisyphos, Processor, Slot, Task, InterruptedException

import json
import os
import sqlalchemy
import argparse
import cmd
import sys
import math
import cli_ui

from pathlib import Path

class CubeProcessor(Processor):
	inputs = []
	outputs = ["cube"]

	def run(self, inputs, outputs):
		outputs.cube = str(int(inputs.task_input) ** 3)


class SqrtProcessor(Processor):
	inputs = []
	outputs = ["sqrt"]

	def run(self, inputs, outputs):
		outputs.sqrt = str(math.sqrt(int(inputs.task_input)))


def processor_names(p):
	if not p:
		return "all"
	else:
		return p


class SisyphosShell(cmd.Cmd):
	intro = 'Welcome to the sisyphois shell.   Type help or ? to list commands.\n'
	prompt = '(sisyphos) '
	file = None

	def __init__(self, sis):
		super().__init__()
		self._sis = sis

	def do_status(self, arg):
		'Show current status of all processors.'
		self._sis.print_status()

	def do_run(self, arg):
		'Run all processors.'
		try:
			self._sis.run(show_progress=True)
		except InterruptedException as e:
			pass

	def do_show(self, processor):
		'Show results for one processor.'
		processor = cli_ui.ask_choice("Pick a processor", choices=self._sis.processors)
		self._sis.print_outputs(processor, up_to=10)

	def do_reset(self, processor):
		'Reset failed tasks for one processor.'
		processor = cli_ui.ask_choice(
			"Pick a processor to reset", choices=self._sis.processors)
		self._sis.reset([processor])
		print("done.")

	def do_reset_hard(self, processor):
		'Reset failed and done tasks for one processor.'
		if cli_ui.ask_yes_no("Are you sure you want to delete all computed data?", default=False):
			processor = cli_ui.ask_choice(
				"Pick a processor to reset", choices=self._sis.processors)
			self._sis.reset([processor], reset_hard=True)
			print("done.")

	def do_migrate(self, arg):
		'Migrate to a new set of slots of processor after you have changed things (experimental).'
		self._sis.migrate()
		print("done.")

	def do_quit(self, arg):
		'Quit the CLI.'
		sys.exit(0)

	def do_exit(self, arg):
		'Quit the CLI.'
		sys.exit(0)


def run():
	sis = Sisyphos(
		Path(os.environ['HOME']) / "sisyphos-example-cli.db",
		[
			Slot(name="cube", sql_name="cb", sql_type=sqlalchemy.Integer),
			Slot(name="sqrt", sql_name="sq", sql_type=sqlalchemy.Float)
		],
		[
			CubeProcessor(name="cube", sql_name="cb"),
			SqrtProcessor(name="sqrt", sql_name="sq")
		])

	if sis.needs_migration():
		SisyphosShell.intro = SisyphosShell.intro + "\nYour schema has changed. Please run MIGRATE."
	else:
		sis.add_tasks([Task(i) for i in range(1000)], show_progress=False)

	SisyphosShell(sis).cmdloop()
