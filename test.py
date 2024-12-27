# defaults read ~/Library/Preferences/com.apple.HIToolbox.plist AppleSelectedInputSources
import os
import re


command = 'defaults read ~/Library/Preferences/com.apple.HIToolbox.plist AppleSelectedInputSources'
line = []
outdata = []

out = os.popen(command).read()

for x in range(0,len(out),30):
	line = out[x:x+30].replace("\n","")
	outdata.append(line)

index = outdata[4].find('U.S.')
#print(index)

if index>-1:
	print("Англиский")
else:
	print("Русский")