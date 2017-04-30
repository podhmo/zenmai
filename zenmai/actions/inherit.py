from dictknife.jsonknife.accessor import access_by_json_pointer
from dictknife import deepmerge
from zenmai.decorators import with_context
from zenmai.utils import unquote
from .load import load


@with_context
def inherit(ref, context, **kwargs):
    data = context.loader.data
    if ref.startswith("#/"):
        parent = access_by_json_pointer(data, ref[1:])
    else:
        parent = unquote(load(ref, context))
    return deepmerge(parent, kwargs, override=True)
