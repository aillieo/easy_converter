folder=.
source=./source
out=$folder/out
out_data=$folder/out/data
name_space=EasyConverter
script=../easy_to_cs.py

python -c '
import sys
import os
sys.path.append(os.path.dirname("'''script'''")) '

rm -rf $out
rm -rf $out_data
python $script -source $source -out $out -outdata $out_data -namespace $name_space

read -p "press any key to continue..."