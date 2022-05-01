#! /usr/bin/env python
# -*- coding: utf-8 -*-
from my_package.ft_serial_1 import Serial
from my_package.conf_com_port import configure_window
from my_package.chat import chat

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
	ser = Serial()
	ok_button = configure_window(ser)
	# ser.timeout = 2
	if ok_button:
		chat(ser)


if __name__== "__main__":
	main()
