#!/usr/bin/env python
#  Copyright (C) 2017  Sebastian Garcia, Ondrej Lukas
#
#  This program is free software; you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation; either version 2 of the License, or
#  (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with this program; if not, write to the Free Software
#  Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA  02111-1307  USA
#
# Authors:
# Sebastian Garcia  eldraco@gmail.com
# Ondrej Lukas      ondrej.lukas95@gmail.com    

# Description. 

import strategy_generator as generator
import argparse
import json
import subprocess


def open_honeypot(port, known_honeypots, protocol='tcp'):
    if port in known_honeypots:
        #ssh HP
        if port == '22':
            command = '/etc/init.d/mitmproxy_wrapper start'
        #minipot
        else:
            command = 'uci del_list ucollect.fakes.enable='+port+protocol
    #no, use TARPIT
    else:
        command = 'iptables -I zone_wan_input 6 -p tcp --dport %s -j TARPIT' % port
    subprocess.Popen(command, shell=True, stdin=subprocess.PIPE, stdout=subprocess.PIPE).communicate()
    print "\tOpening HP in port: {}".format(port)

def close_honeypot(port,known_honeypots, protocol='tcp'):
    if port in known_honeypots:
            #ssh HP
            if port == '22':
                command = '/etc/init.d/mitmproxy_wrapper stop'
            #minipot
            else:
                command = 'uci del_list ucollect.fakes.disable='+port+protocol
        #no, use TARPIT
    else:
        command = 'iptables -D zone_wan_input 6'
    subprocess.Popen(command, shell=True, stdin=subprocess.PIPE, stdout=subprocess.PIPE).communicate()
    print "\tClosing HP in port: {}".format(port)

def get_strategy(ports, active_honeypots, path_to_strategy):
    #print "\tUser is using port(s): " + str(ports)
    #print "\tActive HP: {}".format(active_honeypots)
    #get ports for HP from strategy
    
    #build the string
    ports_s = ''
    for item in ports:
        ports_s += (str(item)+',')
    #get rid of the last comma
    ports_s = ports_s[0:-1]
    
    #get strategy
    suggested_honeypots = generator.get_strategy(ports_s,path_to_strategy)
    return suggested_honeypots

if __name__ == '__main__':
    """parser = argparse.ArgumentParser(description='Tells you which honeypot port to open given your production ports.')

    parser.add_argument('-f', '--file', type=str, help='Strategy file')
    parser.add_argument('-d', '--debug', type=int, help='Debug. From 0 to 10')
    parser.add_argument('-p', '--portsinfo', type=str, help='File containing type of each port', default='/etc/LUDUS/ports_type.json')
    args = parser.parse_args()

    #find out production ports
    ports = []
    with open(args.portsinfo) as data_file:    
    	data = json.load(data_file)
    	for p in data:
    		if data[p].lower() == 'accepted':
    			ports.append(int(p))

    print "User is using port(s): " + str(ports)
    #get ports for HP from strategy
    ports_s = ''
    for item in ports:
    	ports_s += (str(item)+',')
    ports_s = ports_s[0:-2]
 
    suggested_honeypots = generator.get_strategy('80',args.file)
    print "Suggested port(s) for HP: " + str(suggested_honeypots)
    #print suggested_honeypots
    #open the Honeypots on suggested ports
    try:
	    for port in suggested_honeypots:
	    	open_HP_on_port(port)
    except TypeError:
	pass"""
    print get_strategy(['80'])




