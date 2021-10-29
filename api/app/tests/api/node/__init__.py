INVALID_CREATE_FIELDS = [
    ("directives", 123),
    ("directives", ""),
    ("directives", "abc"),
    ("directives", [123]),
    ("directives", [None]),
    ("directives", [""]),
    ("directives", ["abc", 123]),
    ("tags", 123),
    ("tags", ""),
    ("tags", "abc"),
    ("tags", [123]),
    ("tags", [None]),
    ("tags", [""]),
    ("tags", ["abc", 123]),
    ("threat_actor", 123),
    ("threat_actor", ""),
    ("threats", 123),
    ("threats", ""),
    ("threats", "abc"),
    ("threats", [123]),
    ("threats", [None]),
    ("threats", [""]),
    ("threats", ["abc", 123]),
]


INVALID_UPDATE_FIELDS = [
    ("directives", 123),
    ("directives", ""),
    ("directives", "abc"),
    ("directives", [123]),
    ("directives", [None]),
    ("directives", [""]),
    ("directives", ["abc", 123]),
    ("tags", 123),
    ("tags", ""),
    ("tags", "abc"),
    ("tags", [123]),
    ("tags", [None]),
    ("tags", [""]),
    ("tags", ["abc", 123]),
    ("threat_actor", 123),
    ("threat_actor", ""),
    ("threats", 123),
    ("threats", ""),
    ("threats", "abc"),
    ("threats", [123]),
    ("threats", [None]),
    ("threats", [""]),
    ("threats", ["abc", 123]),
]


NONEXISTENT_FIELDS = [
    ("directives", ["abc"]),
    ("tags", ["abc"]),
    ("threat_actor", "abc"),
    ("threats", ["abc"]),
]


VALID_DIRECTIVES = [
    ([]),
    (["test"]),
    (["test1", "test2"]),
    (["test", "test"]),
]


VALID_TAGS = [
    ([]),
    (["test"]),
    (["test1", "test2"]),
    (["test", "test"]),
]


VALID_THREAT_ACTOR = [
    (None),
    ("test"),
]


VALID_THREATS = [
    ([]),
    (["test"]),
    (["test1", "test2"]),
    (["test", "test"]),
]
