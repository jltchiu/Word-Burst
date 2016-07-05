#/bin/bash
#expects directory with stdlist-file as parameter

if [ $# -ne 1 ] ; then
	echo "Must specify the directory to score on. Abort."
	exit -1
fi

export PATH="/data/ASR4/babel/yuchenz/std/cnfkws/local/ActivePerl-5.16/bin:$PATH"
export PATH="/data/ASR4/babel/yuchenz/std/cnfkws/local/bin:$PATH"
export F4DE_BASE="/data/ASR4/babel/yuchenz/std/cnfkws/local/F4DE-2.4.6"

ecf=ecfs/tagalog_devB.ecf
ecf0s=ecfs/tagalog_devb_Small_0.ecf
ecf0b=ecfs/tagalog_devb_Big_0.ecf
ecf1s=ecfs/tagalog_devb_Small_1.ecf
ecf1b=ecfs/tagalog_devb_Big_1.ecf
ecf2s=ecfs/tagalog_devb_Small_2.ecf
ecf2b=ecfs/tagalog_devb_Big_2.ecf
ecf3s=ecfs/tagalog_devb_Small_3.ecf
ecf3b=ecfs/tagalog_devb_Big_3.ecf
ecf4s=ecfs/tagalog_devb_Small_4.ecf
ecf4b=ecfs/tagalog_devb_Big_4.ecf

rttm=references/tagalog_devB.rttm
termList=term_lists/babel106b-v0.2g_conv-dev.kwlist.xml

#remove pronunciation variants
# sed "s/\*\([^ ]*\)\*/\1/" $rttm > references.cleaned.rttm
# sed "s/([0-9])//g" $rttm > references.cleaned.rttm

stdList=$1/*.kwslist.xml
evalScriptDir=$F4DE_BASE/bin

outPrefix=all

echo "$evalScriptDir/KWSEval -e $ecf -r ${rttm} -t $termList -s $stdList -c -o -b -d -f $1"

$evalScriptDir/KWSEval -e $ecf0s -r ${rttm} -t $termList -s $stdList -c -o -b -d -f $1

mv $1/bsum.txt $1/bsum_0s.txt

$evalScriptDir/KWSEval -e $ecf0b -r ${rttm} -t $termList -s $stdList -c -o -b -d -f $1

mv $1/bsum.txt $1/bsum_0b.txt

$evalScriptDir/KWSEval -e $ecf1s -r ${rttm} -t $termList -s $stdList -c -o -b -d -f $1

mv $1/bsum.txt $1/bsum_1s.txt

$evalScriptDir/KWSEval -e $ecf1b -r ${rttm} -t $termList -s $stdList -c -o -b -d -f $1

mv $1/bsum.txt $1/bsum_1b.txt

$evalScriptDir/KWSEval -e $ecf2s -r ${rttm} -t $termList -s $stdList -c -o -b -d -f $1

mv $1/bsum.txt $1/bsum_2s.txt

$evalScriptDir/KWSEval -e $ecf2b -r ${rttm} -t $termList -s $stdList -c -o -b -d -f $1

mv $1/bsum.txt $1/bsum_2b.txt

$evalScriptDir/KWSEval -e $ecf3s -r ${rttm} -t $termList -s $stdList -c -o -b -d -f $1

mv $1/bsum.txt $1/bsum_3s.txt

$evalScriptDir/KWSEval -e $ecf3b -r ${rttm} -t $termList -s $stdList -c -o -b -d -f $1

mv $1/bsum.txt $1/bsum_3b.txt

$evalScriptDir/KWSEval -e $ecf4s -r ${rttm} -t $termList -s $stdList -c -o -b -d -f $1

mv $1/bsum.txt $1/bsum_4s.txt

$evalScriptDir/KWSEval -e $ecf4b -r ${rttm} -t $termList -s $stdList -c -o -b -d -f $1

mv $1/bsum.txt $1/bsum_4b.txt


