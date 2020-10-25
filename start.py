from rapidfuzz import fuzz
from rapidfuzz import process
from random import *
from tabulate import tabulate
import time, random
import os, sys
import json, markovify
import monkeytelepot
from monkeytelepot.loop import MessageLoop
import psutil
import cpuinfo
from hurry.filesize import size, si
import datetime

def reboottimes():
	reboottimes.rtimes = 0
	reboottimes.mainboot = time.time()
	reboottimes.private_id_list = []
	reboottimes.public_id_list = []
reboottimes()

def lobe_slice(S, step):
    return [S[i::step] for i in range(step)]

def getSize(fileobject):
	fileobject.seek(0,2) # move the cursor to the end of the file
	size = fileobject.tell()
	return size

def restart_line():
	sys.stdout.write('\r')
	sys.stdout.flush()

def bootatpaw():
	os.system("cls")
	print('''
 ╔═╗╔╦╗╔═╗╔═╗╦ ╦ VERSION 3.0
 ╠═╣ ║ ╠═╝╠═╣║║║ FUZZY PANDA UPDATE
 ╩ ╩ ╩ ╩  ╩ ╩╚╩╝ (TOTAL RECODE)
--------------------------------------------''')
	
	start_time = time.time()

	## Brain to RAM -------------------------------
	try:
		with open('./brain.json') as data_file:
			bootatpaw.braindata = json.load(data_file)
			bootatpaw.filesize = getSize(data_file)
	except Exception as e:
		bootatpaw.braindata = {'hi':['hello'],'bye':['goodbye']}
		bootatpaw.filesize = 33
		print(e)
	## --------------------------------------------

	## Lobe calculator -------------------------------------------------
	bootatpaw.brainlobes = (len(bootatpaw.braindata.keys()))
	bootatpaw.brainlobes = str((bootatpaw.brainlobes / 30000)).split(".")[0]
	bootatpaw.lobeweight = len(bootatpaw.braindata.keys())/int(bootatpaw.brainlobes)
	bootatpaw.total_lobe_weight = int(str(bootatpaw.lobeweight).split(".")[0])
	bootatpaw.bigbrain = bootatpaw.braindata.keys()
	bootatpaw.lobeweight = 2 ## This is the number of lobes in brain.
	## less lobes = slower but more accurate
	## more lobes = faster but less accurate
	bootatpaw.brain_in_lobes = lobe_slice(list(bootatpaw.bigbrain), bootatpaw.lobeweight)
	## -----------------------------------------------------------------

	## Synapse Calculator -------
	synapses = 0
	for x in bootatpaw.braindata.keys():
		for y in bootatpaw.braindata[x]:
			synapses+=1
	## --------------------------

	table = [["Current Brain Size",str(round(((bootatpaw.filesize/1024)/1024),2))+" MB"],
			["Neurons",str(len(bootatpaw.braindata.keys()))],
			["Synapses",str(synapses)],
			["Number of Lobes", str(len(bootatpaw.brain_in_lobes))],
			["Neurons per Lobe", str(len(bootatpaw.brain_in_lobes[1]))]]
			
	print(" -> Brain to RAM @ %s seconds" % round((time.time() - start_time),1))
	print(tabulate(table, tablefmt="github"))
	print("--------------------------------------------\n")
	bootatpaw.total_learned_messages = 0 # this will be used to force a brain to RAM update
	bootatpaw.total_learn_flood = 100 # if flood is reached, learnthatshit()
	bootatpaw.botname = "atpaw"
	bootatpaw.oldneurons = str(len(bootatpaw.braindata.keys()))
	bootatpaw.oldsinapses = str(synapses)
	reboottimes.rtimes += 1

def learnthatshit(braindata):
	j = json.dumps(braindata, indent=4)
	f = open('brain.json', 'w')
	print(j, end="", file=f)
	f.close()
	bootatpaw()


## -------------- USER SETTINGS --------------- ##
try:
	with open('./settings.json') as data_file:
		usrsettings = json.load(data_file)
except:
		usrsettings = {}
		j = json.dumps(usrsettings, indent=4)
		f = open('./settings.json', 'w')
		print(j, end="", file=f)
		f.close()	

