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
	
	def parse(self, footer):
		self.majorVer = bytesToInt(footer[-12:-8])
		self.minorVer = bytesToInt(footer[-8:-4])
		self.size = bytesToInt(footer[-16:-12])
		if (self.majorVer > gbxMajorVer or (self.majorVer == gbxMajorVer and self.minorVer > gbxMinorVer)):
			return # unsupported version
		self.supportedVer = True
		self.mapper = footer[0:4].decode('ascii')
		self.romSize = bytesToInt(footer[8:12])
		self.ramSize = bytesToInt(footer[12:16])
		self.hasBattery = footer[4]
		self.hasRtc = footer[5]
		self.hasRumble = footer[6]
		
class RomLoader:

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

class RomManager:

	_romLoader = None
	_footerData = None
	
	loadedNonGbx = False
	loadedGbx = False

	def printHashes(self, prefix, data):
		crc32 = format(zlib.crc32(data), "x")
		md5 = hashlib.md5(data).hexdigest()
		sha1 = hashlib.sha1(data).hexdigest()
		sha256 = hashlib.sha256(data).hexdigest()
		print(f"{prefix}:\n crc32  {crc32}\n md5    {md5}\n sha1   {sha1}\n sha256 {sha256}")

	def loadFile(self, filename):
		try:
			self._romLoader = RomLoader()
			self._romLoader.load(filename)
			print()
			print(f"File loaded: {filename} Size: {len(self._romLoader.fullRom)} bytes")
			if (self._romLoader.isGbx):
				if (self._romLoader.gbxFooter):
					print()
					self._footerData = self._parseFooter()
					if (self._footerData.supportedVer):
						self.loadedGbx = True
				else:
					print()
					print("Invalid GBX footer")
			else:
				self.loadedNonGbx = True
				print("No GBX footer detected")
		except FileNotFoundError:
			print("File not found")
		print()	
		
	def printAllHashes(self):
		self.printHashes("File hashes", self._romLoader.fullRom)
		if (self._romLoader.gbxFooter):
			self.printHashes("ROM data hashes", self._romLoader.romWithoutFooter)
			self.printHashes("Footer hashes", self._romLoader.gbxFooter)
	
	def _parseFooter(self):
		footerData = FooterData()
		footerData.parse(self._romLoader.gbxFooter)
		print(f"GBX footer found: ver {footerData.majorVer}.{footerData.minorVer}, size {footerData.size} bytes")	
		if (not footerData.supportedVer):
			print("GBX version not supported!!")
		else:
			print(f"Mapper {footerData.mapper} / Batt {footerData.hasBattery} / Rumble {footerData.hasRumble} / RTC {footerData.hasRtc} / ROM {footerData.romSize} bytes / RAM {footerData.ramSize} bytes")
		return footerData

print(f"GBX ROM Tool v{gbxMajorVer}.{gbxMinorVer}.{scriptRevisionVer}")
if len(sys.argv) != 2:
	print("Usage: py gbx.py filename.gbx")
	exit()

romManager = RomManager()
romManager.loadFile(sys.argv[1])

if (romManager.loadedGbx):
	validOptions = ["h", "e", "r", "x"]
	print("Options: (H) Display hashes / (E) Edit footer / (R) Remove footer / (X) Exit")
elif (romManager.loadedNonGbx):
	validOptions = ["h", "a", "x"]
	print("Options: (H) Display hashes / (A) Add footer / (X) Exit")
else:
	validOptions = ["h", "x"]
	print("Options: (H) Display hashes / (X) Exit")

mode = None
while (mode not in validOptions):
	mode = input("Enter option: ").lower()
print()	

if (mode == "h"):
	romManager.printAllHashes()
elif (mode == "a"):
	print("add not done yet")
elif (mode == "r"):
	print("remove not done yet")
elif (mode == "e"):
	print("edit not done yet")
else:
	print("Bye")
print()	