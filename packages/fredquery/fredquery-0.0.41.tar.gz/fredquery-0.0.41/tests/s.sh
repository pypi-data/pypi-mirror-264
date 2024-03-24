#! /bin/sh
set -ex

python src/fredquery/fredcategories.py --categories --showcategories
python src/fredquery/fredreleases.py --releases --showreleases
# python src/fredquery/fredseries.py
python src/fredquery/fredsources.py --sources --showsources
python src/fredquery/fredtags.py --tags --showtags
