#!/bin/bash

BINOUT="$1"

ADDR_LINES=( 17 27 22 10 9 11 5 6 18 23 8 24 13 15 14 19 26 ) 
DATA_LINES=( 4 3 2 21 20 16 12 1 )
CE=25
OE=7

function as_byte() {
  RAW=$(raspi-gpio get $*)
  ans=""
  bit=0
  for dq in ${DATA_LINES[@]} ; do
    v=$(sed -n -e 's/GPIO '$dq': level=\([01]\).*/\1/p' <<< "$RAW")
    # We need to reverse the bit order here ...
    ans="$v${ans}"
    bit=$((bit+1))
  done
  ch=$(bc <<< "obase=16; ibase=2; $ans")
  cn=$(bc <<< "obase=10; ibase=2; $ans")
  cx='\x'$ch
  echo -n -e $cx >> "$BINOUT"
  if [ $cn -lt 32 -o $cn -gt 126 ] ; then cx="." ; fi
  echo $ans $(printf $cx ) $ch
}

function dump_data() {
RAW=$(raspi-gpio get 1-27)
bit=0
for dq in ${DATA_LINES[@]} ; do
  v=$(sed -n -e 's/GPIO '$dq': level=\([01]\).*/\1/p' <<< "$RAW")
  echo "DQ$bit=$v (GPIO$dq)"
  bit=$((bit+1))
done
}

function dump_all() {
# Set output lines
RAW=$(raspi-gpio get 1-27)
bit=0
for a in ${ADDR_LINES[@]} ; do
  v=$(sed -n -e 's/GPIO '$a': level=\([01]\).*/\1/p' <<< "$RAW")
  echo "A$bit=$v (GPIO$a)"
  bit=$((bit+1))
done
bit=0
for dq in ${DATA_LINES[@]} ; do
  v=$(sed -n -e 's/GPIO '$dq': level=\([01]\).*/\1/p' <<< "$RAW")
  echo "DQ$bit=$v (GPIO$dq)"
  bit=$((bit+1))
done
v=$(sed -n -e 's/GPIO '$CE': level=\([01]\).*/\1/p' <<< "$RAW")
echo "CE=$v (GPIO$CE)"
v=$(sed -n -e 's/GPIO '$OE': level=\([01]\).*/\1/p' <<< "$RAW")
echo "OE=$v (GPIO$OE)"
}

# Make data inputs, pull none
for a in ${DATA_LINES[@]} ; do
  raspi-gpio set $a ip pd
done

# Make Address & OE/CE outputs, pull up high
for a in $OE $CE ${ADDR_LINES[@]} ; do
  raspi-gpio set $a op pu dl
done

echo -n > "$BINOUT"
OPS=( dl dh )
for byte in {0..131071} ; do
  bytebits=$(printf "%17b" $(bc <<< "ibase=10; obase=2; $byte")|sed 's@ @0@g')
  #echo $bytebits
  bit=16 # note address bits in rev order of what we need
  for a in ${ADDR_LINES[@]} ; do
    v=${bytebits:${bit}:1}
    raspi-gpio set $a ${OPS[$v]}
    bit=$((bit-1))
  done
  #dump_all
  #continue
  #sleep 0.01
  # CE then OE
  raspi-gpio set $CE dl
  # 150 ns
  #sleep 0.01
  raspi-gpio set $OE dl
  #sleep 0.01
  #dump_all
  echo $(printf "%08x" $byte) $(as_byte $D)
  # echo "Step..." ; read dummy
  raspi-gpio set $OE dh
  raspi-gpio set $CE dh
done
