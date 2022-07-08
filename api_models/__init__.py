from pydantic import conint, conlist, constr, ConstrainedStr, ConstrainedInt


type_int = conint(strict=True)

type_str = constr(strict=True, min_length=1)

type_list_str = conlist(type_str, min_items=1)


class TypeInt(ConstrainedInt):
    strict = True


class TypeStr(ConstrainedStr):
    min_length = 1
    strict = True
