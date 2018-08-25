#include <stdio.h>
#include <math.h>
/* Dynamixel Basic Position Control Example
 
 Turns left the dynamixel , then turn right for one second,
 repeatedly.
 
                   Compatibility
 CM900                  O
 OpenCM9.04             O
 
                  Dynamixel Compatibility
               AX    MX      RX    XL-320    Pro
 CM900          O      O      O        O      X
 OpenCM9.04     O      O      O        O      X
 **** OpenCM 485 EXP board is needed to use 4 pin Dynamixel and Pro Series ****
 
 created 16 Nov 2012
 by ROBOTIS CO,.LTD.
 */
 
/* Serial device defines for dxl bus */
#define DXL_BUS_SERIAL1 1  //Dynamixel on Serial1(USART1)  <-OpenCM9.04
#define DXL_BUS_SERIAL2 2  //Dynamixel on Serial2(USART2)  <-LN101,BT210
#define DXL_BUS_SERIAL3 3  //Dynamixel on Serial3(USART3)  <-OpenCM 485EXP


/* Control table defines */
#define GOAL_POSITION 30
#define PRESENT_POSITION 36
#define R1 5
#define R2 4
#define R3 3
#define low_pwm 240
#define high_pwm 800
#define middle_pwm 512
#define arm_length 27 //cm

int z=0;
int pwm1=0;
int pwm3=0;
int present=0;
char data[2];
int p_data[2];

int get_pwm(int z)
{
  int pwm;
  double theta;
  double distance;
  distance = z-arm_length;

  theta = asin(distance/arm_length);
 SerialUSB.println(theta);
//  pwm = map(theta, -M_PI/2, M_PI/2, low_pwm, high_pwm); 
  pwm = theta* (high_pwm-low_pwm)/M_PI + 512;
   SerialUSB.println(pwm);
  return pwm;
}

Dynamixel Dxl(DXL_BUS_SERIAL3);

void setup()
{  
  // Dynamixel 2.0 Baudrate -> 0: 9600, 1: 57600, 2: 115200, 3: 1Mbps 
  Dxl.begin(3);
  Dxl.jointMode(R1); //jointMode() is to use position mode
  SerialUSB.begin();

}

void loop()
{
  int i;
  if(SerialUSB.available())
  {
    for(i=0; i<2; i++)
    {
      data[i] = SerialUSB.read();
      p_data[i] = data[i] - '0';
    }

    z = p_data[0] * 10 + p_data[1]; //z_position
    SerialUSB.println(z);

    pwm1 = get_pwm(z);
    //R3
    if ((low_pwm<=pwm1)&&(pwm1<= middle_pwm))
      pwm3 = map(pwm1, low_pwm, middle_pwm, 512, 600); 
      
    if ((middle_pwm<pwm1)&&(pwm1<= high_pwm))
      pwm3 = map(pwm1, (middle_pwm+1), high_pwm, 600, 513);
      
    Dxl.writeWord(R1, GOAL_POSITION, pwm1);     
    Dxl.writeWord(R3, GOAL_POSITION, pwm3);
    Dxl.writeWord(4, GOAL_POSITION, 512);
    //swing
      
    Dxl.writeWord(R2, GOAL_POSITION, 650);
    delay(500);  
    Dxl.writeWord(R2, GOAL_POSITION, 400);
//    delay(500);  
//    Dxl.writeWord(4, GOAL_POSITION, 512);
    
   }    
}


 
