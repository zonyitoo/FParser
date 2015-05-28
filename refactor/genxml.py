
def gen(f, dep, depth=10, count=100):
    if dep == depth:
        return

    f.write('<a>')
    for _ in range(count):
        gen(f, dep + 1, depth, count)
    f.write('</a>')

if __name__ == '__main__':
    file = open('testxml.xml', 'w+')
    gen(file, 0, depth=5, count=10)
