CONFIG_FILE="paths.config"

load_paths() {
    if [ ! -f "$CONFIG_FILE" ]; then
        echo "Configuration file not found."
        echo "Please create a configuration file based on $CONFIG_NAME.example and rename it to $CONFIG_NAME."
        exit 1
    else
        echo "Loading configuration..."
        source $CONFIG_FILE
    fi
}

load_paths

# folder="TestCase"
# source=$folder/source
# out=$folder/out
# out_data=$folder/out/data
# name_space=EasyConverter
# script=easy_converter/easy_to_cs.py

PYTHON=""
if command -v python &>/dev/null; then
    PYTHON="python"
elif command -v python3 &>/dev/null; then
    PYTHON="python3"
else
    echo "Python not available."
    exit 1
fi

rm -rf $out
rm -rf $out_data

$PYTHON $script -source $source -out $out -outdata $out_data -namespace $name_space

# read -p "press any key to continue..."