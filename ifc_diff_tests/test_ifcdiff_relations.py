import ifcdiff
print("repr:", repr(ifcdiff.RELATIONSHIP_TYPE))
try:
    print("iterable ->", list(ifcdiff.RELATIONSHIP_TYPE))
except Exception:
    pass
# If it's an Enum-like:
for name in dir(ifcdiff.RELATIONSHIP_TYPE):
    if not name.startswith("_"):
        print(name)
# If it's a dict-like:
try:
    print("keys:", getattr(ifcdiff.RELATIONSHIP_TYPE, "keys")())
except Exception:
    pass