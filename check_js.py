"""Find bare newlines inside JS string literals in the blueprint f-string."""
import re

src = open("app.py", encoding="utf-8").read()

# Extract blueprint_html content
start = src.index("blueprint_html = f")
end   = src.index("\n    # --- KEY ENTRY", start)
fstr  = src[start:end]

print(f"Blueprint f-string: {len(fstr)} chars\n")

# Each line of the fstr that ends without closing a JS string AND has a real newline
lines = fstr.split("\n")
for i, line in enumerate(lines, 1):
    # A line that starts mid-JS-string (common pattern: line continuations with +)
    # Look for a line that has a closing quote followed by +  but also a \n in it
    # Simplest: look for a single-quoted string that SPANS a newline (i.e. is open)
    # Count unescaped single quotes on this line to see if it's odd
    pass

# Better: simulate what the f-string renders and look for newlines in JS strings
# In the Python source, sequences like \n (single backslash-n) inside the f-string
# become real newlines in the output. \\n becomes \n (literal backslash-n) in output.
# JS strings cannot contain raw newlines - they need \n or \u000a

# Find all occurrences of a single quote followed eventually by a real newline
# before the closing quote
in_fstr = fstr

# Look for the pattern: ' at start of JS string arg, then \n before '
# Python repr helps see escaping
problem_lines = []
for i, line in enumerate(src.split("\n"), 1):
    if i < src[:start].count("\n") + 1:
        continue
    if i > src[:end].count("\n") + 1:
        break
    # a real \n in source = single backslash-n in a string = newline in rendered output
    # This is harmful inside a JS string
    stripped = line.rstrip("\n")
    # Check if this line ends with a single-quoted string that isn't closed
    # i.e. it has content like '...stuff\n' where \n is terminator of Python line
    # The tell-tale: line ends with '\n' +  or has a bare newline-ending string
    
    # Simple flag: if the line contains a JS string-continuation marker and the 
    # raw Python line includes characters that would break JS
    if "explanation:\\n'" in stripped or ("'\\n'" in stripped and "explanation" in stripped):
        problem_lines.append((i, stripped))

if problem_lines:
    print("Found problem lines (old \\n issue):")
    for ln, content in problem_lines:
        print(f"  Line {ln}: {content}")
else:
    print("No explanation:\\n issues found.")

# Also check: any string ending in \n' in the Python source within the fstr
# This means the JS string contains a literal newline 
raw_py_lines = src.split("\n")
fstr_line_start = src[:start].count("\n") + 1
fstr_line_end   = src[:end].count("\n") + 1

print(f"\nBlueprint runs from line {fstr_line_start} to {fstr_line_end}")
print("\nLines with possible bare newline in JS string (end with :\\n' or similar):")
for i in range(fstr_line_start, fstr_line_end + 1):
    line = raw_py_lines[i - 1] if i <= len(raw_py_lines) else ""
    # Pattern: string that ends with \n followed by quote
    # In Python source \n is two chars: backslash + n
    # But a *real* newline (the line ending itself) inside a JS quoted string is the bug
    # Those look like:  '...[end of line]
    # That means the JS string is still "open" at end of line, which is a SyntaxError
    # Look for lines within JS context that have an unclosed single quote
    # Very rough: if the line (inside JS) ends with  +   or ends with  '  where quotes are odd
    pass

print("\n--- Checking for lines ending with open JS string (unclosed quote) ---")
# A simpler check: render similar to what Python would and look for lines with odd quotes
for i in range(fstr_line_start, min(fstr_line_end, fstr_line_start + 600)):
    py_line = raw_py_lines[i - 1] if i <= len(raw_py_lines) else ""
    # After f-string processing: {{ -> {, }} -> }, \\ -> \, \n -> newline
    # Check if the logical line ends mid JS string
    # Simple heuristic: count ' chars not preceded by backslash
    import re as _re
    singles = len(_re.findall(r"(?<!\\)'", py_line))
    if singles % 2 == 1:
        # odd number of quotes - might be continuation or problem
        # only flag if we're clearly in the JS section
        if "'\\n'" in py_line or (singles == 1 and "'" in py_line and "+" in py_line):
            print(f"  Line {i}: {py_line[:120]}")
