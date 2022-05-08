#! /usr/bin/env python
# -*- coding: utf-8 -*-
from concurrent.futures import thread
from my_package.ft_serial_1 import Serial
from my_package.conf_com_port import configure_window
from my_package.chat import chat
from threading import Thread
from multiprocessing import Process
##---Fox exe
if 0:
	import UserList
	import UserString
	import UserDict
	import itertools
	import collections
	import future.backports.misc
	import commands
	import base645
	import __buildin__
	import math
	import reprlib
	import functools
	import re
	import subprocess
###


def main():
	ser1 = Serial()
	ser2 = Serial()
	ok_button = configure_window(ser1,ser2)
	# ser.timeout = 2
	if ok_button:
		th1 = Thread(target=chat, args=ser1)
		th1.start()
		#th2 = Thread(target = chat, args = (ser2))
		#th2.start()


if __name__== "__main__":
	main()
