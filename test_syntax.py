"""
Тестирование синтаксического анализатора.
"""
import sys
sys.path.insert(0, '.')
from src.core.analyzer import scan_rust
from src.core.syntax_analyzer import parse_syntax


def test_correct():
    """Корректная строка."""
    text = "let complex_num2 = num::complex::Complex::new(3.1, -4.2);"
    tokens, lex_errors = scan_rust(text)
    print(f"Лексических ошибок: {len(lex_errors)}")
    syntax_errors = parse_syntax(tokens)
    print(f"Синтаксических ошибок: {len(syntax_errors)}")
    if syntax_errors:
        for err in syntax_errors:
            print(f"  {err.line}:{err.column} {err.message} ({err.fragment})")
        raise AssertionError("Ожидалось отсутствие синтаксических ошибок")
    print("✓ Корректная строка прошла анализ")


def test_missing_semicolon():
    """Отсутствует точка с запятой."""
    text = "let x = num::complex::Complex::new(1.0, 2.0)"
    tokens, _ = scan_rust(text)
    syntax_errors = parse_syntax(tokens)
    print(f"Синтаксических ошибок (нет ;): {len(syntax_errors)}")
    if syntax_errors:
        print("  Ошибки:", [err.message for err in syntax_errors])
    else:
        print("  (ожидалась ошибка отсутствия ;)")


def test_missing_let():
    """Отсутствует ключевое слово let."""
    text = "x = num::complex::Complex::new(1.0, 2.0);"
    tokens, _ = scan_rust(text)
    syntax_errors = parse_syntax(tokens)
    print(f"Синтаксических ошибок (нет let): {len(syntax_errors)}")
    if syntax_errors:
        print("  Ошибки:", [err.message for err in syntax_errors])
    else:
        print("  (ожидалась ошибка отсутствия let)")


def test_wrong_path():
    """Неправильный путь (двоеточие вместо двойного двоеточия)."""
    text = "let x = num:complex::Complex::new(1.0, 2.0);"
    tokens, _ = scan_rust(text)
    syntax_errors = parse_syntax(tokens)
    print(f"Синтаксических ошибок (неправильный путь): {len(syntax_errors)}")
    if syntax_errors:
        print("  Ошибки:", [err.message for err in syntax_errors])
    else:
        print("  (ожидалась ошибка пути)")


def test_multiple_errors():
    """Несколько ошибок в одной строке."""
    text = "let = num::complex::Complex::new(,);"
    tokens, _ = scan_rust(text)
    syntax_errors = parse_syntax(tokens)
    print(f"Синтаксических ошибок (множественные): {len(syntax_errors)}")
    if syntax_errors:
        for err in syntax_errors:
            print(f"  {err.line}:{err.column} {err.message}")
    else:
        print("  (ожидались ошибки)")


def test_empty():
    """Пустая строка."""
    text = ""
    tokens, _ = scan_rust(text)
    syntax_errors = parse_syntax(tokens)
    print(f"Синтаксических ошибок (пустая строка): {len(syntax_errors)}")
    # Пустая строка не содержит токенов, анализатор не должен падать


def test_lexical_error():
    """Лексическая ошибка (недопустимый символ)."""
    text = "let x = num@complex::Complex::new(1.0, 2.0);"
    tokens, lex_errors = scan_rust(text)
    print(f"Лексических ошибок: {len(lex_errors)}")
    syntax_errors = parse_syntax(tokens)
    print(f"Синтаксических ошибок после лексических: {len(syntax_errors)}")
    # Синтаксический анализатор должен работать, несмотря на лексические ошибки


def run_all():
    test_correct()
    print()
    test_missing_semicolon()
    print()
    test_missing_let()
    print()
    test_wrong_path()
    print()
    test_multiple_errors()
    print()
    test_empty()
    print()
    test_lexical_error()
    print("\nВсе тесты завершены.")


if __name__ == "__main__":
    run_all()