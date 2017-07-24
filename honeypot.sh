#!/bin/bash
#SSH HP: uci del_list updater.pkglists.lists='i_agree_honeypot'
#MINIPOTS: uci del_list ucollect.fakes.disable='80tcp'

ACTION=
PORT=
PROTOCOL="tcp"
#get action
if [ $1 == '-e' ] || [ $1 == '--enable' ] 
then
	ACTION='enable'
fi

if [ $1 == '-d' ] || [ $1 == '--disable' ] 
then
	ACTION='disable'
fi
#get port number
if [ $2 == '-p' ] || [ $2 == '--port' ] 
then
	PORT=$3
fi

#action with SSH HP?
if [ $PORT == '22' ]
then
	if [ $ACTION == 'enable' ]
	then
		uci add_list updater.pkglists.lists='i_agree_honeypot'
	else
		uci del_list updater.pkglists.lists='i_agree_honeypot'
	fi
	#save changes
	updater.sh
else
	X=$PORT$PROTOCOL
	if [ $ACTION == 'enable' ]
	then
		uci del_list ucollect.fakes.disable=$X
	else
		uci add_list ucollect.fakes.disable=$X
	fi
	uci commit ucollect

fi
echo "$ACTION HP on port $PORT"