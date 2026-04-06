"""Extract and render the blueprint HTML to disk for browser inspection."""
import json, re, textwrap

src = open("app.py", encoding="utf-8").read()

# Extract SYS_PROMPT value - dedent before exec
sp_start = src.index("    SYS_PROMPT = (")
sp_end   = src.index("\n    blueprint_html = f", sp_start)
sp_block = textwrap.dedent(src[sp_start:sp_end])
ns = {}
exec(sp_block, ns)
SYS_PROMPT = ns["SYS_PROMPT"]
print(f"SYS_PROMPT extracted: {len(SYS_PROMPT)} chars")

# Extract blueprint_html f-string  
bh_start = src.index('    blueprint_html = f"""')
bh_end   = src.index('\n    # --- KEY ENTRY', bh_start)
fstr_body = src[bh_start + len('    blueprint_html = f"""') : bh_end]
# Remove trailing triple-quote
if fstr_body.rstrip().endswith('"""'):
    fstr_body = fstr_body.rstrip()[:-3]

# The fstr_body has {{ -> { and }} -> } after Python f-string processing
rendered = fstr_body.replace("{{", "{").replace("}}", "}")

# Now inject placeholders
key_js   = json.dumps("TEST_API_KEY")
cv_js    = json.dumps("John Smith\nSoftware Engineer at ACME\nPython, JavaScript, SQL")
sys_js   = json.dumps(SYS_PROMPT)

rendered = rendered.replace("var GEMINI_API_KEY_PLACEHOLDER = '';",
                            f"var GEMINI_API_KEY_PLACEHOLDER = {key_js};")
rendered = rendered.replace("var CV_TEXT_PLACEHOLDER = '';",
                            f"var CV_TEXT_PLACEHOLDER = {cv_js};")
rendered = rendered.replace("var HAS_CV_PLACEHOLDER = false;",
                            "var HAS_CV_PLACEHOLDER = true;")
rendered = rendered.replace("var SYS_PROMPT_PLACEHOLDER = '';",
                            f"var SYS_PROMPT_PLACEHOLDER = {sys_js};")

out = "blueprint_test.html"
open(out, "w", encoding="utf-8").write(rendered)
print(f"Written {len(rendered)} chars to {out}")
print("Open in browser and check DevTools console for JS errors")
