from tkinter import *
from tkinter import messagebox

class editinfo(Frame):
    """ default init function """
    def __init__(self):
        super().__init__()
        self.master = root
        self.font = ("arial", 10)
        self.screenwidth = 925
        self.screenheight = 500
        self.screenx = 300
        self.screeny = 100
        self.master.geometry("{}x{}+{}+{}".format(self.screenwidth, self.screenheight, self.screenx, self.screeny))
        self.master.resizable(False, False)
        self.apptitle = "Grader"
        self.master.title(self.apptitle)
        
        p1 = PhotoImage(file="log-in.png")
        self.master.iconphoto(False, p1)
        
        # Load background image
        self.background_image = PhotoImage(file="background.png")
        self.background_label = Label(image=self.background_image)
        self.background_label.place(x=-10, y=0)

        self.lines = []
        with open("setup.txt","r") as f:
            for i in range(9):
                self.line=f.readline().strip()
                self.lines.append(self.line)

        frame=Frame(width=350,height=400,bg="white")
        frame.place(x=460,y=50)

        headinglbl=Label(frame,text="Edit Info",font=("arial",14),bg="white",fg="#f6be00")
        headinglbl.place(x=140,y=20)

        self.userfulllbl=Label(frame,text="User Full Name",bg="white", font=self.font)
        self.userfulllbl.place(x=40,y=70)
        self.userfulltxt=Entry(frame,bg="white",font=self.font,width=25)
        self.userfulltxt.insert(0,self.lines[0])
        self.userfulltxt.place(x=140,y=70)
        self.userfulltxt.focus()

        self.coursenamelbl=Label(frame,text="Course Name",bg="white", font=self.font)
        self.coursenamelbl.place(x=51,y=92)
        self.coursenametxt=Entry(frame,bg="white",font=self.font, width=25)
        self.coursenametxt.insert(0,self.lines[1])
        self.coursenametxt.place(x=140,y=92)

        self.coursecodelbl=Label(frame,text="Course Code",bg="white", font=self.font)
        self.coursecodelbl.place(x=54,y=114)
        self.coursecodetxt=Entry(frame,bg="white",font=self.font, width=25)
        self.coursecodetxt.insert(0,self.lines[2])
        self.coursecodetxt.place(x=140,y=114)

        self.category1_lbl=Label(frame,text="Category 1",bg="white", font=self.font)
        self.category1_lbl.place(x=65,y=136)
        self.category1_txt=Entry(frame,bg="white",font=self.font, width=25)
        self.category1_txt.insert(0,self.lines[3])
        self.category1_txt.place(x=140,y=136)

        self.category1val_lbl=Label(frame,text="Category 1 %",bg="white", font=self.font)
        self.category1val_lbl.place(x=48,y=158)
        self.category1val_txt=Entry(frame,bg="white",font=self.font, width=25)
        self.category1val_txt.insert(0,self.lines[4])
        self.category1val_txt.place(x=140,y=158)

        self.category2_lbl=Label(frame,text="Category 2",bg="white", font=self.font)
        self.category2_lbl.place(x=65,y=180)
        self.category2_txt=Entry(frame,bg="white",font=self.font, width=25)
        self.category2_txt.insert(0,self.lines[5])
        self.category2_txt.place(x=140,y=180)

        self.category2val_lbl=Label(frame,text="Category 2 %",bg="white", font=self.font)
        self.category2val_lbl.place(x=48,y=202)
        self.category2val_txt=Entry(frame,bg="white",font=self.font, width=25)
        self.category2val_txt.insert(0,self.lines[6])
        self.category2val_txt.place(x=140,y=202)

        self.usernamelbl=Label(frame,text="Username",bg="white", font=self.font)
        self.usernamelbl.place(x=68,y=224)
        self.usernametxt=Entry(frame,bg="white",font=self.font,width=25)
        self.usernametxt.insert(0,self.lines[7])
        self.usernametxt.place(x=140,y=224)

        self.passwordlbl=Label(frame,text="Password",bg="white", font=self.font)
        self.passwordlbl.place(x=70,y=246)
        self.passwordtxt=Entry(frame,bg="white",font=self.font, width=25,show="*")
        self.passwordtxt.insert(0,self.lines[8])
        self.passwordtxt.place(x=140,y=246)

        self.confirmpasswordlbl=Label(frame,text="Confirm Password",bg="white", font=self.font)
        self.confirmpasswordlbl.place(x=22,y=268)
        self.confirmpasswordtxt=Entry(frame,bg="white",font=self.font, width=25,show="*")
        self.confirmpasswordtxt.place(x=140,y=268)

        self.savebtn=Button(frame,text="Save",width=10,pady=7, bg="#f6be00",fg="black",border=0,command=self.save)
        self.savebtn.place(x=65,y=320)

        self.menubtn=Button(frame,text="Return to Main Menu",width=20,pady=7,bg="#f6be00",fg="black",border=0,command=self.callmainpage)
        self.menubtn.place(x=145,y=320)

    """ validates and saves new user info """
    def save(self):
        d = {"User Full Name":self.userfulltxt.get().strip(),
            "Course Name":self.coursenametxt.get().strip(),
            "Course Code":self.coursecodetxt.get().strip(),
            "Category 1":self.category1_txt.get().strip(),
            "Category 1 %":self.category1val_txt.get().strip(),
            "Category 2":self.category2_txt.get().strip(),
            "Category 2 %":self.category2val_txt.get().strip(),
            "Username":self.usernametxt.get().strip(),
            "Password":self.passwordtxt.get().strip(),
            }
                
        # Validate percentages
        try:
            perc1 = float(d["Category 1 %"])
            perc2 = float(d["Category 2 %"])
                    
            if perc1 + perc2 != 100:
                messagebox.showerror("Error","Percentages must add up to 100")
                self.category1val_txt.focus_set()
                return
        except:
            messagebox.showerror("Error","The % values should be a float")
            self.category1val_txt.focus_set()
            return

        # Validate password
        password = d["Password"]
        confirm_password = self.confirmpasswordtxt.get()
        if password != confirm_password:
            messagebox.showerror("Error", "Passwords do not match")
            self.passwordtxt.focus_set()
            return

        for i in d:
            if d[i]=="":
                messagebox.showerror("Error","Please fill up all the fields.")
                self.userfulltxt.focus_set()
                return

        # Save data
        with open("setup.txt", "w") as file:
            for j in d:
                file.write(f"{d[j]}\n")
                    
        messagebox.showinfo("Success", "Data saved successfully")
        self.callmainpage()

    """ calls main page """
    def callmainpage(self):
        root.destroy()
        from main_page import root_main
        main_page_instance = root_main()
   
def root_editinfo():
    global root
    root = Tk()
    app = editinfo()
    app.mainloop

#root_editinfo()
