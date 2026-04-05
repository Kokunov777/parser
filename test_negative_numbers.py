import sys
sys.path.insert(0, '.')
from src.core.analyzer import scan_rust, TokenType

def test_negative_numbers():
    test_cases = [
        ("-4.2", [TokenType.FLOAT, "-4.2"]),
        ("-42", [TokenType.INTEGER, "-42"]),
        ("-0.5", [TokenType.FLOAT, "-0.5"]),
        ("-.5", [TokenType.FLOAT, "-.5"]),  # возможно ошибка
        ("- 4.2", [TokenType.OPERATOR, "-"]),  # минус как оператор, затем число
        ("-4.", [TokenType.FLOAT, "-4."]),  # точка в конце
        ("-4.2e-10", [TokenType.FLOAT, "-4.2e-10"]),  # научная нотация (не поддерживается)
    ]
    
    for text, expected in test_cases:
        tokens, errors = scan_rust(text)
        print(f"\nInput: '{text}'")
        print(f"Tokens: {len(tokens)}, Errors: {len(errors)}")
        for token in tokens:
            print(f"  {token.type.name:15} '{token.lexeme}'")
        for err in errors:
            print(f"  ERROR line {err.line}:{err.column} {err.message}")
        
        if tokens:
            actual_type = tokens[0].type
            actual_lexeme = tokens[0].lexeme
            if expected[0] == actual_type and expected[1] == actual_lexeme:
                print("  PASS")
            else:
                print(f"  FAIL: expected {expected[0].name} '{expected[1]}', got {actual_type.name} '{actual_lexeme}'")
        else:
            print("  No tokens")

if __name__ == "__main__":
    test_negative_numbers()