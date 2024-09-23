#!/bin/bash
for i in {1..300}
do
   condor_submit condor.submit
done
