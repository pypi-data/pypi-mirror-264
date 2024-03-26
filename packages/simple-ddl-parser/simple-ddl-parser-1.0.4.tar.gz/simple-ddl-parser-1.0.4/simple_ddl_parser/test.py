from simple_ddl_parser import DDLParser


ddl = """CREATE TABLE a
(
    id UUID PRIMARY KEY
);

CREATE TABLE b
(
    id UUID PRIMARY KEY,
    a_id UUID REFERENCES a(id) NOT NULL
);

"""
result = DDLParser(ddl).run(group_by_type=True)
import pprint

pprint.pprint(result)
