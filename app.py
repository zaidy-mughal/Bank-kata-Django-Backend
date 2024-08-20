import re

# This will match any string
pattern = r".*"

# Example string
test_string = "This is a sample string."

if re.fullmatch(pattern, test_string):
    print("Matched!")
else:
    print("No match.")

