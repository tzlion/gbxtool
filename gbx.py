import os
import sys
import hashlib
import zlib

def bytesToInt(bytes):
	return int(bytes.hex(), 16)

class FooterData:

	def __init__(self, mapper, hasBattery, hasRumble, hasRtc, romSize, ramSize):
		self.mapper = mapper
		self.hasBattery = hasBattery
		self.hasRumble = hasRumble
		self.hasRtc = hasRtc
		self.romSize = romSize
		self.ramSize = ramSize
		
class RomManager:

	fullRom = None
	isGbx = False
	gbxFooter = None
	romWithoutFooter = None
	
	def load(self, filename):
		fileHandle = open(filename, 'rb')
		fileSize = os.path.getsize(filename)
		self.fullRom = fileHandle.read(fileSize) # hopefully there's enough memory lol
		fileHandle.close()	
		self.isGbx = False
		if (fileSize >= 4):
			last4Bytes = self.fullRom[-4:]
			if (last4Bytes == b'GBX!'):
				self.isGbx = True
				self._readFooter()

	def _readFooter(self):
		fileSize = len(self.fullRom)
		if (fileSize < 16):
			return None
		footerSize = bytesToInt(self.fullRom[fileSize - 16:fileSize - 12])
		if (fileSize < footerSize):
			return None
		self.gbxFooter = self.fullRom[fileSize - footerSize:]
		self.romWithoutFooter = self.fullRom[0:-len(self.gbxFooter)]
		
class RomReader:

	def printHashes(self, prefix, data):
		crc32 = format(zlib.crc32(data), "x")
		md5 = hashlib.md5(data).hexdigest()
		sha1 = hashlib.sha1(data).hexdigest()
		sha256 = hashlib.sha256(data).hexdigest()
		print(f"{prefix}:\n crc32  {crc32}\n md5    {md5}\n sha1   {sha1}\n sha256 {sha256}")

	def loadFile(self, filename):
		try:
			romManager = RomManager()
			romManager.load(filename)
			print()
			print(f"File: {filename} Size: {len(romManager.fullRom)} bytes")
			if (romManager.isGbx):
				if (romManager.gbxFooter):
					print()
					self.parseFooter(romManager.gbxFooter)
				else:
					print()
					print("Invalid GBX footer")
			else:
				print("No GBX footer detected")
			print()
			self.printHashes("File hashes", romManager.fullRom)
			if (romManager.gbxFooter):
				self.printHashes("ROM data hashes", romManager.romWithoutFooter)
				self.printHashes("Footer hashes", romManager.gbxFooter)
		except FileNotFoundError:
			print("File not found")
		print()	
		
	def parseFooter(self, footer):

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
		
		return FooterData(mapper, footer[4], footer[5], footer[6], romSize, ramSize)

import sys
if len(sys.argv) != 2:
	print("usage: py gbx.py filename.gbx")
	exit()
romReader = RomReader()	
romReader.loadFile(sys.argv[1])
