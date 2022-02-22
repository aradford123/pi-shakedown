#!/usr/bin/env python
import sys, os
from Motor import Motor

def main():
    PWM=Motor()
    PWM.setMotorModel(0,0,0,0)      

if __name__ == "__main__":
    main()
