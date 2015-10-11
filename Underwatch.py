import os
from time import sleep
import datetime
import re
from clint.textui import colored
import sys
from argparse import ArgumentParser
import re

class Underwatcher:
	
	def __init__(self, args):
		
		self.running = False
		if not args.path:
			self.setPath()
		else:
			self.path = args.path
		self.timestamp = args.timestamp
		if self.timestamp:
			self.format = args.timestamp
		if args.file:
			self.outputMode = "file"
		elif args.sequence:
			self.outputMode = "sequence"
			if not self.timestamp:
				self.format = "%Y-%m-%d %H.%M.%S"
				self.timestamp = True
		else:
			self.outputMode = "screen"
		if args.outputPath:
			self.outputPath = args.outputPath
		else:
			self.outputPath = os.getcwd()
		self.quiet = args.quiet
		self.exit = not args.noExit
		self.mutlipleFiles = args.mutlipleFiles
		
		self.modtimes = {}
		self.fileContents = {}
		
		self.watchSave = args.watchSave
		if self.watchSave:
			self.modtimes["_saveFile"] = os.path.getmtime("_saveFile")
		self.setSaveDescriptions()
		
		for file in os.listdir(self.path):
			filepath = os.path.join(self.path,file)
			self.modtimes[file] = os.path.getmtime(filepath)
			self.readFile(filepath)
		
	def setPath(self):
		
		if os.path.isfile("_path"):
			with open("_path", 'r') as f:
				self.path = f.read()
		else:
			path = "C:\\Users\\<user>\\AppData\\Local\\UNDERTALE"
			user = os.environ.get("USERNAME")
			path = path.replace("<user>", user)
	
			print("Using {} as Undertale data path".format(path))
			r = input("Is this correct? y/n: ")
			if "n" in r.lower():
				path = input("Path: ")
			with open("_path", 'w') as f:
				print(path, file=f, end="")
			self.path = path
			
	def setSaveDescriptions(self):
		
		with open("_saveFile", 'r') as f:
			self.saveFileLines = [l.strip('\r\n"') for l in f.read().split(",")]
	
	def readFile(self, filepath):
		
		file = filepath.split("\\")[-1]
		with open(filepath, 'r') as f:
			if 'ini' in file:
				self.fileContents[file] = {}
				for line in f.readlines():
					if '[' in line:
						section = section = line.strip("\r\n[]")
						self.fileContents[file][section] = {}
					elif '=' in line:
						key = line.split("=")[0]
						value = line.split("=")[1].split('"')[1]
						self.fileContents[file][section][key] = value
			else:
				self.fileContents[file] = []
				for line in f.readlines():
					self.fileContents[file].append(line)
	
	def start(self):
		self.running = True
		if not self.quiet:
			print("Underwatch started.")
		while True:
			try:
				for file in os.listdir(self.path):
					self.currentFile = file
					filepath = os.path.join(self.path,file)
					modtime = os.path.getmtime(filepath)
					if file in self.modtimes:
						modified = modtime != self.modtimes[file]
					else:
						self.modtimes[file] = modtime
						self.output("File created: {}".format(file))
						if file == "playerachievementcache.dat":
							modified = False
						else:
							modified = True
					if modified:
						if file == "playerachievementcache.dat" and self.exit: # As far as I know this file is only modified when exiting the game
							sys.exit(0)										   # (other than on creation) and it's easier than checking for the process
						self.modtimes[file] = modtime
						if self.timestamp and not self.outputMode == "sequence":
							modDatetime = datetime.datetime.fromtimestamp(self.modtimes[file])
							self.output("{}".format(modDatetime.strftime(self.format)))
						if not self.mutlipleFiles:
							self.output("{} changed".format(file))
						elif not self.quiet:
							print("{} changed".format(file))
						if '.ini' in file:
							self.parseini(filepath)
						elif 'file' in file:
							self.parseSave(filepath)
						self.output("")
				if self.watchSave:
					modtime = os.path.getmtime("_saveFile")
					if modtime != self.modtimes["_saveFile"]:
						self.modtimes["_saveFile"] = modtime
						self.setSaveDescriptions()
				sleep(0.1)
			except KeyboardInterrupt:
				sys.exit(0)
					
	def output(self,output):
		escapePattern = re.compile(r'\x1b[^m]*m')
		cleanOutput = escapePattern.sub("", output)  # Strip the escape codes used to colour the ouput
		if not self.quiet:
			print(output)
		if self.outputMode == "file":
			if self.mutlipleFiles:
				filename = "{}.log".format(self.currentFile)
			else:
				filename = "Underwatch.log"
			filepath = os.path.join(self.outputPath, filename)
			if os.path.isfile(filepath):
				mode = 'a'
			else:
				mode = 'w'
			with open(filepath, mode) as f:
				print(cleanOutput, file=f)
		elif self.outputMode == "sequence":
			if self.mutlipleFiles:
				filename = "{}.{}.log".format(self.currentFile, "{}")
			else:
				filename = "Underwatch.{}.log"
			modDatetime = datetime.datetime.fromtimestamp(self.modtimes[self.currentFile])
			filepath = os.path.join(self.outputPath, filename.format(modDatetime.strftime(self.format)))
			if os.path.isfile(filepath):
				mode = 'a'
			else:
				mode = 'w'
			with open(filepath, mode) as f:
				print(cleanOutput, file=f)
				
	def parseini(self, filepath):
		file = filepath.split("\\")[-1]
		with open(filepath, 'r') as f:
			for line in f.readlines():
				if '[' in line:
					section = line.strip("\r\n[]")
					sectionPrinted = False
					if not file in self.fileContents:
						self.fileContents[file] = {}
					if not section in self.fileContents[file]:
						self.fileContents[file][section] = {}
				elif '=' in line:
					key = line.split("=")[0]
					value = line.split("=")[1].split('"')[1]
					if key not in self.fileContents[file][section]:
						self.fileContents[file][section][key] = "_"
					original = self.fileContents[file][section][key]
					if value != original:
						if not sectionPrinted:
							self.output("[{}]".format(section))
							sectionPrinted = True
						self.output("{}: {} >> {}".format(key, colored.red(original), colored.green(value)))
						self.fileContents[file][section][key] = value

	def parseSave(self, filepath):
		file = filepath.split("\\")[-1]
		with open(filepath, 'r') as f:
			i = 0
			for line in f.readlines():
				if file not in self.fileContents:
					self.fileContents[file] = []
				if len(self.fileContents[file]) <= i:
					self.fileContents[file].append("_")
				original = self.fileContents[file][i]
				if line != original:
					description = self.saveFileLines[i]
					if description == "":
						description = "unknown"
					self.output("({}) {} >> {} ({})".format(i+1, colored.red(original), colored.green(line), description).replace('\n','').replace('\r',''))
					self.fileContents[file][i] = line
				i += 1

