#Import data

library(readr)
text_data <- as.matrix(read_csv("/mnt/input/doc_info.txt", 
                                   col_names = FALSE))[,1]
#pre-processing
library(tm)
text_data <- gsub("U.S.", "US", text_data)
text_data <- gsub("’", "", text_data)  # remove apostrophes
text_data <- gsub("[[:punct:]]", "", text_data)  # replace punctuation with space
text_data <- gsub("[[:cntrl:]]", " ", text_data)  # replace control characters with space
text_data <- gsub("[[:digit:]]", "", text_data) # remove digits
text_data <- tolower(text_data)  # force to lowercase

#Output the data to pc to run on BTM on python
write.table(text_data,"/mnt/input/doc_info2.txt",quote = FALSE,row.names = FALSE,col.names = FALSE)






