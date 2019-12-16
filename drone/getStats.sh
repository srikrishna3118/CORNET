#psrecord $(pgrep -f FlyNetSim) --interval 1 --duration 60 --plot Physics.png &
#P1=$!
psrecord $(pgrep -f FlyNetSim.py) --interval 1 --duration 30 --plot CORNET5.png --log 5.txt &
P2=$!
wait $P2
echo 'Done killing them softly'
kill -9 $(pgrep -f FlyNetSim.py) 

