import re
f = open('voyna-i-mir-tom-1.txt', 'rt')
text = []
i=0
text2 = []
serch = " а полк прошел тысячу верст."
ok = 0

def returnline(input_txt):
	for i in range(len(input_txt)):	
			if input_txt[i] != "\n":				
				return input_txt[i]

for line in f:
	#print(str(i)+" "+line)
	# text.append(line)
	index = line.find(serch)
	if index != -1:
		print("совподение найдено - "+str(i))
		out=line.split(serch)

		for x in range(0,len(out[1]),70):
			text2.append(out[1][x:x+70])

		if text2[0]!="\n":			
			print(text2[0])
			break
		else:
			print("но строки нет")
			ok=1

	elif ok==1:

		print("следующая строка - "+str(i))

		for x in range(0,len(line),70):
			text2.append(line[x:x+70])

		print(returnline(text2))
		break
			
	i+=1




