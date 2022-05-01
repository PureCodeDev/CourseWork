#! /usr/bin/env python
# -*- coding: utf-8 -*-
from tkinter.messagebox import *
from my_package.configurations import BAUDRATES, BYTESIZES, PARITIES, STOPBITS

cut_port = []
##---Обрезаем полное имя COM-порта до <COM(цифра)>
def cut_port_name(str):
	global cut_port
	for i in range(len(str)):
		cut_port.append(str[i])
		cut_port[i] = cut_port[i].device
	return cut_port


def validation(name, com_port, speed_b, size_b, parity_b, bit_stop, ser):
	"""
	Валидация параметров COM-порта
	"""
	username = name.get()
	if not username:
		showerror("Пользователь не определен.", "Пожалуйста, введите имя")
		return False
	ser.username = username
	port = com_port.get()
	if port not in cut_port:
		showerror("Некорректный COM-порт.", port + " не существует")
		return False
	ser.port = port
	speed = speed_b.get()
	# speed_u = unicode(speed, 'utf-8')
	if int(speed) not in BAUDRATES:
		showerror("Некорректная скорость.", speed + " не существует")
		return False
	ser.baudrate = speed
	byte_size = size_b.get()
	# byte_size_u = unicode(byte_size, 'utf-8')
	if int(byte_size) not in BYTESIZES:
		showerror("Плохой размер байта.", byte_size + " не существует")
		return False
	ser.bytesize = int(byte_size)
	parity = parity_b.get()
	if parity not in PARITIES:
		showerror("Плохой бит четности.", parity + " не существует")
		return False
	ser.parity = parity
	stopbits = bit_stop.get()
	# stopbits_u = unicode(stopbits, 'utf-8')
	# if stopbits_u.isnumeric() == False or float(stopbits) not in STOPBITS:
	try:
		if float(stopbits) not in STOPBITS:
			showerror("Плохой стопбит.", stopbits + " не существует")
			return False
	except:
		showerror("Плохой стопбит.", stopbits + " не существует")
		return False
	ser.stopbits = float(stopbits)
	return True
