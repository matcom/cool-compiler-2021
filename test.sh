#!/bin/bash

CURDIR=$(dirname $0)

$CURDIR/src/coolc.sh "$CURDIR/tests/$1/$2.cl" && spim -file "$CURDIR/tests/$1/$2.mips"
