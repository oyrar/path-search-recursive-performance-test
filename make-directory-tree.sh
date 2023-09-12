#!/bin/bash

for i in $(seq 100); do for n in $(seq ${i}); do mkdir -vp ./path/path$i/path$n; done ; done
find . path -type d | while read dn; do touch $dn/fn1; done
