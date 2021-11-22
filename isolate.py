import argparse
from subprocess import check_output, Popen, PIPE, run
from collections import namedtuple
import re
import os

Symbol = namedtuple("Symbol", ['address', 'type', 'name'])
symbols = []
symbol_set = set()


def get_symbols(elf_file):
    nm_output = check_output(["nm", "-g"] + elf_file).decode().splitlines()
    for line in nm_output:
        line = line.split()
        if len(line) == 0 or len(line) == 1 or len(line) > 3:
            continue
        else:
            if len(line) == 2:
                s = Symbol(None, line[0], line[1])
            else:
                s = Symbol(line[0], line[1], line[2])
            if s.type != 'T':
                continue
            symbols.append(s)
            symbol_set.add(s.name)
    return symbols


def main():
    parser = argparse.ArgumentParser(description='Isolate elf symbols.')
    parser.add_argument('-o', required=True, metavar="OUTPUT", help='output file name')
    parser.add_argument('-p', required=True, metavar="PATTERN", help='pattern of symbols to be exposed', action='append')
    parser.add_argument('FILES', type=str, nargs='+', help='.o and .a files', action='append')
    args = parser.parse_args()
    files = sum(args.FILES, [])
    patterns = args.p + ["_*"]

    get_symbols(files)
    # print(symbols)
    # defined_functions = [x for x in symbols if x.type in ('T', 't')]
    # print(defined_functions)
    symbol_list = list(symbol_set)
    symbol_str = '\n'.join(symbol_list)
    p = Popen(['c++filt'], stdout=PIPE, stdin=PIPE, stderr=PIPE)
    stdout_data = p.communicate(input=symbol_str.encode())[0].decode().splitlines()
    symbol_map = {k: v for k, v in zip(stdout_data, symbol_list)}

    export_symbols = set()
    patterns = [re.compile(x.replace("*", ".+")) for x in patterns]
    for sym in symbol_map.keys():
        for pat in patterns:
            if pat.match(sym):
                export_symbols.add(symbol_map[sym])
                continue

    remove_symbols = symbol_set - export_symbols
    # print(remove_symbols)
    filename = '+'.join(files + [args.o]).replace('.', '_') + '.txt'
    with open(filename, 'w') as f:
        i = 1
        for s in remove_symbols:
            f.write(f"{s} pri_{i}{args.o.replace('.', '_')}_{s}\n")
            i += 1

    run(["ld", "-r", "-o", args.o] + files)
    run(["objcopy", f"--redefine-syms={filename}", args.o])
    # os.remove(filename)


if __name__ == '__main__':
    main()
