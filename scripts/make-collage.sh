#!/bin/sh

CONFIG=$(dirname $0)/config.ini
AVATARS_DIR=$(dirname $0)/$(awk '/avatars_dir/ { print $3 }' $CONFIG)
AVATARS=$(ls $AVATARS_DIR/* | sed "s/gif$/gif[0]/g")
DEST=$(dirname $0)/../sedemnajstka/sedemnajstka/public/images/collage.gif

montage -background none -geometry 64x64+2+2 -tile 10x $AVATARS $DEST
