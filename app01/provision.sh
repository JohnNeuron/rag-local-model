#!/bin/sh

#cat <<EOT >> /home/vagrant/.ssh/authorized_keys
#--sua_chave_ssh_control_node_para_relacao_de_confianca
#EOT 



#Descomente caso esteja usando OLLAMA em outra máquina

#set -e

#echo "Atualizando pacotes..."
#sudo apt-get update -y

#echo "Instalando iptables e iptables-persistent..."
#sudo apt-get install -y iptables iptables-persistent

#echo "Habilitando IP forwarding..."
#sudo sysctl -w net.ipv4.ip_forward=1

#echo "Habilitando redirecionamento de pacotes destinados a endereços locais..."
#sudo sysctl -w net.ipv4.conf.all.route_localnet=1

# Limpa regras NAT existentes (opcional)
#echo "Limpando regras NAT existentes..."
#sudo iptables -t nat -F

#echo "Adicionando regra de redirecionamento para tráfego de entrada (PREROUTING)..."
#sudo iptables -t nat -A PREROUTING -p tcp --dport 11434 -j DNAT --to-destination 192.168.1.4:11434

#echo "Adicionando regra de redirecionamento para tráfego de saída (OUTPUT)..."
#sudo iptables -t nat -A OUTPUT -p tcp --dport 11434 -j DNAT --to-destination 192.168.1.4:11434

#echo "Garantindo que tráfego de loopback seja permitido..."
#sudo iptables -A INPUT -i lo -j ACCEPT
#sudo iptables -A OUTPUT -o lo -j ACCEPT

#echo "Salvando as regras do iptables..."
#sudo netfilter-persistent save

#echo "Provisionamento concluído com sucesso."




