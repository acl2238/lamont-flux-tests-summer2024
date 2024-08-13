For Nick Frearson's reference

Instructions:

To run the data collection program at startup on newer models (likely including the one you are using:
1. Open terminal
2. Type "nano ~/.config/wayfire.ini"
3. Input these lines at the end of the file:

[autostart]

run = lxterminal -e python3 (path to script)

The path to script will look something like /home/name/.../k30.py

4. Make sure that all requirements are satisfied (refer to requirements.txt)
5. Make sure all hardware is plugged in (batteries plugged in, GPS plugged into USB, pump on, etc)
6. Edit the destination file in k30.py to point to whatever directory you want to save data to (I recommend making a folder in the code directory for storing all data)
7. reboot

The program will run continuously in a loop, and turning the switch to an "on" position will start logging today. Turning the switch to the "off" position will stop the dataogging and the program will wait for the next switch pull to start logging data again. Ideally the switch should be mounted to something and states labeled. 

Wiring Schematics:

<img width="1327" alt="Screenshot 2024-08-13 at 11 30 02 AM" src="https://github.com/user-attachments/assets/7767787a-15c0-41ce-8aff-20ab013452ba">

<img width="1316" alt="Screenshot 2024-08-13 at 11 35 55 AM" src="https://github.com/user-attachments/assets/9c9c1ffa-8757-4b72-809f-14b458381a6e">

<img width="1316" alt="Screenshot 2024-08-13 at 11 48 17 AM" src="https://github.com/user-attachments/assets/98e77b49-7974-4545-afa5-ead21a816733">

