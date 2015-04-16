ip6tables -F
ip6tables -A OUTPUT -p tcp --tcp-flags RST RST -j DROP
