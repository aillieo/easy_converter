folder=.
source=./source
out=$folder/out
out_data=$folder/out/data
name_space=EasyConverter

python ../easy_to_lua.py -source $source -out $out -outdata $out_data -namespace $name_space

read -p "press any key to continue..."