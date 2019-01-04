import visa
import keyboard
import time
import string




rm = visa.ResourceManager()
print(rm.list_resources())
controller = rm.open_resource('GPIB0::11::INSTR')
print(controller.query('*IDN?'))

print("Control the paddles with w,e for going up and s,d for going down")
leftPaddles = 0
rightPaddles = 0
while True:
    if keyboard.is_pressed('q'):
        print('Quit!')
        break;
    if keyboard.is_pressed('w'):
        leftPaddles = leftPaddles + 1
        string1 = ':PADD1:POSITION ' + str(leftPaddles)
        string2 = ':PADD2:POSITION ' + str(leftPaddles)
        controller.write(string1)
        controller.write(string2)
    if keyboard.is_pressed('e'):
        rightPaddles = rightPaddles + 1
        string1 = ':PADD3:POSITION ' + str(rightPaddles)
        string2 = ':PADD4:POSITION ' + str(rightPaddles)
        controller.write(string1)
        controller.write(string2)
        print(rightPaddles)
    if keyboard.is_pressed('s'):
        leftPaddles = leftPaddles - 1
        string1 = ':PADD1:POSITION ' + str(leftPaddles)
        string2 = ':PADD2:POSITION ' + str(leftPaddles)
        controller.write(string1)
        controller.write(string2)
    if keyboard.is_pressed('d'):
        rightPaddles = rightPaddles - 1
        string1 = ':PADD3:POSITION ' + str(rightPaddles)
        string2 = ':PADD4:POSITION ' + str(rightPaddles)
        controller.write(string1)
        controller.write(string2)
    time.sleep(.1)

#controller.write(':PADD1:POSITION 500')
#controller.write(':PADD2:POSITION 500')
#controller.write(':PADD3:POSITION 500')
#controller.write(':PADD4:POSITION 500')
visa.log_to_screen()
