#read data into an array- "tweeets"
tweets_data_path = "FILEPATH"
tweets_data = []
tweets_file = open(tweets_data_path, "r")

splitLen = 500         # 100 lines per file
outputBase = 'output' # output.1.txt, output.2.txt, etc.
count = 0
at = 0


dest = None
for line in tweets_file:
    if count % splitLen == 0:
        if dest: dest.close()
        dest = open(outputBase + str(at) + '.json', 'w')
        at += 1
    dest.write(line)
    count += 1
