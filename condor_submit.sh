#!/bin/bash
for i in {1..10}
do
   condor_submit condor.submit
done