if __name__ == "__main__":
	parser = ArgumentParser()
	parser.add_argument("-p", "--path", dest="path", help="explicitly set the Undertale save folder, overrides _path file")
	fileOutGroup = parser.add_mutually_exclusive_group()
	fileOutGroup.add_argument("-f", "--file", action="store_true", help="output all changes to Underwatch.log.")
	fileOutGroup.add_argument("-s", "--sequence", action="store_true", help="output each change to a timestamped file. The format is %%Y-%%m-%%d %%H.%%M.%%S by default, and can be changed with -t")
	parser.add_argument("-m", "--multiple", dest="mutlipleFiles", action="store_true", help="output changes to multiple files (save0.log, undertale.ini.log, etc.)")
	parser.add_argument("-o", "--out", dest="outputPath", metavar="PATH", help="explicitly set the output directory, default is the working directory")
	parser.add_argument("-t", "--time", nargs="?", dest="timestamp", metavar="FORMAT", const="[%H:%M:%S]", help="output a timestamp with each change. The default format is [%%H:%%M:%%S], see readme.txt for format options")
	parser.add_argument("-u", "--update", dest="watchSave", action="store_true", help="monitor _saveFile, allows updating of descriptions without restarting")
	parser.add_argument("-q", "--quiet", help="don't ouput to the screen.", action="store_true")
	parser.add_argument("-x", "--no-exit", dest="noExit", action="store_true", help="prevent Underwatch from closing when Undertale closes (CRTL+C to kill Underwatch)")
	args = parser.parse_args()
	watcher = Underwatcher(args)
	watcher.start()