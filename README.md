A small, versatile, no-nonsense solution for simple batches.

* support for multiple processing stages
* support for simple DAG data flow pipelines
* concurrent (e.g. runs in multiple processes)
* robust interrupt and resume (i.e. sound transactions)

# Caveats

Never change sql_names or processors/slots after you've started
running your batches. This will break everything. You will have
to recompose your data manually directly from the sqlite3 db. In
fact, Sisyphos should usually detect this and will deny to run.

Sisyphos has some rudimentary support for adding new processors
and slots using migrations (see the CLI demo), but this is not
very thoroughly tested and needs to be used very carefully.

# License

MIT.
