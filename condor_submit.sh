#!/bin/bash
for i in {1..1000}
do
   condor_submit condor.submit
done
