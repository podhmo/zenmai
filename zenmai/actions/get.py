from zenmai.decorators import with_context


@with_context
def get(name, context):
    return getattr(context.scope, name)
