# @julianofischer
# use mode: python3 time_filtering.py trace_file begin_time final_time

import sys

assert 3 <= len(sys.argv) <= 4, "Illegal number of arguments"

begin_time = int(sys.argv[2])
end_time = -1
if len(sys.argv) == 4:
    end_time = int(sys.argv[3])

with open(sys.argv[1], 'r') as trace_file, open(sys.argv[1]+"_output",'+w') as output_file:
    for line in trace_file:
        line = line.rstrip().split()
        time = int(line[0])

        if time >= begin_time:
            if time > end_time > -1:
                break

            time = time - begin_time
            line[0] = str(time)
            output_file.write("\t".join(line)+"\n")
