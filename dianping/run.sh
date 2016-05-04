#!/bin/bash


export LANG=zh_CN.UTF-8

export http_proxy=http://proxy1.yidian.com:3130/

PROGRAM_PATH="/home/services"
CRAWL_PATH="${PROGRAM_PATH}/dianping"

LOG_PATH="/data/log/dianping/"


PYTHON_PATH="/usr/local/python-2.7/bin"

if [ ! -d $LOG_PATH ];then
    mkdir -p $LOG_PATH
fi

ID=`date +%Y%m%d`


function send_mail(){
    echo $1 | mail -s $2 taojinqiu@yidian-inc.com
}

cd $CRAWL_PATH

$PYTHON_PATH/python $PYTHON_PATH/scrapy crawl comments -a tasks_filename=kfc_verified.json >>${LOG_PATH}/crawl.log 2>&1


if [ $? -ne 0 ]; then
    send_mail "xinggan crawl error" ${ID}
    exit 1
fi

