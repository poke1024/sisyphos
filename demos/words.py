"""Words Example

Shows a two-stage pipeline, that first tokenizes a text and then counts
tokens in that tokenized version.
"""

from sisyphos import Sisyphos, Processor, Slot, Task

import json
import os
import sqlalchemy

from pathlib import Path

class WordSplitProcessor(Processor):
	inputs = []
	outputs = ["tokens"]

	def run(self, inputs, outputs):
		outputs.tokens = json.dumps(inputs.task_input.split())


class WordCountProcessor(Processor):
	inputs = ["tokens"]
	outputs = ["word_count"]

	def run(self, inputs, outputs):
		outputs.word_count = len(json.loads(inputs.tokens))


def run():
	sis = Sisyphos(
		Path(os.environ['HOME']) / "sisyphos-example-words.db",
		[
			Slot(name="tokens", sql_name="tk", sql_type=sqlalchemy.Text),
			Slot(name="word_count", sql_name="wc", sql_type=sqlalchemy.Integer)
		],
		[
			WordSplitProcessor(name="split_words", sql_name="psp"),
			WordCountProcessor(name="count_words", sql_name="pwc")
		])


	print("adding tasks.\n")

	sis.add_tasks([
		Task("the fat cat on the mat"),
		Task("the giant lion")])

	print("running processors.\n")

	sis.run()

	print("status is now:\n")

	sis.print_status()

	print("\nresults:\n")

	sis.print_outputs("count_words")
