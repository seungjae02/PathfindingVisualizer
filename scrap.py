thing = []



with open('grid.txt') as nodes_file:
    for yidx, line in enumerate(nodes_file):
        for xidx, pos in enumerate(line):
            if pos == '1':
                thing.append((xidx, yidx))

print(len(thing))