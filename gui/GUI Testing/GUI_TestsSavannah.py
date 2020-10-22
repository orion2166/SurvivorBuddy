def tester(trying, recived, expected, txt_If_True = "Test Passed", txt_If_False = "Test Failed"):

	print("Trying Value: ", trying)
	print("Recieved Value: ",recieved)
	print("Expected Value: ", expected)
	if(recieved == expected):
		print(txt_If_True)
	else:
		print(txt_If_False)

# Function Block 1
print("Begining Tests for Function Block 1 from IDEF0:")


init() #Application.py [1.1]
connect() #SerialArmController.py [1.2]
connect() #Application.py [1.3]
set_status(status) #StatusBar.py [1.4]

# Function Block 3
update_position() #SerialArmController.py [3.1]
append_line() #NotificationsFrame.py [3.2]
update_render() #PositonFrame.py [3.3]
send_command() #NotificationsFrame.py [3.4]
set_pitch(val) #SerialArmController.py [3.5]
set_yaw(val) #SerialArmController.py [3.5]
set_roll(val) #SerialArmController.py [3.5]


