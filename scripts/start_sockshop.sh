#!/bin/bash 

set -x

sudo pkill -9 -f sockshop
sudo pkill -9 -f haproxy

sh ./start_cart.sh &
sh ./start_catalogue.sh &
sh ./start_users.sh &
#sh ./start_orders.sh &
#sh ./start_payment.sh &
#sh ./start_shipping.sh &

echo "staring haproxy"
haproxy -f ../cfgTmp/sockshop.cfg


#java -jar ~/git/coherence-spring-sockshop-sample/orders/target/orders-1.2.4-SNAPSHOT.jar &
#ordersPid=$!
#sleep 15
#
#java -jar ~/git/coherence-spring-sockshop-sample/payments/target/payments-1.2.4-SNAPSHOT.jar &
#paymentsPid=$!
#sleep 15
#
#java -jar ~/git/coherence-spring-sockshop-sample/shipping/target/shipping-1.2.4-SNAPSHOT.jar &
#shippingPid=$!
#sleep 15