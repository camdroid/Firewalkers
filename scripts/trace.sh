echo '' >> traceroute.txt
echo $(date) >> traceroute.txt
traceroute6 2604:a880:800:10::7df:6001 --tcp >> traceroute.txt 
