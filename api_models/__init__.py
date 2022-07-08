from pydantic import conint, conlist, constr


type_int = conint(strict=True)

type_str = constr(strict=True, min_length=1)

type_list_str = conlist(type_str, min_items=1)
