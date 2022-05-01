#! /usr/bin/env python
# -*- coding: utf-8 -*-
from asyncio.windows_events import NULL
import tkinter as tk
from tkinter.ttk import *

from numpy import empty

from my_package.configurations import BAUDRATES, BYTESIZES, PARITIES, STOPBITS
import serial
from serial.tools import list_ports
from my_package.validation import validation, cut_port_name

def configure_window(ser):
	global ok_button
	ok_button = False

	"""Создание окна настроек параметров"""
	conf_window = tk.Tk()
	
	screen_width = conf_window.winfo_screenwidth()#центрируем окно
	screen_height = conf_window.winfo_screenheight()

	x_cordinate = int((screen_width/2) - (350/2))
	y_cordinate = int((screen_height/2) - (200/2))

	conf_window.geometry("350x200+{}+{}".format(x_cordinate, y_cordinate-50))#-50 for a eye beaty
	#conf_window.geometry('350x200')
	conf_window.title('Конфигурация соединения')
	conf_window['bg'] = '#DCDCDC'

	"""Имя пользователя"""
	label_name = tk.Label(conf_window, text='Пользователь:', font=("Algerian", 15), bg='#DCDCDC')
	label_name.grid(row=0, column=0)
	default_name = tk.StringVar(conf_window, value='A')
	name = tk.Entry(conf_window, width=23, textvariable=default_name)
	name.grid(row=0, column=2)

	"""COM-port"""
	label_port = tk.Label(conf_window, text='Порт:', font=("Algerian", 15), bg='#DCDCDC')
	label_port.grid(row=1, column=0)
	com_port = Combobox(conf_window)

	com_port['values'] = cut_port_name(list_ports.comports())
	com_port.current(0)
	com_port.grid(row=1, column=2)

	"""Скорость обмена"""
	label_speed = tk.Label(conf_window, text='Скорость:', font=("Algerian", 15), bg='#DCDCDC')
	label_speed.grid(row=2, column=0)
	speed_b = Combobox(conf_window)
	speed_b['values'] = BAUDRATES
	speed_b.current(12)
	speed_b.grid(row=2, column=2)

	"""Размер байта"""
	label_byte_size = tk.Label(conf_window, text='Размер байта:', font=("Algerian", 15), bg='#DCDCDC')
	label_byte_size.grid(row=3, column=0)
	size_b = Combobox(conf_window)
	size_b['values'] = BYTESIZES
	size_b.current(3)
	size_b.grid(row=3, column=2)

	"""Бит четности"""
	label_bit_parity = tk.Label(conf_window, text='Бит четности:', font=("Algerian", 15), bg='#DCDCDC')
	label_bit_parity.grid(row=4, column=0)
	parity_b = Combobox(conf_window)
	parity_b['values'] = PARITIES
	parity_b.current(0)
	parity_b.grid(row=4, column=2)

	"""Стоп бит"""
	label_stop_bit = tk.Label(conf_window, text='Стоп бит:', font=("Algerian", 15), bg='#DCDCDC')
	label_stop_bit.grid(row=5, column=0)
	bit_stop = Combobox(conf_window)
	bit_stop['values'] = STOPBITS
	bit_stop.current(0)
	bit_stop.grid(row=5, column=2)

	##-- Настройки сохраняются
	def clicked(event):
		global ok_button
		if validation(name, com_port, speed_b, size_b, parity_b, bit_stop, ser):
			conf_window.destroy()
			ok_button = True


	"""Кнопка завершения настроек"""
	button = tk.Button(conf_window, text="Готово!", command=clicked, bg='white')
	button.focus_set()
	button.bind('<Button-1>', clicked)
	button.bind('<Return>', clicked)

	label_name = tk.Label(conf_window, text='          ', font=("Algerian", 15), bg='#DCDCDC')
	label_name.grid(row=0, column=1)
	
	button.grid(column=0, columnspan = 3, sticky = tk.W+tk.E)

	conf_window.mainloop()
	return ok_button