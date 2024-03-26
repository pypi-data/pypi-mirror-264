from datetime import date, datetime

import numpy
import pandas
from railib import api
from relationalai.clients.types import ImportSource, ImportSourceFile
from relationalai.clients.client import ResourceProvider
from relationalai.dsl import Graph, RelationRef, build
from relationalai.loaders.loader import TYPE_TO_REL_SCHEMA, Loader, compute_file_hash, compute_str_hash
from relationalai.rel_utils import assert_no_problems, emit_nested_relation
from relationalai.loaders.types import Schema
from relationalai.metamodel import ActionType, Builtins, Var
from relationalai.rel import sanitize
from relationalai.std import rel


def df_type(df_type_name):
    match df_type_name:
        case "bool":
            type = Builtins.Bool
        case "int64":
            type = Builtins.Number
        case "float64":
            type = Builtins.Number
        case _:
            type = Builtins.String
    return type

class ExternalRow:
    def __init__(self, data, columns):
        self._data = data
        self._columns = columns

    def __getitem__(self, index):
        if isinstance(index, str):
            return getattr(self, index)
        return self._data[index]

    def __getattribute__(self, name):
        if name in ["_data", "_columns"]:
            return object.__getattribute__(self, name)
        if name in self._columns:
            return self._data[self._columns.index(name)]
        return object.__getattribute__(self, name)

# See https://pandas.pydata.org/docs/reference/api/pandas.read_csv.html
# for keyword arg docs.
def load_file(graph:Graph, csv_file, **kwargs):
    df = pandas.read_csv(csv_file, **kwargs)

    # create subqueries for each column that consist of a data object
    # and a bind for the column relation, also create a data ref
    # add a range for the id
    # when a dataref is used, it should add a get for the column relation
    # the rest just works?

    id = rel.range(0, len(df), 1)
    items = []
    for col in df.columns:
        sub = df[[col]]
        col_type = df_type(df[col].dtype)
        with graph.scope(dynamic=True):
            # By setting Builtins.RawData on the task, we're telling the denester to not
            # put a reference to the parent scope in this one
            graph._stack.active()._task.parents.append(Builtins.RawData)
            v1 = []
            v2 = []
            for (i, v) in sub.itertuples():
                if v is not None and v != "" and v is not False and (isinstance(v,str) or isinstance(v, date) or isinstance(v, datetime) or not numpy.isnan(v)):
                    v1.append(i)
                    v2.append(v)

            v1_var = Var(type=Builtins.Number)
            v2_var = Var(name=col, type=col_type)
            graph._action(
                build.relation_action(ActionType.Get, Builtins.RawData, [Var(value=v1), Var(value=v2), v1_var, v2_var])
            )
            temp = build.relation(sanitize(csv_file) + "_" + col, 2)
            graph._action(
                build.relation_action(ActionType.Bind, temp, [v1_var, v2_var])
            )
            usage_var = Var(name=col, type=col_type)
            items.append(RelationRef(graph, temp, [id, usage_var]))

    return ExternalRow(items, [c for c in df.columns])

class CSVLoader(Loader):
    """Load CSV files and URLs in RAI DB using `load_csv`."""
    type = "csv"

    def load(self, provider: ResourceProvider, model: str, source: ImportSource, *, schema: Schema|None = None, syntax: dict|None = None):
        assert isinstance(source, ImportSourceFile), "CSV Loader can only load from files and URLs, not {type(source).__name__}"

        id = compute_str_hash(source.raw_path)
        prefix = f"""def config:path = "{source.raw_path}" """
        inputs = None

        if not source.is_url():
            # We can infer the schema and do proper content hashing for local files
            if not schema:
                schema, _ = self.guess_schema(source.raw_path, syntax)
            with open(source.raw_path, "r") as csv_file:
                data = csv_file.read()

            id = compute_file_hash(source.raw_path)
            prefix = "def config:data = data"
            inputs = {"data": data}

        relation = sanitize(source.name)
        schema = schema or {}

        q = f"""
        {prefix}
        {emit_nested_relation("config:syntax", syntax, api._syntax_options)}
        {emit_nested_relation("config:schema", {col: TYPE_TO_REL_SCHEMA.get(type, "string") for col, type in schema.items()})}
        {emit_nested_relation("insert:__resource", {
        "id": (relation, id),
        "type": (relation, self.type),
        "name": (relation, source.name)
        })}
        def insert:__resource:schema = "{relation}", config:schema
        def insert:{relation} = load_csv[config]
        """
        q = "\n".join(line.strip() for line in q.splitlines())
        res = provider.exec_raw(model, provider.get_default_engine(), q, readonly=False, inputs=inputs)
        assert_no_problems(res)

    @classmethod
    def guess_schema(cls, path: str, syntax: dict|None = None):
        """Guess the schema by reading a chunk of the file."""
        # @TODO: should map the rel syntax settings to pandas probably?
        # @TODO: pick an appropriate magic number of rows to consider for type information.
        chunk = pandas.read_csv(path, nrows=100)
        chunk = chunk.rename(columns={k: k.strip() for k in chunk.columns})
        schema = Schema()
        for col in chunk.columns:
            schema[col] = df_type(chunk[col].dtype)
        return schema, chunk

CSVLoader.register_for_extensions(".csv")
