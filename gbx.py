import os
import sys

def loadFile(filename):
	try:
		fileHandle = open(filename, 'rb')
		fileSize = os.path.getsize(filename)
		isGbx = False
		if (fileSize >= 4):
			fileHandle.seek(fileSize - 4)
			last4Bytes = fileHandle.read(4)
			if (last4Bytes == b'GBX!'):
				isGbx = True
			fileHandle.seek(0)
		print(f"File: {fileHandle.name} Size: {fileSize} bytes")
		if (isGbx):
			gbxFooter = readFooter(fileHandle, fileSize)
			if (gbxFooter):
				parseFooter(gbxFooter)
			else:
				print("Invalid GBX footer")
		else:
			print("No GBX footer detected")
		fileHandle.close()
	except FileNotFoundError:
		print("file not found")

def bytesToInt(bytes):
	return int(bytes.hex(), 16)
	
def parseFooter(footer):

	MAX_SUPPORTED_MAJOR_VERSION = 1

	footerMajVer = bytesToInt(footer[-12:-8])
	footerMinVer = bytesToInt(footer[-8:-4])
	footerSize = bytesToInt(footer[-16:-12])

	print(f"GBX footer found - ver {footerMajVer}.{footerMinVer}, size {footerSize} bytes")

	if (footerMajVer != MAX_SUPPORTED_MAJOR_VERSION):
		print("GBX version not supported!!")
		return False

	if (footerSize < 16):
		print("invalid footer size!!")
		return False
	
	mapper = footer[0:4].decode('ascii')
	romSize = bytesToInt(footer[8:12])
	ramSize = bytesToInt(footer[12:16])

	print(f"Mapper {mapper} / Batt {footer[4]} / Rumble {footer[5]} / RTC {footer[6]} / ROM {romSize} bytes / RAM {ramSize} bytes")

	return True
		
def readFooter(fileHandle, fileSize):
	if (fileSize < 16):
		return None
	fileHandle.seek(fileSize - 16)	
	footerSize = bytesToInt(fileHandle.read(4))
	if (fileSize < footerSize):
		fileHandle.seek(0)
		return None
	fileHandle.seek(fileSize - footerSize)
	gbxFooter = fileHandle.read(footerSize)
	fileHandle.seek(0)
	return gbxFooter

import sys
if len(sys.argv) != 2:
	print("usage: python gbx.py filename.gbx")
	exit()
loadFile(sys.argv[1])
