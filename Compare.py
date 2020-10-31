#compare
#python3

import os

INPUT_TWEET_APP_ID = 'FILENAME'
INPUT_DB_APP_ID = 'FILENAME2'

tweet_id_list = []
db_id_list = []

join_list = []

file_t = open(INPUT_TWEET_APP_ID, 'r')
for tline in file_t:
	tweet_id_list.append(tline)

file_d = open(INPUT_DB_APP_ID, 'r')
for dline in file_d:
	dline = dline.replace('|', '')
	db_id_list.append(dline)
	#print(dline)

join_list = list(set(tweet_id_list) & set(db_id_list))

print('tweet id: ' + str(len(tweet_id_list)))
print('db id: ' + str(len(db_id_list)))
print('join: ' + str(len(join_list)))
