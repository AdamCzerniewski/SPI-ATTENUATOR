the purpose of this project is to provide tools for analysis and automation involving the PE4302 SPI attenuator

required items to run this program include the following below:

RIGOL DSA832E Spectrum Analyzer, 
RIGOL DSG821 Signal Generator, 
RASPBERRY PI 4, 
PE4302 SPI attenuator

the PE4302 has to be modified from its standard factory set up otherwise it will not work
J5, J6, and J7 are soldered, and the J4 joint is not soldered

wick the joints highlighted in red (J5, J6, J7) and solder the joint highlighted in green (J4)
![wick3joints_solder1joint](https://github.com/user-attachments/assets/b29ba807-9eef-485b-a78f-a66cde1a2842)


next step is to connect the PE4302 to the RPI
each connection will be color coded

these are the GPIO pins being used on the RPI viewed on [https://www.pinout.xyz](https://pinout.xyz/)
![GPIOPINSCONNECTIONS_SCREENSHOTHIGHLIGHTED](https://github.com/user-attachments/assets/7982f182-6fd7-4c06-a038-4a6d74b1cde5)

these are the main connections (GND, DATA, CLK, LE)
![RPI_GPIO_PIN_CONNECTIONS](https://github.com/user-attachments/assets/86a87aca-c90c-4663-b9ad-0019dc39eb1f)

this is the 5v connection and the second GND connection 
![GROUND_5V_CONNECTIONS](https://github.com/user-attachments/assets/4521af38-fe70-47b7-b209-123f2d918e2a)

the 5v connection is optional as you can connect power to the 3.3v pin. Do not connect the 5v and the 3.3v together
![OPTIONAL_3 3V_CONNECTION](https://github.com/user-attachments/assets/1104492b-345c-4cc6-aad7-bdef6db014e3)

finally, connect the Signal Generator to the input of the attenuator, and connect the Spectrum Analyzer to the output of the attenuator
![SIG_GEN_SPEC_AN_CONNECTION_TOATTEN](https://github.com/user-attachments/assets/bc6dfc84-ede2-47b7-bbd8-c7f52071c471)
