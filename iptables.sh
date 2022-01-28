#!/bin/bash


DAY_TIME=`date +%F\ %T`
UFW_DOMAIN='98.net'




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



# Detect the domain name status code, and restart if it is not 200.
function check_code(){
  echo -e "${DAY}\t\c"
  code=$(curl -o /dev/null -w '%{http_code}\n' -s -I ${UFW_DOMAIN})
  if [[ $code == 200 ]];then
    echo -e "\033[32m Running...... \033[0m"
  else
    supervisorctl restart all >/dev/null
    echo -e "\033[31m Restart...... \033[0m"
  fi
}




function main(){


while :
do
  CHECK_IPTABLES=$(iptables -L OUTPUT |grep -i 'tcp spt:http'|wc -l)
  [ ${CHECK_IPTABLES} == 4 ] || iptables_rule
  check_django || supervisorctl start django
  check_redirect || netstat -tunlp |grep -w "0.0.0.0:80" |awk '{print $NF}' |cut -d '/' -f 1| xargs kill -9; supervisorctl start redirect
  check_code
  sleep 5
done


}



main
