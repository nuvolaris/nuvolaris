F=${1:?file}

FILE=$(realpath $F)
echo $FILE

CUR="$(basename $FILE)"
CONT="$(dirname $FILE)"
while ! test -d ${CONT}.diff
do 
    echo $CUR
    CUR="$(basename $CONT)/$CUR"
    CONT=$(dirname $CONT)
    echo $CONT
done

echo  CONTAINER $CONT
echo  PATH $CUR

code -r -d ${CONT}.diff/$CUR $CONT/$CUR
