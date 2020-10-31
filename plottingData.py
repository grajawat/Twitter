import json
import pandas as pd
import collections
import matplotlib.pyplot as plt
import numpy as np

#read data into an array- "tweets"
tweets_data_path = "FILENAME"
tweets_data = []
tweets_file = open(tweets_data_path, encoding="utf8")
for line in tweets_file:
	try:
		tweet = json.loads(line)
		tweets_data.append(tweet)
	except:
		continue
		
print(len(tweets_data))

tweets = pd.DataFrame() #structire tweets data into pandas dataframe to simplify data manipulation
#create and empty dataframe called tweets
print(tweets)
tweets['created_at'] = list(map(lambda tweet: tweet['created_at'], tweets_data))
#tweets['country'] = map(lambda tweet: tweet['place']['country'] if tweet['place'] != None else None, tweets_data)

tweets['id'] = list(map(lambda tweet : tweet['id'], tweets_data))
tweets['text'] = len(list(map(lambda tweet : tweet['text'], tweets_data)))
#tweets['url'] = len(list(map(lambda tweet : tweet['url'], tweets_data)))
#tweets['lang'] = len(list(map(lambda tweet : tweet['lang'], tweets_data)))
#tweets['country'] = list(map(lambda tweet : tweet['country'], tweets_data))
tweets['country'] = list(map(lambda tweet: tweet['place']['country'] if tweet['place'] != None else None, tweets_data))
tweets['lang'] = list(map(lambda tweet : tweet['lang'] if tweet['lang'] != None else None, tweets_data))




#displaying tweets graphically
tweets_by_country = tweets['lang'].value_counts()

fig, ax = plt.subplots()
ax.tick_params(axis='x', labelsize=20)
ax.tick_params(axis='y', labelsize=15)
ax.set_xlabel('Languages', fontsize=20)
ax.set_ylabel('Number of tweets' , fontsize=15)
ax.set_title('Top 5 languages', fontsize=15, fontweight='bold')
tweets_by_country[:5].plot(ax=ax, kind='bar', color='blue')

countryList = list(tweets['lang'])
countries = []
for val in countryList:
    if val != None:
	    countries.append(val)
counter=collections.Counter(countries)
valueList = list(counter.values())
valueList.sort(reverse=True)
keyList = list(tweets_by_country.index)
valueTop = valueList[:5]
keyTop = keyList[:5]
fig = plt.figure()
ax = fig.add_axes([0,0,1,1])
ax.bar(keyTop,valueTop)
plt.show()
#print(tweets_by_country)
