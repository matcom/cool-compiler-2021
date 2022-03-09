INPUT_FILE=$1
OUTPUT_FILE=${INPUT_FILE:0: -2}mips

echo "ChalkCode"
echo "Copyright © 2022: Andy Sánchez Sierra, Edaurdo Moreira González, Yadiel Felipe Medina"

python3 main.py $INPUT_FILE

