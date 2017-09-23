from functable import FunctionTable

COMMANDS = FunctionTable()


@COMMANDS.register
def list_balances():
    """List all known address balances."""
    raise NotImplementedError(list_balances)
