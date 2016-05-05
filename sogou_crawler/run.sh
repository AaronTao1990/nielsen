#!/bin/bash


export LANG=zh_CN.UTF-8

SPIDER_NAME=$1
# check if process is running

count=`ps -fe | grep "${SPIDER_NAME}" | grep -v "grep" | grep -v "run"`
if [ "$?" == "0" ]; then
    echo "--1--"
    exit 0
fi
echo "--2--"

PROGRAM_PATH="/home/ec2-user"
CRAWL_PATH="${PROGRAM_PATH}/wemedia_crawler/sogou_crawler"


LOG_PATH="/data/log/sogou/${SPIDER_NAME}"


if [ ! -d $LOG_PATH ];then
    mkdir -p $LOG_PATH 
fi

ID=`date +%Y%m%d`

function send_mail(){
     echo $1 | mail -s $2 taojinqiu@yidian-inc.com
}

cd $CRAWL_PATH

/usr/bin/python /usr/local/bin/scrapy crawl ${SPIDER_NAME} 1>>${LOG_PATH}/${ID}.log 2>&1


if [ $? -ne 0 ]; then
	send_mail "sogou crawl error" ${ID}
    exit 1
fi

