from sqlalchemy import DateTime
from sqlalchemy.ext.compiler import compiles
from sqlalchemy.sql import expression


# https://docs.sqlalchemy.org/en/14/core/compiler.html#utc-timestamp-function
class utcnow(expression.FunctionElement):
    type = DateTime()


@compiles(utcnow, "postgresql")
def pg_utcnow(element, compiler, **kw):  # pragma: no cover
    return "TIMEZONE('utc', CURRENT_TIMESTAMP)"
