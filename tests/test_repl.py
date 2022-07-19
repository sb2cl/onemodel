from onemodel.repl import Repl


def test_init():
    result = Repl()
    assert isinstance(result, Repl)

def test_read(monkeypatch):
    # Use a monkeypatch to replace the builtin input function for testing.

    repl = Repl()

    text = "parameter foo"
    monkeypatch.setattr('builtins.input', lambda _: text)
    result = repl.read()
    assert result == "parameter foo"

    text = ""
    monkeypatch.setattr('builtins.input', lambda _: text)
    result = repl.read()
    assert result == None

    text = "     "
    monkeypatch.setattr('builtins.input', lambda _: text)
    result = repl.read()
    assert result == None

def test_evaluate():
    text = """parameter foo = 10"""

    repl = Repl()
    repl.evaluate(text)

    assert repl.onemodel["foo"]["value"] == 10

def test_print():
    repl = Repl()
    result = repl.print("<parameter foo>")
    assert result == "<parameter foo>"
