def run_python(code: str, context: dict = None):
    context = context or {}
    exec(code, context)
    return context