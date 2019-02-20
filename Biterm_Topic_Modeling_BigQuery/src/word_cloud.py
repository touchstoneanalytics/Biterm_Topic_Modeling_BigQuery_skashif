from wordcloud import (WordCloud, get_single_color_func)
import pickle
import random
import csv
#import matplotlib.pyplot as plt

class SimpleGroupedColorFunc(object):
    """Create a color function object which assigns EXACT colors
       to certain words based on the color to words mapping

       Parameters
       ----------
       color_to_words : dict(str -> list(str))
         A dictionary that maps a color to the list of words.

       default_color : str
         Color that will be assigned to a word that's not a member
         of any value from color_to_words.
    """

    def __init__(self, color_to_words, default_color):
        self.word_to_color = {word: color
                              for (color, words) in color_to_words.items()
                              for word in words}

        self.default_color = default_color

    def __call__(self, word, **kwargs):
        return self.word_to_color.get(word, self.default_color)


with open('/mnt/output/topics.pickle', 'rb') as handle:
    topics_dict = pickle.load(handle)


with open('/mnt/output/topics_25.csv', 'w') as csv_file:
    writer = csv.writer(csv_file)
    for key, value in topics_dict.items():
       writer.writerow([key, value])
'''
#colors = ['#00ff00', '#0000ff', 'red', '#abff00',  '#abffab',  '#00ffab',  '#ab0000',  '#ab8912',  '#00ffff',  '#ababab']
colors = ['#ff275d', '#237e7f', '#00b0f0', '#000000',  '#ffff00',  '#00872b',  '#ae8a64',  '#ab85c3',  '#c7f4da',  '#ff1493']

frequency_dict = {}
color_dict = {}
i = 0
for k1,v1 in topics_dict.items():
    #color = '#%06x' % random.randint(0, 0xFFFFFF)
    #color_dict[color] = []
    
    color_dict[colors[i]] = []
    for k2,v2 in v1.items():
        frequency_dict[k2] = float(v2)
        color_dict[colors[i]].append(k2)
        #color_dict[color].append(k2)
    
    i+= 1

wordcloud = WordCloud(width=900,height=500, max_words=1628,background_color='white',relative_scaling=1,normalize_plurals=False).generate_from_frequencies(frequency_dict)

# Words that are not in any of the color_to_words values
# will be colored with a grey single color function
default_color = 'black'

# Create a color function with single tone
grouped_color_func = SimpleGroupedColorFunc(color_dict, default_color)

# Apply our color function
wordcloud.recolor(color_func=grouped_color_func)

plt.imshow(wordcloud, interpolation='bilinear')
plt.axis("off")
#plt.show()
plt.savefig('/mnt/output/word_cloud.png')
'''