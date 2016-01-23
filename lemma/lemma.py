# -*- coding: utf-8 -*-
from pymystem3 import Mystem

def Analyze():
	mystem = Mystem()
	result = mystem.analyze('У попа была собака он ее любил')
	print result[2]['analysis'][0]['gr']

#if __name__ == 'main':
Analyze()