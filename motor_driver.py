#This is code of Raspberry Car
import RPi.GPIO as GPIO
import ConfigParser

class CarControler():

	def __init__(self):
		#read config information
		config = ConfigParser.ConfigParser()
		config.read("config.ini")
		self.LeftMotor_pin1  = config.getint("motor_param","LeftMotor_pin1")
		self.LeftMotor_pin2	 = config.getint("motor_param","LeftMotor_pin2")
		self.RightMotor_pin1 = config.getint("motor_param","RightMotor_pin1")
		self.RightMotor_pin2 = config.getint("motor_param","RightMotor_pin2")
		self.PWM_frequency 	 = config.getint("motor_param","PWM_frequency")
		self.VISION_Kp		 = config.getfloat("motor_param","VISION_Kp")

		#init
		GPIO.setwarnings(False)
		GPIO.setmode(GPIO.BOARD)
		GPIO.setup(self.LeftMotor_pin1,GPIO.OUT)
		GPIO.setup(self.LeftMotor_pin2,GPIO.OUT)
		GPIO.setup(self.RightMotor_pin1,GPIO.OUT)
		GPIO.setup(self.RightMotor_pin2,GPIO.OUT)
		
		self.LeftMotor_PWM1  = GPIO.PWM(self.LeftMotor_pin1,self.PWM_frequency)
		self.LeftMotor_PWM2  = GPIO.PWM(self.LeftMotor_pin2,self.PWM_frequency)
		self.RightMotor_PWM1 = GPIO.PWM(self.RightMotor_pin1,self.PWM_frequency)
		self.RightMotor_PWM2 = GPIO.PWM(self.RightMotor_pin2,self.PWM_frequency)

	def stop(self):
		self.LeftMotor_PWM1.stop()
		self.LeftMotor_PWM2.stop()
		self.RightMotor_PWM1.stop()
		self.RightMotor_PWM2.stop()

	def moveforward(self):
		self.LeftMotor_PWM1.start(40)
		self.LeftMotor_PWM2.start(0)
		self.RightMotor_PWM1.start(40)
		self.RightMotor_PWM2.start(0)
		
	def movebackward(self):
		self.LeftMotor_PWM1.start(0)
		self.LeftMotor_PWM2.start(40)
		self.RightMotor_PWM1.start(0)
		self.RightMotor_PWM2.start(40)

	def turnleft(self):
		self.LeftMotor_PWM1.start(30)
		self.LeftMotor_PWM2.start(0)
		self.RightMotor_PWM1.start(70)
		self.RightMotor_PWM2.start(0)
		
	def turnright(self):
		self.LeftMotor_PWM1.start(70)
		self.LeftMotor_PWM2.start(0)
		self.RightMotor_PWM1.start(30)
		self.RightMotor_PWM2.start(0)

	def autorun(self,bias):	
		Error = bias * self.VISION_Kp
		if Error > 0 :
			if Error > 35 :
				Error = 35
			self.LeftMotor_PWM1.start(30-0.53*Error)
			self.LeftMotor_PWM2.start(0)
			self.RightMotor_PWM1.start(30+Error)
			self.RightMotor_PWM2.start(0)
		elif Error < 0 :
			if Error < -35 :
				Error = -35
			self.LeftMotor_PWM1.start(30-Error)
			self.LeftMotor_PWM2.start(0)
			self.RightMotor_PWM1.start(30+0.53*Error)
			self.RightMotor_PWM2.start(0)


if __name__ == "__main__":
	RaspCar = CarControler()
	while(True):
		direction = input("direction:")
		if direction == 1:
			RaspCar.moveforward()
		elif direction == 2:
			RaspCar.movebackward()
		elif direction == 3:
			RaspCar.turnleft()
		elif direction == 4:
			RaspCar.turnright()
		else:
			RaspCar.stop()






		
