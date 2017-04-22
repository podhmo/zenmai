from zenmai.decorators import with_context
from dictknife import Accessor


@with_context
def get(name, context, accessor=Accessor()):
    if "#/" not in name:
        return getattr(context.scope, name)
    else:
        name, path = name.split("#/", 2)
        root = getattr(context.scope, name)
        return accessor.access(root, path.split("/"))
