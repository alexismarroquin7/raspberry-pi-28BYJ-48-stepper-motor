# GPIO library
import RPi.GPIO as GPIO 

# time library to pause
import time

# uses numbers configuration for GPIO pins
GPIO.setmode(GPIO.BOARD)


class StepperMotor(): # 28BYJ-48 Stepper Motor
  '''
    * control_pins = [in1, in2, in3, in4]
      * default control_pins values use GPIO.BOARD numbers
  '''
  def __init__(self, control_pins = [ 7 , 11 , 13 ,  15  ]):
    self.control_pins = control_pins
    
    # halfstep sequence
    self.sequence = [ 
      [1,0,0,0],
      [1,1,0,0],
      [0,1,0,0],
      [0,1,1,0],
      [0,0,1,0],
      [0,0,1,1],
      [0,0,0,1],
      [1,0,0,1]
    ]
    
    # direction contants
    self.CLOCKWISE = 'clockwise';
    self.COUNTER_CLOCKWISE = 'counter_clockwise';
    
  def setup (self):
    for pin in self.control_pins:
      GPIO.setup(pin, GPIO.OUT) # set up each pin as an output
      GPIO.output(pin, 0) # initialize pins as OFF / LOW

  def turn (self, degree = 360, direction = ''):
    
    if(direction == ''):
      direction = self.CLOCKWISE # set direction as off by default

    '''
      if degree == 360 it will make 1 rotation (360/360 degrees = 1 rotation)
      if degree == 180 it will make 1/2 rotation (180/360 degrees = 1/2 rotation)
      if degree == 90 it will make 1/4 rotation (90/360 degrees = 1/4 rotation)
      etc...
    '''
    temp = degree / 360; 
    
    '''
      1 revolution = 8 cycles
      gear reduction = 1/64
      8 * 64 = 512 cycles
    '''
    
    # calculates the required amount of steps 
    # 512 steps = 1 rotation
    # 512/2 = 256 steps = 1/2 rotation
    cycles = int(512 * temp); 
    
    # clockwise sequence
    start = 0;
    end = len(self.sequence); # 8
    step = 1;
    
    # if the direction given is counter clockwise, it will iterate through the sequence in reverse
    if(direction == self.COUNTER_CLOCKWISE):
      start = len(self.sequence) - 1; # 7
      end = 0;
      step = -1;
    
    for i in range(cycles):
      for halfstep in range(start, end, step):
        for pin in range(4):
          GPIO.output(self.control_pins[pin], self.sequence[halfstep][pin])
        time.sleep(.001)
    
  
  def cleanup(self):
    GPIO.cleanup()

sm = StepperMotor()
sm.setup()
sm.turn(360, sm.CLOCKWISE)
time.sleep(.1)
sm.turn(360, sm.COUNTER_CLOCKWISE)
sm.cleanup()
