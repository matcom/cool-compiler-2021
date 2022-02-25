BASEDIR=$(dirname "$0")
INPUT=$BASEDIR/input.txt
OUTPUT=$BASEDIR/output.txt
EXPECTED_OUTPUT=$BASEDIR/expected_output.txt
FILE=$BASEDIR/testing.mips

$BASEDIR/coolc.sh $BASEDIR/testing.cl
spim -file $FILE < $INPUT > $OUTPUT
if cmp -b -i 0:178 $EXPECTED_OUTPUT $OUTPUT
then
    echo "Test Passed"
else
    echo "Test Failed"
fi
