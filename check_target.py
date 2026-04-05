import sys
sys.path.insert(0, '.')
from src.core.analyzer import scan_rust, TokenType

text = "let complex_num2 = num::complex::Complex::new(3.1, -4.2);"
tokens, errors = scan_rust(text)

print("Анализ строки:")
print(repr(text))
print("\nРаспознанные лексемы:")
for i, token in enumerate(tokens):
    print(f"{i:2}: {token.type.name:20} '{token.lexeme}' ({token.start_line}:{token.start_col}-{token.end_line}:{token.end_col})")

print("\nОшибки:")
for err in errors:
    print(f"  {err.line}:{err.column} {err.message}")

# Проверка конкретно лексемы -4.2
float_tokens = [t for t in tokens if t.type == TokenType.FLOAT]
print("\nВещественные числа:")
for t in float_tokens:
    print(f"  {t.lexeme}")

# Убедимся, что -4.2 присутствует
if any(t.lexeme == "-4.2" for t in tokens):
    print("\nЛексема -4.2 корректно распознана.")
else:
    print("\nОШИБКА: Лексема -4.2 не найдена")
    sys.exit(1)