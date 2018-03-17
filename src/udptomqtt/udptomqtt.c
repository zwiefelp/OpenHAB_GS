/*
    Simple udp server
*/
#include<stdio.h> //printf
#include<string.h> //memset
#include<stdlib.h> //exit(0);
#include<arpa/inet.h>
#include<sys/socket.h>
#include "mqtt.h"
#include "frozen.h"

#define BUFLEN 512  //Max length of buffer
#define PORT 1902   //The port on which to listen for incoming data

const char *client_name = "udptomqtt_daemon"; 	// -c
const char *broker_ip_addr     = "192.168.20.17";		// -i
uint32_t    broker_port        = 1883;			// -p
const char *topic       = "/openhab/mqtttest";	// -t
char msg[BUFLEN];
char temp[BUFLEN];

void die(char *s)
{
    perror(s);
    exit(1);
}

void parse_options(int argc, char** argv);

int main(int argc, char** argv) {

    puts("UDP to MQTT Daemon");
    if(argc > 1) {
      parse_options(argc, argv);
    }

    struct sockaddr_in si_me, si_other;

    int s, slen = sizeof(si_other) , recv_len;
    char buf[BUFLEN];

    //create a UDP socket
    if ((s=socket(AF_INET, SOCK_DGRAM, IPPROTO_UDP)) == -1)
    {
        die("socket");
    }

    // zero out the structure
    memset((char *) &si_me, 0, sizeof(si_me));

    si_me.sin_family = AF_INET;
    si_me.sin_port = htons(PORT);
    si_me.sin_addr.s_addr = htonl(INADDR_ANY);

    //bind socket to port
    if( bind(s , (struct sockaddr*)&si_me, sizeof(si_me) ) == -1)
    {
        die("bind");
    }

    char json[BUFLEN];
    char *token;
    char *search = "}";
    char *data;

    //  mqtt_broker_handle_t *broker = mqtt_connect("default_pub","127.0.0.1", 1883);
    mqtt_broker_handle_t *broker;

    //keep listening for data
    while(1)
    {
        printf("Waiting for data...");
        fflush(stdout);

        //try to receive some data, this is a blocking call
        if ((recv_len = recvfrom(s, buf, BUFLEN, 0, (struct sockaddr *) &si_other, &slen)) == -1)
        {
            die("recvfrom()");
        }

        //print details of the client/peer and the data received
        printf("Received packet from %s:%d\n", inet_ntoa(si_other.sin_addr), ntohs(si_other.sin_port));
        printf("Data: %s\n" , buf);

        snprintf(temp,recv_len + 1,"%s",buf);
        token = strtok(temp, search);
        token = strtok(NULL, search + 1);
        strcpy(json,token);
        printf("JSON=%s\n",json);

        json_scanf(json, strlen(json), "{data: %Q}", &data);
        printf("data=%s\n",data);
        snprintf(msg,BUFLEN,"%s",data);

	broker = mqtt_connect(client_name, broker_ip_addr, broker_port);
        if(broker == 0) {
	    puts("Failed to connect");
	    die("mqtt_connect()");
	}

        if(mqtt_publish(broker, topic, msg, QoS1) == -1) {
            printf("publish failed\n");
        }
        else {
            printf("Sent: %s\n", msg);
        }

        mqtt_disconnect(broker);

    }

    close(s);
    return 0;
}

void parse_options(int argc, char** argv)
{
   int i;
   for( i = 1; i < argc; ++i) {
      if(strcmp("-c",argv[i]) == 0) {
      	printf("client:%s ",argv[++i]);
      	client_name = argv[i];
      }
      if(strcmp("-i",argv[i]) == 0) {
      	printf("ip:%s ",argv[++i]);
      	broker_ip_addr = argv[i];
      }
      if(strcmp("-p",argv[i]) == 0) {
      	printf("port:%s ", argv[++i]);
      	broker_port = atoi(argv[i]);
      }
      if(strcmp("-t",argv[i]) == 0) {
      	printf("topic:%s ",argv[++i]);
      	topic = argv[i];
      }
   }
   puts("");
}
