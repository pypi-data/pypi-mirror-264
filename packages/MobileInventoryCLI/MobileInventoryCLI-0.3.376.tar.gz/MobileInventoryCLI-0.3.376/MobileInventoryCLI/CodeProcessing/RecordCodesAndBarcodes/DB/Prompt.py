#Prompt.py
from colored import Fore,Style 

class Prompt:
	state=True
	status=None
	def __init__(self,func,ptext='do what',helpText='',data={}):
		while True:
			cmd=input(f'{Fore.light_yellow}{ptext}{Style.reset}:{Fore.light_green} ')
			print(Style.reset,end='')
			
			if cmd.lower() in ['q','quit']:
				exit('quit')
			elif cmd.lower() in ['b','back']:
				self.status=False
				return
			elif cmd.lower() in ['?','h','help']:
				print(helpText)
			else:
				#print(func)
				func(cmd,data)
				break

	def __init2__(self,func,ptext='do what',helpText='',data={}):
		while True:
			cmd=input(f'''{Fore.light_yellow}{ptext}{Style.reset}
{Fore.light_blue}Prompt CMDS:[{Fore.green}q{Style.reset}={Fore.green_yellow}quit{Style.reset}|{Fore.cyan}b{Style.reset}={Fore.blue}back{Style.reset}|{Fore.light_red}h{Style.reset}={Fore.red}help{Style.reset}{Fore.light_blue}]{Style.reset}
:{Fore.light_green} ''')
			print(Style.reset,end='')
			
			if cmd.lower() in ['q','quit']:
				exit('quit')
			elif cmd.lower() in ['b','back']:
				return
			elif cmd.lower() in ['h','help']:
				print(helpText)

			else:
				return func(cmd,data)	
	#since this will be used statically, no self is required 
	#example filter method
	def cmdfilter(text,data):
		print(text)

prefix_text=f'''{Fore.light_red}$code{Fore.light_blue} is the scanned text literal{Style.reset}
{Fore.light_magenta}{Style.underline}#code refers to:{Style.reset}
{Fore.grey_70}e.{Fore.light_red}$code{Fore.light_blue} == search EntryId{Style.reset}
{Fore.grey_70}B.{Fore.light_red}$code{Fore.light_blue} == search Barcode{Style.reset}
{Fore.grey_70}c.{Fore.light_red}$code{Fore.light_blue} == search Code{Style.reset}
{Fore.light_red}$code{Fore.light_blue} == search Code | Barcode{Style.reset}
'''
def prefix_filter(text,self):
	split=text.split(self.get('delim'))
	if len(split) == 2:
		prefix=split[0]
		code=split[-1]
		try:
			if prefix.lower() == 'c':
				self.get('c_do')(code)
			elif prefix == 'B':
				self.get('b_do')(code)
			elif prefix.lower() == 'e':
				self.get('e_do')(code)
		except Exception as e:
			print(e)
	else:
		self.get('do')(text)

if __name__ == "__main__":	
	Prompt(func=Prompt.cmdfilter,ptext='code|barcode',helpText='test help!',data={})
		

	