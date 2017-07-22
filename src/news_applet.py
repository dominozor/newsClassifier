from Tkinter import *
import ttk
from PIL import ImageTk, Image
from textblob.classifiers import NaiveBayesClassifier
from textblob import TextBlob
import pickle
import sys
import os
import re
import subprocess
stopwords=[]
test=[]
width=40
height=300


class Window:       
	def __init__(self, master):     
		self.trainModelPath=""
		self.inpDirName=""
		self.selectedOption=1
		self.master=master
		trainedFile=Label(root, text="Trained Model File Path").grid(row=1, column=0)
		self.bar=Entry(master,width=width)
		self.bar.grid(row=1, column=1)
		inputFile=Label(root, text="Input Folder Path").grid(row=2, column=0)
		self.bar2=Entry(master,width=width)
		self.bar2.grid(row=2, column=1)  
		
		#Radio Button
		self.var = IntVar()
		self.R1 = Radiobutton(root, text="Classify Text", variable=self.var, value=1,
                  command=self.sel)
		self.R1.grid(row=3, column=4,sticky=W)
		self.R2 = Radiobutton(root, text="Test From Test Folder", variable=self.var, value=2,
                  command=self.sel)
		self.R2.grid(row=2, column=4,sticky=W)

		#Result
		resultLabel=Label(root, text="Result:").grid(row=7, column=0,sticky=E)
		self.result=Label(root,text="NULL")
		self.result.grid(row=7, column=1,sticky=W)

		#Classify Option
		
		classifyInpText=Label(root, text="Input Text").grid(row=3, column=0)
		self.bar3=Entry(master,width=width)
		self.bar3.grid(row=3,column=1)

		#Pipe Action

		self.numberOfTestInputQuery='find ./test -type f -name "*.txt" | wc -l'
		self.numberOfInput=int(subprocess.Popen(self.numberOfTestInputQuery, shell=True, stdout=subprocess.PIPE).stdout.read())

		#Progress Bar
		
		self.currentPrg=0
		progressText=Label(root, text="Progress").grid(row=5, column=0)
		self.progress = ttk.Progressbar(master, orient="horizontal",
                                        length=width*10, mode="determinate")
		self.progress.grid(row=6,column=0,columnspan=4)
		self.progress["maximum"]=self.numberOfInput
		#Image
		image_pil=Image.open("news.jpg").resize((400, 300))
		img = ImageTk.PhotoImage(image_pil)
		
		panel = Label(master, image = img)
		panel.grid(row=4, column=0,columnspan=2)
		

		#Buttons  
		y=7
		self.cbutton= Button(root, text="OK", command=self.process_csv)
		y+=1
		self.cbutton.grid(row=10, column=4, sticky =W+E)
		self.trainbutton= Button(root, text="Browse", command=self.browseTrain)
		self.trainbutton.grid(row=1, column=3)
		self.bbutton= Button(root, text="Browse", command=self.browseInput)
		self.bbutton.grid(row=2, column=3)
		self.qbutton=Button(root,text="QUIT",command=self.quit)
		self.qbutton.grid(row=19, column=4, sticky =W+E)
		master.mainloop()
	def sel(self):
		self.selectedOption=self.var.get()
	
	def browseTrain(self):
		from tkFileDialog import askopenfilename

		Tk().withdraw() 
		self.trainModelPath = askopenfilename()
		self.bar.insert(END, self.trainModelPath)
		self.bar.grid(row=1, column=1) 
		self.master.mainloop()
	def browseInput(self):
		from tkFileDialog import askopenfilename
		from tkFileDialog import askdirectory

		Tk().withdraw() 
		self.inpDirName = askdirectory()+'/'
		self.bar2.insert(END, self.inpDirName)
		self.bar2.grid(row=2, column=1) 
		self.master.mainloop()
	
	def classify(self):
		example=self.bar3.get()
		
		if self.trainModelPath and example:
			self.progress["value"]=0
			self.master.update_idletasks()
			trained_model_file = open(self.trainModelPath, 'rb')
			cl = pickle.load(trained_model_file)
			trained_model_file.close()

			with open("stopwords", 'r') as infile:
				data = infile.read().replace("\n","")

			stopwords=data.split(",")

			example= example.replace("\n","").lower()

			for stopword in stopwords:
				regex=r'\b'+re.escape(stopword)+r'\b'
				lowercase = re.compile(regex)
				example = lowercase.sub(r'', example)
				example=re.sub(r'[^\x00-\x7F]+','', example)
				example=re.sub(r'[\x21-\x2F]+','', example)
				example=re.sub(r'[\x3A-\x40]+','', example)
				example=" ".join(example.split())
			res=cl.classify(example).upper()
			
			self.result.config(text=res)
			

	def folderClassify(self):
		if self.trainModelPath and self.inpDirName:
			self.progress["value"]=0
			self.master.update_idletasks()
			self.numberOfInput=int(subprocess.Popen(self.numberOfTestInputQuery, shell=True, stdout=subprocess.PIPE).stdout.read())
			trained_model_file = open(self.trainModelPath, 'rb')
			cl = pickle.load(trained_model_file)
			trained_model_file.close()

			with open("stopwords", 'r') as infile:
				data = infile.read().replace("\n","")
			self.progress["value"]=10
			self.master.update_idletasks()
			stopwords=data.split(",")

			folders = [folder for folder in os.listdir(self.inpDirName)]
			progs=10
			
			for category in folders:
				print category
				
				
				os.chdir(self.inpDirName + category)
				for files in os.listdir('.'):
					with open(files, 'r') as my_file:
						data = my_file.read().lower()
						for stopword in stopwords:
							regex=r'\b'+re.escape(stopword)+r'\b'
							lowercase = re.compile(regex)
							data = lowercase.sub(r'', data)
						data=re.sub(r'[^\x00-\x7F]+','', data)
						data=re.sub(r'[\x21-\x2F]+','', data)
						data=re.sub(r'[\x3A-\x40]+','', data)
						data=" ".join(data.split())
						test.append((data, category))
						progs+=0.5
						self.progress["value"]=progs
						self.master.update_idletasks()
				os.chdir('../..')
			self.progress["value"]=self.numberOfInput
			res=cl.accuracy(test)
			self.result.config(text=res)
			

	def process_csv(self):

		if(self.selectedOption==1):
			self.classify()
		else:
			self.folderClassify()

		

	def quit(self):
		sys.exit()

root = Tk()
root.wm_title("News Classifier")
root.minsize(width,height)
window=Window(root)
root.mainloop()  
