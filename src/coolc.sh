INPUT_FILE=$1
OUTPUT_FILE=${INPUT_FILE:0: -2}mips

echo "ChalkCode"
echo "Copyright © 2022: Andy Sánchez Sierra, Edaurdo Moreira González, Yadiel Felipe Medina"
# echo "Compiling $INPUT_FILE into $OUTPUT_FILE"

python main.py -f $INPUT_FILE

