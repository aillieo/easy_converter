SCRIPT=../../../src/easy_to_cs.py
CONFIG_FILE="paths.config"
NAME_SPACE="EasyConverter"

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

PYTHON=""
if command -v python &>/dev/null; then
    PYTHON="python"
elif command -v python3 &>/dev/null; then
    PYTHON="python3"
else
    echo "Python not available."
    exit 1
fi

rm -rf $OUTPUT_SRC_DIR
rm -rf $OUTPUT_DATA_DIR

$PYTHON $SCRIPT -source $INPUT_DIR -out $OUTPUT_SRC_DIR -outdata $OUTPUT_DATA_DIR -namespace $NAME_SPACE

read -p "press any key to continue..."