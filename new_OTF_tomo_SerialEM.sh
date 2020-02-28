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
    ext="*.mrc"

    ;;
offload1)
    ext="*.mrc"

    ;;
  *)
    echo "Error: Illegal server."
    exit 1
    ;;
esac


if [ ! -d "$savepath" ]; then
    mkdir -p "$savepath"
fi

if [ ! -d "Raw_data" ]; then
    mkdir -p "Raw_data"
fi

if [ ! -d "To_stack" ]
then
    mkdir -p "To_stack"
fi


echo "Start: $start_time End: $end_time"

while [ $current_time -lt $end_time ]
do
rsync -rutlDv "$src/" "$savepath"
ln -s $savepath/$ext "Raw_data/" &>/dev/null
if [ -f "CtfFind/job003/micrographs_ctf.star" ]
then
	python /fbs/emsoftware2/LINUX/fbscem/scripts/Tomo_OTF/tomo-micrograph-analysis.py CtfFind/job003/micrographs_ctf.star
fi
cd To_stack
ls ../MotionCorr/job002/Raw_data/*.mrc &&
ln -s ../MotionCorr/job002/Raw_data/*.mrc .
cd ..
sleep 30
current_time=$(date +%s)
done
python /fbs/emsoftware2/LINUX/fbscem/scripts/Tomo_OTF/tomo-micrograph-analysis.py CtfFind/job003/micrographs_ctf.star

cd To_stack
ls ../MotionCorr/job002/Raw_data/*.mrc &&
ln -s ../MotionCorr/job002/Raw_data/*.mrc .
cd ..

