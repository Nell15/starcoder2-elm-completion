import re
from pathlib import Path

# Parse type signatures (e.g., "myFunction : Int -> String")
def parse_type_signature(line):
    return re.compile(r"^[a-z][a-zA-Z0-9_]*\s*:\s*.+$", re.MULTILINE).match(line)

# Parse function definitions (e.g., "myFunction x = x + 1")
def parse_function_definition(line):
    return re.compile(r"^[a-z][a-zA-Z0-9_]*\s+.*=\s*([\s\S]*?)(?=^[a-z]|^module|^import|^--|$)", re.MULTILINE).match(line)

# Parse module declarations
def parse_module_declaration(line):
    return re.compile(r"^module\s+[A-Z][a-zA-Z0-9_.]*(\s+exposing\s+\(.*\))?$", re.MULTILINE).match(line)

# Parse import statements (e.g., "import MyModule exposing (..)")
def parse_import(line):
    return re.compile(r"^import\s+[A-Z][a-zA-Z0-9_.]*(\s+as\s+[A-Z][a-zA-Z0-9_.]*)?(\s+exposing\s+\(.*\))?$", re.MULTILINE).match(line)

# Parse comments (e.g., "-- This is a comment")
def parse_comment(line):
    return re.compile(r"^--.*$", re.MULTILINE).match(line)

# Parse multiline comments
def parse_multiline_comment(line):
    return re.compile(r"{-(.*?)\s*-}", re.MULTILINE).match(line)

def parse_line(line):
    if (not (
        parse_type_signature(line)
        or parse_function_definition(line)
        or parse_module_declaration(line)
        or parse_import(line)
        or parse_comment(line)
        or parse_multiline_comment(line)
    )):
        return False, f"Invalid syntax : `{line}`"
    return True, "Valid syntax"

def parse_elm(code):
    # Check for empty code
    if not code:
        return False, "Empty code"

    # Remove line breaks only in multiline comments
    code = re.sub(r"{-(.*?)\s*-}", lambda m: "{- " + ' '.join(m.group(1).splitlines()) + " -}", code, flags=re.DOTALL)

    # Remove line breaks after function definitions
    code = re.sub(r"([a-zA-Z0-9_]+)\s*=\s*([\s\S]*?)(?=^[a-z]|^module|^import|^--|$)", lambda m: m.group(1) + " = " + ' '.join(m.group(2).splitlines()), code, flags=re.MULTILINE)

    # Pase each line of code
    for line_number, line in enumerate(code.splitlines(), start=1):
        # Remove leading and trailing whitespace
        line = line.strip()
        if not line:
            continue
        # Parse the line
        is_valid, message = parse_line(line)
        if not is_valid:
            return False, f"{message}"
    return True, "Valid Elm code"

def read_elm_files():
    elm_files = []
    for filepath in Path("data/files").rglob("*.elm"):
        with open(filepath, 'r', encoding='utf-8') as f:
            elm_files.append((filepath.name, f.read()))
    return elm_files

if __name__ == "__main__":
    elm_files = read_elm_files()
    for filename, code in elm_files[:20]:
        is_valid, message = parse_elm(code)
        if not is_valid:
            print(f"File {filename} is not valid Elm code. Error: {message}")
        else:
            print(f"File {filename} is valid Elm code.")