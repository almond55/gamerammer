import os
import sys
import csv
import random
import getopt

def parsefile(inputfile):
    isafile = os.path.isfile(inputfile)
    if not isafile: 
        print('%s is not a valid file.' % inputfile)
        sys.exit(2)
    f = open(inputfile, 'r')
    reader = csv.reader(f, delimiter=';')
    copies = 1
    base = None
    first_half = {}
    second_half = {}
    rand_value = {}
    for row in reader:
        if 'cards' in row[0]:
            copies = int(row[1])
            continue
        if any('rand' in s for s in row):
            rand_base = row[0].split('_')
            base_num = rand_base[1]
            rand_value[base_num] = {}
            rand_value[base_num]['lowerlimit'] = int(row[1])
            rand_value[base_num]['upperlimit'] = int(row[2])
            continue
        base_name = row[0]
        if base_name != base:
            ls = []
            base = base_name
            for column in row:
                if column != base_name and column != '':
                    first_half.setdefault(base, []).append(column)
            continue
        else:
            for column in row:
                if column != base_name and column != '':
                    second_half.setdefault(base, []).append(column)            
    f.close()
    output = []
    for iteration in range(copies):
        outline = {}
        for base in first_half.keys():
            element = None
            if base in second_half.keys():
                element = random.choice(first_half[base]) + random.choice(second_half[base])
            else:
                element = random.choice(first_half[base])
            if '%s' in element:
                lowerlimit = rand_value[base]['lowerlimit']
                upperlimit = rand_value[base]['upperlimit']
                element = element % random.randint(lowerlimit, upperlimit)
            outline[base] = element
        output.append(outline)
    return output
    
def makecsv(outfile, output):
    f = open(outfile, 'w')
    for header in output[0].keys():
        f.write("%s;" % header)
    f.write("\n")
    for item in output:
        for element in item.values():
            f.write("%s;" % element)
        f.write("\n")
    f.close()

def makend(outfile, output):
    cards = len(output)
    f = open(outfile, 'w')
    f.write('page = 21, 29.7, portrait, hv\n')
    f.write('dpi = 300\ncardsize = 6, 9\ngap = 0,0\n')
    f.write('cards = %s\n' % cards)
    f.write('border = rectangle, #000000, 0.1, dotted, #000000\n')
    f.write('font = "Liberation Sans", 25, TB, #000000\n')
    count = 0
    for item in output:
        count = count + 1
        for element in item.values():
            f.write('text = %s, "%s", 0.5, 0.5, 5, 8, center, center\n' % (
                count, element)
            )
    f.close()

def main(argv):
    try:
        opts, args = getopt.getopt(argv, "h")
    except getopt.GetoptError:
        print('python gr.py <input file name> <output file name>')
        sys.exit(2)
    
    output = parsefile(args[0])
    if args[1] == 'demo.txt':
        try:
            makend(args[1], output)
        except IndexError:
            print('Output filename required')
            sys.exit(2)
    else:
        try:
            makecsv(args[1], output)
        except IndexError:
            print('Output filename required')
            sys.exit(2)

if __name__ == "__main__":
    main(sys.argv[1:])

