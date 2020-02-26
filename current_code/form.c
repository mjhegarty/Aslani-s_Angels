#include <stdlib.h>
#include <stdint.h>
#include <stdio.h>

enum type{HZ_500,HZ_100, HZ_1, DEBUG};

int format_packet(uint8_t * packet){
    uint16_t sig_1;
    uint16_t sig_2;
    //Bitwise unpacking of j
    sig_1 = (uint16_t)packet[1] | (((uint16_t)packet[2] & 0xF0) << 4);
    sig_2 = (uint16_t)packet[3] | (((uint16_t)packet[2] & 0x0F) << 8);
    printf("sig 1 is %u, sig 2 is %u", sig_1, sig_2);
    return 0;
}




int main(void){



    return 0;



}





/*
    //For  12 bit samples s1, s2...
    uint16_t s0 = 512;
    uint16_t s1 = 259;
    //We need to transmit them in 8 bit chunks
    uint8_t b0, b1, b2;
    //We can pair up every 2 signals into 3 bytes
    b0 = s0&0xff;
    b1 = ((s0>>4)&0xf0) | ((s1>>8)&0x0f);
    b2 = s1&0xff;

    //Then reconstruct on the other side
    s0 = (uint16_t)b0 | (((uint16_t)b1 & 0xf0) << 4);
    s1 = (uint16_t)b2 | (((uint16_t)b1 & 0x0f) << 8);
*/
    








