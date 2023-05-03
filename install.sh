#!/bin/bash

COGNIVA_HOME=`pwd`
export PATH=$COGNIVA_HOME/bin:$PATH
export PYTHONPATH=$COGNIVA_HOME:$PYTHONPATH

# Creates cogniva.conf
CONF_FILE=cogniva.conf
CONF_PATH=`eval echo ~$USER`/.cogniva

if [ -d "$CONF_PATH" ]; then
    read -p "$CONF_PATH already exists. Overwrite (y/n)? " ANSWER

    if [ "$ANSWER" = "n" ]; then
        echo "cogniva ready"
        return
    fi

    if [ "$ANSWER" = "y" ]; then

        rm -r $CONF_PATH
        mkdir $CONF_PATH

        echo "[CLUSTER]"                       > $CONF_PATH/$CONF_FILE
        echo "log_path=$COGNIVA_HOME/"        >> $CONF_PATH/$CONF_FILE
        echo "name=phoenix"                   >> $CONF_PATH/$CONF_FILE
        echo "nodes="                         >> $CONF_PATH/$CONF_FILE
        echo "patterns=dataset"               >> $CONF_PATH/$CONF_FILE
        echo "prefix=sample"                  >> $CONF_PATH/$CONF_FILE

        echo "cogniva ready"
        return
    fi
else

    mkdir $CONF_PATH

    echo "[CLUSTER]"                       > $CONF_PATH/$CONF_FILE
    echo "log_path=$COGNIVA_HOME/"        >> $CONF_PATH/$CONF_FILE
    echo "name=phoenix"                   >> $CONF_PATH/$CONF_FILE
    echo "nodes="                         >> $CONF_PATH/$CONF_FILE
    echo "patterns=dataset"               >> $CONF_PATH/$CONF_FILE
    echo "prefix=sample"                  >> $CONF_PATH/$CONF_FILE

    echo "cogniva ready"
    return
fi
