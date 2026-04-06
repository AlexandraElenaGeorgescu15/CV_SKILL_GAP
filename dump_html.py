"""Render blueprint_html to a file so we can inspect the JS."""
import sys, os
sys.path.insert(0, os.path.dirname(__file__))

# Minimal stubs so we can import the blueprint string without running streamlit
import types
st_mock = types.ModuleType("streamlit")
sys.modules["streamlit"] = st_mock
sys.modules["pdfplumber"] = types.ModuleType("pdfplumber")
sys.modules["streamlit.components"] = types.ModuleType("streamlit.components")
sys.modules["streamlit.components.v1"] = types.ModuleType("streamlit.components.v1")

src = open("app.py", encoding="utf-8").read()

# Extract the SYS_PROMPT and blueprint_html as raw text (no execution needed)
# Just look at lines inside the f-string that have suspicious patterns:
# a real Python \n (not \\n) inside a JS single-quoted string continuation

lines = src.split("\n")
fstr_start = next(i for i,l in enumerate(lines) if "blueprint_html = f" in l)

# look through from fstr_start for lines where a ' is followed by \n before closing '
# The dangerous pattern in Python source is when a line ENDS with something like:
#   '...\n' +       <- \n here is a real newline char -> bad in JS
#   vs
#   '...\\n' +      <- \\n renders as \n in JS -> fine

print("Scanning for bare \\n in single-quoted JS strings (lines after f-string start):")
found = False
for i, line in enumerate(lines[fstr_start:], fstr_start + 1):
    # Find single-quoted strings on this line
    # The bug: line has '...:\n' where the \n terminates the Python line
    # In Python source these look like: one backslash followed by n before a quote
    import re
    matches = re.findall(r"'[^'\\]*(?:\\.[^'\\]*)*'", line)
    for m in matches:
        if "\n" in m:  # real newline
            print(f"Line {i}: REAL NEWLINE IN JS STRING: {repr(m[:80])}")
            found = True
    # Also: string ends before content is finished - i.e. line ends with '  +
    if re.search(r"'\\n'\s*\+", line) or re.search(r"explanation:\\n", line):
        print(f"Line {i}: suspicious \\n pattern: {line.rstrip()}")
        found = True

if not found:
    print("None found - the \\n bug is fixed!")
    
# Also render a small test: just find all \n (single backslash-n being real newline)
# inside what would be JS string contexts.
# In Python source the blueprint is f""" so:
# - Lines of text are literally in the f-string
# - A line like:   '...stuff:\n' +   has \n at end BEFORE the end-of-Python-line
# Python interpretes \n within a string literal as newline.
# But wait: in the F-STRING source, \n is NOT inside a Python string - it IS a
# literal backslash-n since the f-string body is treated as a raw text template
# ... actually no! In a Python f-string, \n IS still escape-processed!
# So 'stuff\n' inside the f-string = 'stuff' + newline in the rendered HTML.

# Check all lines in blueprint for unescaped \n that would break JS:
in_scriptblock = False
for i, line in enumerate(lines[fstr_start:], fstr_start + 1):
    if "<script>" in line:
        in_scriptblock = True
    if "</script>" in line:
        in_scriptblock = False
    if not in_scriptblock:
        continue
    # Look for lines that have \n (as \-n) in a JS string - these should be \\n
    # In the Python source: \n = one backslash + n (but Python interprets as newline!)  
    # So we need to look at the RAW source bytes
    raw_bytes = line.encode("utf-8")
    # Check if this line has b'\n' embedded inside a ' string (not \\n)
    # Actually the line already had the \n stripped by split(\n)
    # So we need to look at repr to see if there are \n chars that AREN'T from line endings
    import re
    # Find all JS string literals on this line (single-quoted)
    for m in re.finditer(r"'((?:[^'\\]|\\.)*)'", line):
        content = m.group(1)
        # If content has a real \n character (not \\n), that's the bug
        if "\n" in content:
            print(f"Line {i}: REAL NEWLINE inside JS string literal: {repr(m.group()[:80])}")
            found = True
print("Done")
