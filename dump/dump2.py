import glob

files = glob.glob("./out/output-*-*.log")
# print(files)

for file in files:
    with open(file, "r") as fin:
        data = fin.read()

    binary = b""

    lines = data.split("\n")
    for line in lines:
        if line.startswith("$"):
            val = line.split("=")[1].strip()
            print(val)
            val = int(val, 16)
            print(val)
            binary += val.to_bytes(4, byteorder="little")

    _, start, end = file.split("-")
    end = end.split(".")[0]

    start = int(start, 16)
    end = int(end, 16)

    assert (end - start) == len(binary)

    with open("output.bin", "w+b") as fout:
        fout.seek(start)
        fout.write(binary)

    # print(start, end)
    # print(binary)