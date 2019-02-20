# BTM for Topic Modeling Using Bigquery Data

This project gets data (headlines) from Bigquery table (rss_articles), performs some preprocessing, applies Biterm Topic Algorithm on 
the data and then tries to generate word cloud (as png) from the output topics. Currently we are using the 10 best topics. In the PNG, words
in the same topic have the same color

### **Usage Commands**

Since this project uses C++ code to run the Biterm topic model algorithm, its structure is a bit different from other Python project.
All the code is run through the Bash shell file. (Before running the code, make sure that the file is executable). To run it from terminal,
issue the following command
```
run_headlines_data.sh
```

Here is the brief description of different codes that are run using this script:

1) The very first command that this code runs is the following:
```
python3 src/headline_downloader.py
```

The goal of this script is to grab headlines from the BigQuery table. It is important to note that to access bigquery, we need to have the 
'bigquery_access.json' file in the input folder. If this code runs successfully, it will generate 'headlines.txt' file inside the input folder

2) After successfully downloading the dataset, next step to perform cleaning on the input data. For this we run the following command:
```
python3 src/data_cleaner.py -i headlines.txt -o headlines_clean.txt
```

The first parameter is the name of the input file and second parameter is the name of the output file that will be generated as output. This code will remove stop words from text and tries to form bigrams if possible. To control how many bigrams are formed, we have the following
line of code:
```
Phrases(sentence_stream, min_count=10, threshold=100)
```

The min_count and threshold paramter controls how many bigrams are formed. Once the script runs successfully, it will generate 'headlines_clean.txt' file inside the input folder which will have all the extra words removed

Then in the shell script, we set the parameter K (currently 10) which controls how many topics will be generated.

The other two parameters (**alpha** and **beta**) are related to the algorithm and I haven't modified them

The parameter **niter** (currently 1000) controls how many iterations the algorithm will run for

The parameter **save_step** controls after how many steps of iterations the model parameters should be stored. It is not too useful for us

After that we set some directory paths and run the biterm algorithm.

After running the algorithm, the file 'topicDisplay.py' stores the output model in a Python pickle file called 'topics.pickle'
in the output folder.

Finally we run the 'word_cloud.py' which reads the pickle file and generates a word cloud PNG image in the output folder.


### **Input Folder Details**

Initially this folder will contain 'bigquery_access.json' file which contains key to access Bigquery table

After running the code, we will see 2 additional txt files. 'headlines.txt' contains headlines downloaded from Bigquery and 'headlines_clean.txt'
contains the same headlines from which the stop words have been removed

### **Output Folder Details**

After running the code, it will contain a folder called "model" which contains the generated model. 'doc_wids.txt' contains the headlines in which words have been converted to their respective ids. 'voca.txt' will contain the mapping from word to numeric ids. 

'topics.pickle' contains the topic information which is the result of running the biterm topic model algorithm. Finally 'word_cloud.png' contains the topic cloud generated from running the algorithm