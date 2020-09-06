import os
import sys
import hashlib
import zlib

gbxMajorVer = 1
gbxMinorVer = 0
scriptRevisionVer = "dev"

def bytesToInt(bytes):
	return int(bytes.hex(), 16)

class FooterData:
	majorVer = None
	minorVer = None
	supportedVer = False
	mapper = None
	hasBattery = None
	hasRumble = None
	hasRtc = None
	romSize = None
	ramSize = None
		
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
		if (fileSize < footerSize or footerSize < 16):
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
		
		footerData = FooterData()

		footerData.majorVer = bytesToInt(footer[-12:-8])
		footerData.minorVer = bytesToInt(footer[-8:-4])
		footerData.size = bytesToInt(footer[-16:-12])
		
		if (footerData.majorVer > gbxMajorVer or (footerData.majorVer == gbxMajorVer and footerData.minorVer > gbxMinorVer)):
			footerData.supportedVer = False
		else:
			footerData.supportedVer = True
		
		if (footerData.supportedVer):
			footerData.mapper = footer[0:4].decode('ascii')
			footerData.romSize = bytesToInt(footer[8:12])
			footerData.ramSize = bytesToInt(footer[12:16])
			footerData.hasBattery = footer[4]
			footerData.hasRtc = footer[5]
			footerData.hasRumble = footer[6]
			
		print(f"GBX footer found - ver {footerData.majorVer}.{footerData.minorVer}, size {footerData.size} bytes")	
			
		if (not footerData.supportedVer):
			print("GBX version not supported!!")

		print(f"Mapper {footerData.mapper} / Batt {footerData.hasBattery} / Rumble {footerData.hasRumble} / RTC {footerData.hasRtc} / ROM {footerData.romSize} bytes / RAM {footerData.ramSize} bytes")
		
		return footerData

import sys
print("GBX ROM Tool v{gbxMajorVer}.{gbxMinorVer}.{scriptRevisionVer}")
if len(sys.argv) != 2:
	print("Usage: py gbx.py filename.gbx")
	exit()
romReader = RomReader()	
romReader.loadFile(sys.argv[1])
