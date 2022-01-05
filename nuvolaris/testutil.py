import re

# takes a string, split in lines and search for the word (a re)
# if field is a number, splits the line in fields separated by spaces and print the selected field
# the output is always space trimmed for easier check
def grep(input, word, field=None):
    """
    >>> import util
    >>> util.grep("a\nb\nc\n", "b")
    b
    >>> util.grep(b"a\nb\n c\n", r"a|c")
    a
    c
    """
    try: input = input.decode()
    except: pass
    for line in input.split("\n"):
        if re.search(word, line):
            line = line.strip()
            if not field is None:
                try:
                    line = line.split()[field]
                except:
                    line = "missing-field"
            print(line)

# capture and print an excection
def catch(f):
    try: f()
    except Exception as e:
        print(type(e), str(e).strip())
