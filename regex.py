import re

text = "Fronte nd234"
char = re.search('[0-9]+', text )

clean = text[0:char.start()]

print(clean)
# "a{10}" - exactly 10


# a{3,6} - aaa, aaaa, aaaaa, aaaaaa

# [0-9]+