import os
import sys
import hashlib
import zlib

def printHashes(prefix, data):
	crc32 = format(zlib.crc32(data), "x")
	md5 = hashlib.md5(data).hexdigest()
	sha1 = hashlib.sha1(data).hexdigest()
	print(f"{prefix}:\n crc32 {crc32}\n md5   {md5}\n sha1  {sha1}")

def loadFile(filename):
	try:
		fileHandle = open(filename, 'rb')
		fileSize = os.path.getsize(filename)
		fullFileData = fileHandle.read(fileSize) # hopefully there's enough memory lol
		fileHandle.close()
		isGbx = False
		if (fileSize >= 4):
			last4Bytes = fullFileData[-4:]
			if (last4Bytes == b'GBX!'):
				isGbx = True
		print()
		print(f"File: {filename} Size: {fileSize} bytes")
		gbxFooter = None
		if (isGbx):
			gbxFooter = readFooter(fullFileData)
			if (gbxFooter):
				print()
				parseFooter(gbxFooter)
			else:
				print()
				print("Invalid GBX footer")
		else:
			print("No GBX footer detected")
		print()
		printHashes("File hashes", fullFileData);
		if (gbxFooter):
			romWithoutFooter = fullFileData[0:-len(gbxFooter)]
			printHashes("ROM data hashes", romWithoutFooter)
			printHashes("Footer hashes", gbxFooter)
	except FileNotFoundError:
		print("File not found")
	print()	

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
		
def readFooter(fullFileData):
	fileSize = len(fullFileData)
	if (fileSize < 16):
		return None
	footerSize = bytesToInt(fullFileData[fileSize - 16:fileSize - 12])
	if (fileSize < footerSize):
		return None
	gbxFooter = fullFileData[fileSize - footerSize:]
	return gbxFooter

import sys
if len(sys.argv) != 2:
	print("usage: py gbx.py filename.gbx")
	exit()
loadFile(sys.argv[1])
