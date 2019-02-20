#!/bin/bash
# run BTM for Apple Customer Support Data


K=5   # number of topics

# parameters for Biterm topic modelling algorithm
alpha=1.5
beta=0.05

niter=3000 # changed this from 100 to 1000
save_step=1001

# path to relevant directories
input_dir=input/
output_dir=output/
model_dir=output/model/

# the input docs for training
doc_pt=input/reviews_clean.csv

# removing all the *.o files so that every time
# mode is built fresh
rm src/*.o

echo "=============== Index Docs ============="
# docs after indexing
dwid_pt=output/doc_wids.txt
# vocabulary file
voca_pt=output/voca.txt
python src/indexDocs.py $doc_pt $dwid_pt $voca_pt

## learning parameters p(z) and p(w|z)
echo "=============== Topic Learning ============="
W=`wc -l < $voca_pt` # vocabulary size
make -C src
src/btm est $K $W $alpha $beta $niter $save_step $dwid_pt $model_dir

## infer p(z|d) for each doc
echo "================ Infer P(z|d)==============="
echo "src/btm inf sum_b $K $dwid_pt $model_dir"
src/btm inf sum_b $K $dwid_pt $model_dir

## output top words of each topic
echo "================ Topic Display ============="
python src/topicDisplay.py $model_dir $K $voca_pt

## generate word cloud with the output results
echo "================ Generate word cloud ============="
python3 src/word_cloud.py