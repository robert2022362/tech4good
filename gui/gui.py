# Import modules
from tkinter import *
import tkinter.font as font
import tkinter.filedialog as filedialog
import tkinter.messagebox as messagebox
from audio_recording import *
import os

# Root window
root = Tk()
root.geometry("600x600")
root.title("种子计划")

# Define two different font sizes
size_1 = font.Font(family="Lucida Grande", size=20)
size_2 = font.Font(family="Lucida Grande", size=16)

# Main frame
class Main:

	# Define constructor
	def __init__(self, master):

		self.master = master

		# Create main frame
		self.frame = Frame(master)
		self.frame.pack()

		# Create title
		self.title = Label(self.frame, text="普通话评测", font=size_1)
		self.title.grid(row=0, pady=20)

		self.description2 = Label(self.frame, text="静夜思\n李白\n床前明月光，\n疑似地上霜。\n举头望明月，\n低头思故乡。", font=size_2, wraplength=500)
		self.description2.grid(row=1, pady=50)

		# Create description
		self.description1 = Label(self.frame, text="请按Start recording开始录音，并在10秒以内朗读以上段落", font=size_2, wraplength=300)
		self.description1.grid(row=2)

		self.start_recording = Button(self.frame, text="Start recording", padx=20, pady=10, command=start)
		self.start_recording.grid(row=3)

		self.check_accuracy = Button(self.frame, text="Check result", padx=20, pady=10, command=self.check)
		self.check_accuracy.grid(row=4)
	
	def check(self):
		
		if os.stat('accuracy.txt').st_size != 0:
			with open('accuracy.txt', 'r') as f:
				accuracy = float(f.readline())
				if accuracy > 80:
					message = "恭喜你！你的普通话很标准"
				elif accuracy > 60:
					message = "你的普通话不错，继续努力哦！"
				else:
					message = "你的普通话有待进步哦"
				messagebox.showinfo(title="Result", message=f"你的分数是{accuracy}!\n{message}")
			os.system("python empty_out.py")
			os.system("python empty_information.py")

		



# Create main frame
main = Main(root)

# Keep root window open
root.mainloop()
