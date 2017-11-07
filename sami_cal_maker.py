# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import csv, sys

"""
	Takes in a PHSENA or PCO2WA certification text file and produces a CSV file of the values.
	The text document derives from a file provided by Sunburst that contains the calibration values
	
"""
file = open(sys.argv[1], 'r')

def pco2_maker(file): 
	""" Produces a PCO2W calibration file based on the format dictated by OOI.

		Args:
			file (str): the name of the calibration text file


	"""
	# Reads text file
	lines = file.readlines()
	# Maps value
	keys = [key.strip(' ').rstrip() for key in lines[0].split("\t")]
	values = [value.strip(' ').rstrip() for value in lines[1].split("\t")]

	data = dict(zip(keys, values))
	# Set up CSV writing
	wr = csv.writer(open("PCO2W_Cal_File.csv", "w", newline=''))

	equivalent = {"CC_cala" : "SAMI_A", "CC_calb" : "SAMI_B", "CC_calc" : "SAMI_C", "CC_calt" : "AvgT"} 
	constants = {"CC_ea434": 19706, "CC_ea620": 34, "CC_eb434": 3073, "CC_eb620": 44327}
	csv_format = ["CC_cala", "CC_calb", "CC_calc", "CC_calt", "CC_ea434", "CC_ea620", "CC_eb434", "CC_eb620"]
	csv_maker(wr, csv_format, data, constants, equivalent)

def phsen_maker(file):
	""" Produces a PHSEN calibration file based on the format dictated by OOI.

		Args:
			file (str): the name of the calibration text file

	"""

	data = {}
	for line in file.readlines():
		key, val = line.split("	")
		data[key] = val

	# Set up CSV writing
	wr = csv.writer(open("PHSEN_Cal_File.csv", "w", newline=''))

	equivalent = {"CC_ea434" : "Ea_434", "CC_eb434" : "Eb_434", "CC_ea578" : "Ea_578", "CC_eb578": "Eb_578"} 
	constants = {"CC_ind_off": 0, "CC_ind_slp": 1, "CC_psal": 35}
	csv_format = ["CC_ea434", "CC_ea578", "CC_eb434", "CC_eb578", "CC_ind_off", "CC_ind_slp", "CC_psal"]
	csv_maker(wr, csv_format, data, constants, equivalent)

def csv_maker(wr, csv_format, data, constants, equivalent):
	top = ["serial", "name", "value", "notes"]
	wr.writerow(top)
	for val in csv_format:
		row = ["", val]
		if val in equivalent.keys():
			row.append(data[equivalent[val]].rstrip().strip())
		if val in constants:
			row.append(constants[val])
		wr.writerow(row)


lines = 0
with open(sys.argv[1]) as f:
	for line in f:
		lines += 1

if lines == 2:
	print(lines)
	pco2_maker(file)
else:
	print(lines, "PHSEN")
	phsen_maker(file)
