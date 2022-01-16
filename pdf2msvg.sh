#!/usr/bin/env nix-shell
#!nix-shell -i sh -p pdf2svg nodePackages.svgo parallel perl python38

# usage: ./pdf2msvg pdffile [open_program]

set -e

if [ "$1" == "" ]; then
  echo "please provide a file name"
  exit 1
fi
if [ ! -f "$1" ]; then
  echo "$1 is not a file name"
  exit 1
fi

FILENAME=$(echo $1 | cut -d. -f1)
DIRNAME=$FILENAME-pages

delete_if_exists() {
	if [ -d "$1" ]; then
	  read -p 'Delete existing directory "'$1'" (y/n)? ' choice

	  case "$choice" in 
		j|J|y|Y ) ;;
		n|N ) exit 1;;
		* ) echo "Invalid input, exiting..."; exit 1;;
	  esac

	  rm -rf $1
	fi
}

delete_if_exists $DIRNAME
delete_if_exists $DIRNAME-big
delete_if_exists $DIRNAME-w

mkdir -p pages
mkdir $DIRNAME
mkdir $DIRNAME-big

echo Converting PDF pages to SVGs...
pdf2svg $1 $DIRNAME-big/$FILENAME-page%03d.svg all

echo Minimizing SVGs...
# all on one core
#svgo -q -f $DIRNAME-big -o $DIRNAME

# one file per command per job
parallel svgo -q {} -o $DIRNAME/{/} ::: $DIRNAME-big/*

# combine ... some cores get free once they're done
#parallel --shuf -m svgo {} -o $DIRNAME ::: $DIRNAME-big/*

# combine to consider startup time - but has large variation
#find $DIRNAME-big -type f | shuf | xargs -n 4 sh -c 'echo svgo "$@" -o '"$DIRNAME" | parallel

rm -rf $DIRNAME-big

mkdir $DIRNAME-w

echo "Resizing SVGs & adding a white background..."

for f in $DIRNAME/*.svg; do
	#WIDTH=$(< "$f" grep -Po 'width="\K[0-9\.]*' | head -1)
	WIDTH=$(< "$f" grep -Po 'viewBox="[\d\.]+ [\d\.]+ \K[\d\.]*' | head -1)

	#HEIGHT=$(< "$f" grep -Po 'height="\K[0-9\.]*' | head -1)
	HEIGHT=$(< "$f" grep -Po 'viewBox="[\d\.]+ [\d\.]+ [\d\.]+ \K[\d\.]*' | head -1)

	NHEIGHT=$(perl -E "say 720*$HEIGHT/$WIDTH")

	#echo replacing $HEIGHT with $NHEIGHT
	#sed 's/^\([^>]*height=\)".*\?"/\1"'$NHEIGHT'"/' $f
	sed -i 's/^\([^>]*height=\)"[^"]*"/\1"'$NHEIGHT'"/' $f
	#echo replacing $WIDTH with 720
	sed -i 's/^\([^>]*width=\)"[^"]*"/\1"720"/' $f

	#exit 1

	python3 - $f > $(dirname $f)-w/$(basename $f) <<EOF
import sys

with open(sys.argv[1], "r") as f:
	data = f.readlines()

	print(data[0].replace('>', '><rect width="100%" height="100%" fill="white"/>',1))

	for i in range(1,len(data)):
		print(data[i])
EOF

done

rm -rf $DIRNAME
mv $DIRNAME-w $DIRNAME

# open first svg with the supplied program
if [ $# -gt 1 ]; then
	$2 $(find $DIRNAME -name '*.svg' | sort | head -1)
fi
