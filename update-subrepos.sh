cd "$(dirname $0)"
BASE=$(pwd)
git submodule update --recursive --init
cat $BASE/update-subrepos.json |\
 jq -r '.[] | "\(.dir) \(.branch)"' | grep "$1" |\
 while read DIR BRANCH
 do 
    echo "*** $DIR ***"
    cd $BASE/$DIR
    REPO="$(basename $DIR)"
    if ! git remote -v | grep origin | grep nuvolaris/$REPO
    then echo "bad origin in $DIR" 
         continue
    fi
    git fetch --all
    git checkout origin/$BRANCH -B $BRANCH
 done