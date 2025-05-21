import os
import re
from datasets import Dataset
from tqdm import tqdm

# === REGEXES ===

# Remove line/block comments
comment_re = re.compile(r'--.*?$|{\-.*?\-}', re.MULTILINE | re.DOTALL)


# === 2. Regex to skip unwanted top-level lines
# enleve pas tout je suis pas doué
skip_line_re = re.compile(
    r'^\s*(port\s+module|effect\s+module|module|import)\b.*$',
    re.MULTILINE
)


# Match all top-level code units: type, function, operator, infix
code_unit_re = re.compile(
    r'''
    ^(?:type\s+alias|type)\s+[A-Z][\w]*.*?(?=\n^[^ \t]|\Z)
    |
    ^\([\s\S]+?\)\s*:.*?(?=\n^[^ \t]|\Z)
    |
    ^\([\s\S]+?\)\s*=.*?(?=\n^[^ \t]|\Z)
    |
    ^[a-z_][\w']*\s+.*?=.*?(?=\n^[^ \t]|\Z)
    |
    ^infix\s+(left|right|non)\s+\d+\s+\(.+?\)\s*=\s*.+?(?=\n^[^ \t]|\Z)
    ''',
    re.MULTILINE | re.DOTALL | re.VERBOSE
)

# === HELPERS ===

def remove_comments(code: str) -> str:
    return comment_re.sub('', code)

def extract_code_units(code: str):
    matches = [m.group(0).strip() for m in code_unit_re.finditer(code)]
    return [m.strip() for m in matches if m.strip()]

def remove_excluded_lines(code: str) -> str:
    return skip_line_re.sub('', code)

# === MAIN SCRIPT ===

def collect_code_units(code_root, rm_mod_imp=False):
    all_units = []
    for root, _, files in os.walk(code_root):
        for file in tqdm(files):
            if file.endswith(".elm"):
                path = os.path.join(root, file)
                with open(path, "r", encoding="utf-8", errors="ignore") as f:
                    raw = f.read()
                    no_comments = remove_comments(raw)
                    no_others = remove_excluded_lines(no_comments) if rm_mod_imp else no_comments
                    units = extract_code_units(no_others)
                    for unit in units:
                        all_units.append(unit)
    return all_units

def build_dataset(code_units):
    return Dataset.from_list([{"text": unit} for unit in code_units])

# === RUN ===

elm_dir = "data/files"
clean_mod_imp = False

code_units = collect_code_units(elm_dir, clean_mod_imp)
print(f"Total code units extracted: {len(code_units)}")

dataset = build_dataset(code_units)
dataset.to_json("elm_code_units.jsonl")
