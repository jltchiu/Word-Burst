window=$1
stoplist=$2
penalty=$3

cd /home/jchiu1/BABEL/

python WordBurst.py input.net Tagalog ${window} ${stoplist} ${penalty} ./cnfs/Tagalog_dev/Tagalog_LimitedLP_rescore_${window}_${stoplist}_${penalty}_MI.net

cd /home/jchiu1/BABEL/jackofknife/scripts/

./retrieval.sh /home/jchiu1/BABEL/cnfs/Tagalog_dev/Tagalog_LimitedLP_rescore_${window}_${stoplist}_${penalty}_MI.net ~/BABEL/result/Tagalog_LimitedLP_rescore_${window}_${stoplist}_${penalty}_MI 106 10hr

cd /home/jchiu1/BABEL/jackofknife/scoring/

bash ./scoring.sh /home/jchiu1/BABEL/result/Tagalog_LimitedLP_rescore_${window}_${stoplist}_${penalty}_MI/