def save_settings(usrsettings):
	j = json.dumps(usrsettings, indent=4)
	f = open('./settings.json', 'w')
	print(j, end="", file=f)
	f.close()
	bootatpaw()
## ------------------------------------------- ##

def handle(msg):
	content_type, chat_type, chat_id = monkeytelepot.glance(msg)
	contentstr = (content_type +" | "+ str(chat_id))
	
	passtotalk = False
	admins = [580621896]
	botusername = "atnetbot"
	banlist = ["574901745"]
	
	if msg['from']['id'] in banlist:
		bot.sendMessage(chat_id, "You have been banned from using Atpaw.")
	else:
		
		## Private 
		if chat_type != "private":
			try:
				if chat_id not in reboottimes.public_id_list:
					reboottimes.public_id_list.append(chat_id)
			except:
				...

		## Check for replies and learn text
		try:
			if msg['reply_to_message']!= None and chat_type != "private":
				
				if content_type == 'sticker':
					lastkey = msg['sticker']['emoji']
				elif content_type == 'text':
					lastkey = msg['text']
				
				try:
					print("---> REPLIED EMOJI: ",msg['reply_to_message']['sticker']['emoji'])
					msg_primary = msg['reply_to_message']['sticker']['emoji']
				except:
					msg_primary = msg['reply_to_message']['text'].lower()
				
				try:
					if msg_primary!="/share":
						bootatpaw.total_learned_messages += 1
						## msg_primary is primary key msg['reply_to_message']
						## user_text   is append msg['text']
						msg_primary = msg_primary.replace("@atnetbot", "").replace("@atnetbot", "")
						msg_primary = msg_primary.replace(", ", "").replace(". ", "").replace("?", "").replace("!", "")
						msg_primary = msg_primary.replace("<", "").replace(">", "").replace("@", "")
						msg_primary = msg_primary.replace(" ", " ").replace(".", "")
						msg_primary = msg_primary.replace(" ", " ")
						firstkey = msg_primary
						if firstkey not in bootatpaw.braindata.keys():
							bootatpaw.braindata[firstkey] = [lastkey]
						elif firstkey in bootatpaw.braindata:
							bootatpaw.braindata[firstkey].append(lastkey)
						synapses = 0
						for x in bootatpaw.braindata.keys():
							for y in bootatpaw.braindata[x]:
								synapses+=1
						print("!!! N: "+str(len(bootatpaw.braindata.keys()))+" | S: "+str(synapses)+" | FLOOD: "+str(bootatpaw.total_learned_messages)+"/"+str(bootatpaw.total_learn_flood)+" !!!")
						if bootatpaw.total_learned_messages>=bootatpaw.total_learn_flood:
							print("!!! WRITING DATA TO BRAIN AND RECALCULATING !!!")
							total_learned_messages = 0
							learnthatshit(bootatpaw.braindata)
				except:
					...
		except Exception as e:
			#print("---> ERROR:",e)
			...
		
		## Check for messages and reply
		try:
			if msg['reply_to_message']['from']['username'].lower() == botusername: 
				passtotalk = True
				botinput = msg['text']
		except:
			passtotalk = False
		
		## passtotalk here
		if content_type != 'text':
			try:
				if msg['reply_to_message']['from']['username'].lower() == botusername:
					try:
						botinput = msg['sticker']['emoji']
						print("---> STICKER DECODE: "+str(botinput))
					except:
						botinput = ""
					passtotalk = True
				
				try:
					if botname in msg['caption'].lower():
						botinput = msg['caption']
						passtotalk = True
				except:
					...
			except Exception as e:
				#print(e)
				passtotalk = False
		
		elif content_type == 'text':
			if bootatpaw.botname in msg['text'].lower(): 
				botinput = msg['text']
				passtotalk = True

		if chat_type == "private":
			passtotalk = True
			try:
				botinput = msg['text']
			except:
				try:
					botinput = msg['caption']
				except:
					botinput = ""
		
		## general commands go here
		if content_type == "text": # General commands
			
			if "/settings_set_" in msg['text']:
				## pull from usrsettings (settings are group specific)
				if chat_type!="private":
					checkstatus = bot.getChatAdministrators(chat_id)
					userlist = []
					for x in checkstatus:
						userlist.append(x['user']['id'])
					if msg['from']['id'] in userlist:
						bot.sendMessage(chat_id, "You have group admin privs.")
					else:
						bot.sendMessage(chat_id, "Insufficient group admin privs.")
			
			if msg['text'] == "/start":
				passtotalk = False
				disclaimmessage = '''
The creator of this bot 
is not responsible for anything that this bot (@atnetbot) says or does.
It is presented as is, and all content used by this bot is generated from the users it interacts with.
Please be considerate when adding the bot to chats, and when talking to the bot in PM.'''
				bot.sendMessage(chat_id, "Heyo, my name is Atpaw.\nAtpaw Current version: 3.0\nFeel free to add me in your group, I learn faster that way.\n\nDISCLAIMER!\n"+disclaimmessage,reply_to_message_id=msg['message_id'])
			
			## stats here		
			if msg['text'] == "/atpawstats":
				passtotalk = False
				lastboot = "%s"% round((time.time() - reboottimes.mainboot),1)
				apecheck = int(lastboot.split(".")[0])
				if apecheck >= 1200: rce = "True"
				else: rce = "False"
				bot.sendMessage(chat_id, "Some technical stats \n~~~~~~~~~~~~~~~\nTime Online: "+str(datetime.timedelta(seconds = int(lastboot.split(".")[0])))+"\n\n* I'm in about "+str(len(reboottimes.public_id_list))+" groups.\n* I spoke to "+str(len(reboottimes.private_id_list))+" users.\n\n* Random Chimp Event: "+rce+"\n\nRebooted: "+str(reboottimes.rtimes)+" time(s)",reply_to_message_id=msg['message_id'])
				
			if msg['text'] == '/share':
				passtotalk = False
				try:
					sharethis = msg['reply_to_message']['text']
					sharefilter = [ "Successfully shared to @atpawchannel!", 
									"Remember to reply to what you want me to share.\nOnly things I say can be shared, and to keep the atpaw channel sfw, I can't share stickers",
									"LEARN == FLOOD.",
									"Since my last bootup ~ ",
									"Atpaw Brain Status",
									"\n~~~~~~~~~~~~~~~",
									"/share"]
					guybrushthreepwoodquotes = ["I can’t help but feel I’ve been ripped off.\n*turns to face the fourth wall*\nI’m sure you're feeling something similar.",
												"How can you see without eyeballs?",
												"I see a diorama of the children of the world living in peace and freedom. No, wait. It can't be that. It's just too dark to make out what's in there.",
												"I can hold my breath for ten minutes!",
												"I had a feeling that in hell there would be mushrooms.",
												"How come you didn't just go with the chimps?",
												"Let me see the best ship you've got.",
												"Look behind you, a Three-Headed Monkey!",
												"I’m selling these fine leather jackets.",
												"I must have left it in my other pants.",
												"Never pay more than 20 bucks for a computer game.",
												"¡He dejado en libertad los prisioneros y ahora vengo por ti!",
												"hat do you know about lifting voodoo curses?"]
					
					if msg['reply_to_message']['from']['username'].lower() == "atnetbot":
						sharetochannel_one = False
						sharetochannel_two = False
						
						for x in sharefilter:
							if x in msg['reply_to_message']['text']:
								sharetochannel_one = False
								break
							else:
								sharetochannel_one = True
								
						for x in guybrushthreepwoodquotes:
							if x in msg['reply_to_message']['text']:
								sharetochannel_two = False
								break
							else:
								sharetochannel_two = True
								
						if sharetochannel_one is True and sharetochannel_two is True: 
							bot.forwardMessage("@atpawchannel", from_chat_id=chat_id,
											   message_id=msg['reply_to_message']['message_id'])
							bot.forwardMessage(-1001343826263, from_chat_id=chat_id,
											   message_id=msg['reply_to_message']['message_id'])
							bot.sendMessage(chat_id, "Successfully shared to @atpawchannel!",
											reply_to_message_id=msg['message_id'])
						else:
							bot.sendMessage(chat_id, random.choice(guybrushthreepwoodquotes), reply_to_message_id=msg['message_id'])
				except Exception as e:
					bot.sendMessage(chat_id,
									"Remember to reply to what you want me to share.\nOnly things I say can be shared, and to keep the atpaw channel sfw, I can't share stickers.\n\nError: "+str(e),
									reply_to_message_id=msg['message_id'])
			
			if msg['text'] == '/brain':
				synapses = 0
				passtotalk = False
				for x in bootatpaw.braindata.keys():
					for y in bootatpaw.braindata[x]:
						synapses+=1
				brainmsg = "Atpaw Brain Status"
				brainmsg += "\n~~~~~~~~~~~~~~~"
				try:
					brainmsg += "\n"+str(cpuinfo.get_cpu_info()['brand'])
				except:
					brainmsg += "\nCPU: unidentified."
				try:
					brainmsg += "\nMemory: "+str(size(psutil.virtual_memory()[0], system=si))+"B"
				except:
					brainmsg += "\nMemory: unidentified"
				brainmsg += "\n~~~~~~~~~~~~~~~"
				brainmsg += "\nBRAIN SPECS"
				brainmsg += "\nPhysical Size: "+str(round(((bootatpaw.filesize/1024)/1024),2))+" MB"
				brainmsg += "\nNeurons:  "+bootatpaw.oldneurons+" | SH: "+str(len(bootatpaw.braindata.keys()))
				brainmsg += "\nSynapses: "+bootatpaw.oldsinapses+" | SH: "+str(synapses)
				brainmsg += "\n~~~~~~~~~~~~~~~"
				brainmsg += "\nMEMORY FLOOD: "+str(bootatpaw.total_learned_messages)+"."+str(bootatpaw.total_learn_flood)
				bot.sendMessage(chat_id, brainmsg,
								reply_to_message_id=msg['message_id'])
		
		## Admin commands here
		if msg['from']['id'] in admins and content_type == 'text':
			if msg['text'] == "/commands":
				syscommands  = "Atpaw V3 System Commands\n"
				syscommands += "~~~~~~~~~~~~~~~\n"
				syscommands += "/update_brain - (N) (S) update\n"
				syscommands += "/start - Start message\n"
				syscommands += "/share - Share message\n"
				syscommands += "/generate_sentence - Not implemented"
				bot.sendMessage(chat_id, syscommands, reply_to_message_id=msg['message_id'])
			if msg['text'] == '/update_brain':
				bootatpaw.total_learned_messages = bootatpaw.total_learn_flood
				synapses = 0
				for x in bootatpaw.braindata.keys():
					for y in bootatpaw.braindata[x]:
						synapses+=1
				bot.sendMessage(chat_id, "LEARN == FLOOD. Reboot Imminent.\n(N): "+bootatpaw.oldneurons+" --> "+ str(len(bootatpaw.braindata.keys())) +"\n(S): "+bootatpaw.oldsinapses+" --> "+str(synapses))

		## Random chimp event and timer
		lastboot = "%s"% round((time.time() - reboottimes.mainboot),1)
		if int(lastboot.split(".")[0])>=1200:
			spawn_random_chimp_event = randint(1,500)
		else:
			spawn_random_chimp_event = 1
		
		if content_type == "text":
			if botusername in msg['text'].lower():
				spawn_random_chimp_event = 500
		
		if spawn_random_chimp_event>=499:
			passtotalk = True
			print("---> RCE or @ in "+str(msg['from']['id'])+" | RCE: "+str(spawn_random_chimp_event))
			try:
				botinput = msg['sticker']['emoji']
				print("---> STICKER DECODE: "+str(botinput))
			except Exception as e:
				try:
					print("---> trying text...")
					botinput = msg['text']	
				except Exception as e:
					print(e)
					...
					
		if passtotalk == True:
			start_time = time.time()
			uselobe = randint(0, bootatpaw.lobeweight-1)
			botoutput = process.extractOne(botinput, bootatpaw.brain_in_lobes[uselobe])
			try:
				print(contentstr+" | DECODING @ LOBE "+str(uselobe)+" | CERTAINTY: "+str(botoutput[-1])+"%")
			except Exception as e:
				print("<<<",e,">>>")
			decodertries = 0
			while botoutput[-1] <= 80: ## 80% certainty or more, else no dice
				print(contentstr+" | DECODING IN LOBE "+str(uselobe)+" | "+str(botoutput[-1])+"%")
				uselobe = randint(0, bootatpaw.lobeweight-1)
				botoutput = process.extractOne(botinput, bootatpaw.brain_in_lobes[uselobe])
				decodertries += 1
				if decodertries == 5:
					break

			extkey = botoutput[0]			
			finaloutput = None
			brewtries = 0
			
			if botoutput[-1] == 0.0:
				finaloutput = random.choice(["oh, ok uwu", "o ok",
									  "no u", "what",
									  "ok then", "wh-",
									  "stfu, lmao", "sigh",
									  "why tho"])
			
			while finaloutput is None:
				try:
					text_model = markovify.Text(bootatpaw.braindata[extkey], state_size=randint(2,4))
					finaloutput = (text_model.make_sentence())
					markoved = "ST_GEN"
					brewtries += 1
					if brewtries == 5:
						finaloutput = random.choice(bootatpaw.braindata[extkey])
						markoved = "ST_LEN"
						break
				except Exception as e:
					#print(e)
					markoved = "ST_LEN"
					finaloutput = random.choice(bootatpaw.braindata[extkey])
				
			#print(finaloutput)
			## Last chance to filter shit goes here
			
			repprob = randint(1, 10)
			if repprob == 1:
				finaloutput = finaloutput.replace("hello", "hewwo").replace("Hello", "Hewwo")
				finaloutput = finaloutput.replace("is ", "ish ")
				finaloutput = finaloutput.replace("He's ", "me ish ").replace("He's ", "me ish ")
				finaloutput = finaloutput.replace("you ", "chu ").replace("You ", "Chu ")
				finaloutput = finaloutput.replace(" I ", " me ")
				finaloutput = finaloutput.replace("I ", "me ")
			if repprob == 2:
				finaloutput = finaloutput.replace("He'll ", "I'll ").replace("he'll ", "I'll ")
				finaloutput = finaloutput.replace("hello", "hewwo").replace("Hello", "Hewwo")
				finaloutput = finaloutput.replace("is ", "ish ")
				finaloutput = finaloutput.replace("He's ", "me ish ").replace("He's ", "me ish ")
				finaloutput = finaloutput.replace("you ", "chu ").replace("You ", "Chu ")
				finaloutput = finaloutput.replace(" I ", " me ")
				finaloutput = finaloutput.replace("I ", "me ")

			if repprob == 3:
				finaloutput = finaloutput.replace("He'll ", "I'll ").replace("he'll ", "I'll ")

			if repprob >= 4:
				finaloutput = finaloutput
			
			finaloutput = finaloutput.replace("@","")
			try:
				print("<<< RESPONSE TIME: %s seconds" % round((time.time() - start_time),3), "| MODEL:",markoved,"| OUTPUT FILTER:",repprob,">>>")
				bot.sendMessage(chat_id, finaloutput, reply_to_message_id=msg['message_id'])
			except:
				print("<< Critical decode error, sending dud. >>")
				finaloutput = random.choice(["oh, ok uwu", "o ok",
											"no u", "what",
											"ok then", "wh-",
											"stfu, lmao", "sigh",
											"why tho"])
				bot.sendMessage(chat_id, finaloutput, reply_to_message_id=msg['message_id'])
				
			if msg['from']['id'] not in reboottimes.private_id_list:
				reboottimes.private_id_list.append(msg['from']['id'])
				
			## check if bot promised a DM/PM
			## check for word "not" and "them"
			
			if "not" not in finaloutput and "them" not in finaloutput:
				## now check for DM/PM
				dmlist = ['pm ','dm ','pm me', 'dm me', 'check pms', 'check dms']
				quirkytext = ['Hai', 'Henlo', 'Woof', 'Mew', '*fox noises*']
				for x in dmlist:
					if x in finaloutput.lower():
						try:
							print("<--- ATTEMPTING TO START PM WITH: "+str(msg['from']['id']))
							bot.sendMessage(msg['from']['id'], random.choice(quirkytext))
						except:
							...
			
		elif passtotalk == False:
			...

DEBUGTOKEN = "" 
TOKEN = ""
bootatpaw()
bot = monkeytelepot.Bot(TOKEN)
MessageLoop(bot, handle).run_as_thread()
print("... Systems Online")

# Keep the program running.
while 1:
	time.sleep(10)