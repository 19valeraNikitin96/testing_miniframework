#!/usr/bin/python3
if __name__ == '__main__':
    lines = None
    with open("numbers2.txt", "r") as data_file:
        lines = data_file.readlines()
    sum = 0
    for line in lines:
        if line.strip() == '' or '#' in line:
            continue
        num = float(line)
        sum += num
    print(sum)