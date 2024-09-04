import py7zr
pathfile = "./proyecto1/traces.7z"

with py7zr.SevenZipFile(pathfile,'r') as trace_fh:
    trace_fh.extractall(path="./proyecto1/")
    for line in trace_fh:
        line = line.rstrip()
        print(line)
# with py7zr.SevenZipFile(pathfile,'r') as trace_fh:
#     for line in trace_fh:
#         line = line.rstrip()
#         PC,result = line.split(" ")
#         print(PC, result)