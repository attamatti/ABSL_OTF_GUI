#!/bin/sh
todays_date=$(date +"%d%m%Y")
current_user=$(whoami)
start_time=$(date +%s)
end_time=$(($start_time + $5))
current_time=$start_time
src=$1
project=$3
savepath=$2$current_user/${todays_date}_${project}


if [ ! -d $2$current_user ] 
then
    mkdir $2$current_user
fi

case "$4" in
offload2)
    ext="Images-Disc1/Grid*/Data/*-*.mrc"

    ;;
offload1)
    ext="Images-Disc1/Grid*/Data/*Fractions.mrc"

    ;;
  *)
    echo "Error: Illegal server."
    exit 1
    ;;
esac


while [ $current_time -lt $end_time ]
do
rsync -rutlDv "$src/" "$savepath"
ln -s $savepath/$ext Raw_data/ &>/dev/null
if [ -f "CtfFind/job003/micrographs_ctf.star" ]
then
    python /fbs/emsoftware2/LINUX/fbscem/scripts/fetch/scripts_fetch/micrograph_analysis.py --i CtfFind/job003/micrographs_ctf.star
fi

sleep 30
current_time=$(date +%s)
done

python /fbs/emsoftware2/LINUX/fbscem/scripts/fetch/scripts_fetch/micrograph_analysis.py --i CtfFind/job003/micrographs_ctf.star
rm OTFFT_running
