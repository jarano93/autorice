#!/bin/zsh

readonly SCHEME_DIR="$HOME/.config/colorschemes"
readonly FNAME=$(basename $1)

if [ ! -d $SCHEME_DIR ]; then
    mkdir $SCHEME_DIR
fi
if [ ! -f "$SCHEME_DIR/$FNAME.scheme" ]; then
    echo -n "Creating colorscheme for $FNAME"
    output=$( python2 $2/kmeans.py $1 )
    echo $output > $SCHEME_DIR/$FNAME.scheme
    echo " -- DONE!"
else
    echo "Scheme exists for $FNAME"
fi
echo "$FNAME.scheme" > $SCHEME_DIR/active
