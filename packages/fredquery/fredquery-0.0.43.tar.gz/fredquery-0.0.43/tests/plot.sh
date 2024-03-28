#¡ sh
set -ex

D='src/fredquery'
cd $D

python fredplot.py --categoryid 32455


python fredplot.py --releaseid 365

python fredplot.py  --sourceid 69


python fredplot.py --tagname price

