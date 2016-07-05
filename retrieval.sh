#!/bin/bash

if [ $# -ne 4 ]; then
    echo "Must specify the confusion networks and result dir."
    echo "Usage: retrieval.sh <confusion networks> <result dir> <101|104|105|106> <10hr|2hr>"
    echo "  101: Cantonese"
    echo "  104: Pashto"
    echo "  105: Turkish"
    echo "  106: Tagalog"
    exit 2;
fi

cnf_file=$1
result_dir=`readlink -m $2 | sed "s/[/]*$//"`
lang=$3
langstr=""
split=$4

if [ $lang == "101" ]; then
    langstr="cantonese";
elif [ $lang == "104" ]; then
    langstr="pashto";
elif [ $lang == "105" ]; then
    langstr="turkish";
elif [ $lang == "106" ]; then
    langstr="tagalog";
else
    echo "Invalid language id: ${lang}. Must be 101, 104, 105 or 106."
    exit 4;
fi

if [[ $split != "10hr" && $split != "2hr" ]]; then
    echo "Invalid split: ${split} ... must be either 2hr or 10hr."
    exit 3;
fi

if [ ! -d ${result_dir} ]; then
    mkdir -p ${result_dir}
fi

if [ ! -d ${result_dir}_raw ]; then
    mkdir -p ${result_dir}_raw
fi

if [ $split == "2hr" ]; then
    ./kwsearch.py ./config/config_${langstr}_2hr.py ${cnf_file} ${result_dir}/detections.kwslist.xml --global-threshold=YES || exit 1;
    ./kwsearch.py ./config/config_${langstr}_2hr.py ${cnf_file} ${result_dir}_raw/detections.kwslist.xml --global-threshold=NO || exit 1;
elif [ $split == "10hr" ]; then
    ./kwsearch.py ./config/config_${langstr}.py ${cnf_file} ${result_dir}/detections.kwslist.xml --global-threshold=YES || exit 1;
    ./kwsearch.py ./config/config_${langstr}.py ${cnf_file} ${result_dir}_raw/detections.kwslist.xml --global-threshold=NO || exit 1;
fi

pushd ../scoring
if [ $split == "2hr" ]; then
    ./score_${langstr}_2hr.sh ${result_dir}/
elif [ $split == "10hr" ]; then
    ./score_${langstr}.sh ${result_dir}/
fi
popd
