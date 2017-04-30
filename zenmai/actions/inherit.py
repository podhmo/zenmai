from dictknife.jsonknife.accessor import access_by_json_pointer
from zenmai.decorators import with_context
from zenmai.utils import unquote
from .concat import concat
from .load import load


@with_context
def inherit(ref, context, **kwargs):
    data = context.loader.data
    if "#/" not in ref:
        parent = access_by_json_pointer(data, ref)
    else:
        parent = unquote(load(ref, context))
    return concat([parent, kwargs])