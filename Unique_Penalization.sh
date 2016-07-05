#conf=$1
penalty=$1

cd /home/jchiu1/BABEL/

python Unique_Penalization.py input.net ${penalty} ./cnfs/Tagalog_dev/Tagalog_LimitedLP_rescore_NoTime_Penalty_${penalty}.net

cd /home/jchiu1/BABEL/jackofknife/scripts/

./retrieval.sh /home/jchiu1/BABEL/cnfs/Tagalog_dev/Tagalog_LimitedLP_rescore_NoTime_Penalty_${penalty}.net ~/BABEL/result/Tagalog_LimitedLP_rescore_NoTime_Penalty_${penalty} 106 10hr

cd /home/jchiu1/BABEL/jackofknife/scoring/

bash ./scoring.sh /home/jchiu1/BABEL/result/Tagalog_LimitedLP_rescore_NoTime_Penalty_${penalty}/
