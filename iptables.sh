#!/bin/bash



function iptables_rule(){

iptables -F
iptables -A OUTPUT -p tcp --sport 80 --tcp-flags SYN,RST,ACK,FIN,PSH SYN,ACK -j NFQUEUE --queue-num 2
iptables -A OUTPUT -p tcp --sport 80 --tcp-flags SYN,RST,ACK,FIN,PSH ACK -j NFQUEUE --queue-num 4
iptables -A OUTPUT -p tcp --sport 80 --tcp-flags SYN,RST,ACK,FIN,PSH PSH,ACK -j NFQUEUE --queue-num 6
iptables -A OUTPUT -p tcp --sport 80 --tcp-flags SYN,RST,ACK,FIN,PSH FIN,ACK -j NFQUEUE --queue-num 8

}



function check_django(){
  lsof -i:8080 >/dev/null
  return $?
}


function check_redirect(){
  lsof -i:80 >/dev/null
  return $?
}


function main(){

CHECK_IPTABLES=$(iptables -L OUTPUT |grep -i 'tcp spt:http'|wc -l)

while :
do
  [ ${CHECK} == 4 ] || iptables_rule
  check_django || supervisorctl start django
  check_redirect || supervisorctl start redirect
  sleep 2
done


}



main
