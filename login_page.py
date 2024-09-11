from tkinter import *
from tkinter import messagebox

class App(Tk):
    """ setup innit function """
    def __init__(self):
        super().__init__()
        self.passwordcharacter="*"
        self.font=("arial",10)
        self.screenwidth=925
        self.screenheight=500
        self.screenx=300
        self.screeny=100
        self.screenname=""
        self.geometry("{}x{}+{}+{}".format(self.screenwidth, self.screenheight, self.screenx,self.screeny))
        self.apptitle="Grader"
        self.title(self.apptitle)

        self.configure(bg="white")
        self.resizable(False,False)
        
        p1=PhotoImage(file="log-in.png")
        self.iconphoto(False,p1)
        
        self.loginpagetitle="Log In Form"
        self.signinpagetitle="Sign In Form"
        self.signuppagetitle="Sign Up Form"
        self.currentpage=""
        self.loginpage()
        self.protocol("WM_DELETE_WINDOW",self.on_closing)
        self.mainloop()

    """ function on closing window """
    def on_closing(self):
        if self.screenname=="login":
            self.destroy()
        else:
            self.loginpage()

    """ login in page setup """
    def loginpage(self):
        def drawseparator(f,w,h,xcoordinate,ycoordinate):
            frame=Frame(f,width=w,height=h,bg="black")
            frame.place(x=xcoordinate,y=ycoordinate)
            
        self.screenname="login"
        self.currentpage="loginpage"
        self.loginframe=Frame(width=self.screenwidth,height=self.screenheight,bg="white")
        self.loginframe.place(x=0,y=0)
        self.title=self.loginpagetitle

        bgimage=PhotoImage(file="background.png")
        bglbl=Label(self.loginframe,image=bgimage,bg="white")
        bglbl.image=bgimage
        bglbl.place(x=-10,y=0)

        frame=Frame(self.loginframe,width=350,height=400,bg="white")
        frame.place(x=460,y=50)

        headinglbl=Label(frame,text="Log In",font=("arial",15),bg="white",fg="#f6be00")
        headinglbl.place(x=140,y=20)

        user=Entry(frame,width=25,fg="lightgray",border=0,bg="white",font=self.font)
        user.place(x=30,y=80)
        drawseparator(frame,295,2,25,107)
        user.insert(0,"User Name")

        password=Entry(frame,width=25,fg="lightgray",border=0,bg="white",font=self.font)
        password.place(x=30,y=150)
        password.insert(0,"Password")
        drawseparator(frame,295,2,25,177)

        """ changes font colour on user activity """
        def user_on_enter(e):
            if user.cget("fg")=="lightgray":
                user.delete(0,END)
            else:
                user.config(fg="gray")
        def user_on_leave(e):
            s=user.get().strip()
            if s=="":
                user.insert(0,"User Name")
                user.config(fg="lightgray")
            else:
                user.config(fg="gray")
 

        user.bind("<FocusIn>",user_on_enter)
        user.bind("<FocusOut>",user_on_leave)

        
        """ changes password font colour on user activity """
        def password_on_enter(e):
            if password.cget("fg")=="lightgray":
                password.delete(0,END)
                password.config(show=self.passwordcharacter)
            else:
                password.config(fg="gray")
        def password_on_leave(e):
            s=password.get().strip()
            if s=="":
                password.insert(0,"Password")
                password.config(fg="lightgray")
                password.config(show="")
            else:
                password.config(fg="gray")
                password.config(show=self.passwordcharacter)

        password.bind("<FocusIn>",password_on_enter)
        password.bind("<FocusOut>",password_on_leave)
        
        """ calls main page after login """
        def callmainpage(self):
            from main_page import root_main
            main_page_instance = root_main()

            
        """ runs when signin button is pressed """
        def signin():
            userid=user.get().strip()
            passid=password.get().strip()

            try:
                with open("setup.txt","r") as f:
                    lines=f.readlines()
                    usern=lines[7].strip()
                    passw=lines[8].strip()
                                
                if userid==usern and passid==passw:
                    messagebox.showinfo("Successful","Log in Successful")
                    self.on_closing()
                    callmainpage(self)
                                
                else:
                    messagebox.showerror("Error","Log in information doesn't match")

            except:
                messagebox.showerror("Error","Setup file not found.\nPlease Sign Up.")

                
        """ sign up page screen """
        def signuppage():
            def signup():
                d = {"User Full Name":userfulltxt.get().strip(),
                     "Course Name":coursenametxt.get().strip(),
                     "Course Code":coursecodetxt.get().strip(),
                     "Category 1":category1_txt.get().strip(),
                     "Category 1 %":category1val_txt.get().strip(),
                     "Category 2":category2_txt.get().strip(),
                     "Category 2 %":category2val_txt.get().strip(),
                     "Username":usernametxt.get().strip(),
                     "Password":passwordtxt.get().strip(),
                     }
                
                # Validate percentages
                try:
                    perc1 = float(d["Category 1 %"])
                    perc2 = float(d["Category 2 %"])
                    
                    if perc1 + perc2 != 100:
                        messagebox.showerror("Error","Percentages must add up to 100")
                        category1val_txt.focus_set()
                        return
                except:
                    messagebox.showerror("Error","The % values should be a float")
                    category1val_txt.focus_set()
                    return

                # Validate password
                password = d["Password"]
                confirm_password = confirmpasswordtxt.get()
                if password != confirm_password:
                    messagebox.showerror("Error", "Passwords do not match")
                    passwordtxt.focus_set()
                    return

                for i in d:
                    if d[i]=="":
                        messagebox.showerror("Error","Please fill up all the fields.")
                        userfulltxt.focus_set()
                        return
                        
                # Save data
                with open("setup.txt", "w") as file:
                    for j in d:
                        file.write(f"{d[j]}\n")
                    
                messagebox.showinfo("Success", "Data saved successfully")
                self.screenname="login"
                self.signupframe.destroy()

                
            self.currentpage="signuppage"
            self.screenname="Signup"
            self.signupframe=Frame(width=self.screenwidth, height=self.screenheight,bg="white")
            self.signupframe.place(x=0,y=0)
           
            bgimage=PhotoImage(file="background.png")
            bglbl=Label(self.signupframe,image=bgimage,bg="white")
            bglbl.image=bgimage
            bglbl.place(x=-10,y=0)

            frame=Frame(self.signupframe,width=350,height=400,bg="white")
            frame.place(x=460,y=50)

            headinglbl=Label(frame,text="Sign Up",font=("arial",15),bg="white",fg="#f6be00")
            headinglbl.place(x=140,y=20)

            userfulllbl=Label(frame,text="User Full Name",bg="white", font=self.font)
            userfulllbl.place(x=40,y=70)
            userfulltxt=Entry(frame,bg="white",font=self.font,width=25)
            userfulltxt.place(x=140,y=70)
            userfulltxt.focus()

            coursenamelbl=Label(frame,text="Course Name",bg="white", font=self.font)
            coursenamelbl.place(x=51,y=92)
            coursenametxt=Entry(frame,bg="white",font=self.font, width=25)
            coursenametxt.place(x=140,y=92)

            coursecodelbl=Label(frame,text="Course Code",bg="white", font=self.font)
            coursecodelbl.place(x=54,y=114)
            coursecodetxt=Entry(frame,bg="white",font=self.font, width=25)
            coursecodetxt.place(x=140,y=114)

            category1_lbl=Label(frame,text="Category 1",bg="white", font=self.font)
            category1_lbl.place(x=65,y=136)
            category1_txt=Entry(frame,bg="white",font=self.font, width=25)
            category1_txt.place(x=140,y=136)

            category1val_lbl=Label(frame,text="Category 1 %",bg="white", font=self.font)
            category1val_lbl.place(x=48,y=158)
            category1val_txt=Entry(frame,bg="white",font=self.font, width=25)
            category1val_txt.place(x=140,y=158)

            category2_lbl=Label(frame,text="Category 2",bg="white", font=self.font)
            category2_lbl.place(x=65,y=180)
            category2_txt=Entry(frame,bg="white",font=self.font, width=25)
            category2_txt.place(x=140,y=180)

            category2val_lbl=Label(frame,text="Category 2 %",bg="white", font=self.font)
            category2val_lbl.place(x=48,y=202)
            category2val_txt=Entry(frame,bg="white",font=self.font, width=25)
            category2val_txt.place(x=140,y=202)

            usernamelbl=Label(frame,text="Username",bg="white", font=self.font)
            usernamelbl.place(x=68,y=224)
            usernametxt=Entry(frame,bg="white",font=self.font,width=25)
            usernametxt.place(x=140,y=224)

            passwordlbl=Label(frame,text="Password",bg="white", font=self.font)
            passwordlbl.place(x=70,y=246)
            passwordtxt=Entry(frame,bg="white",font=self.font, width=25,show="*")
            passwordtxt.place(x=140,y=246)

            confirmpasswordlbl=Label(frame,text="Confirm Password",bg="white", font=self.font)
            confirmpasswordlbl.place(x=22,y=268)
            confirmpasswordtxt=Entry(frame,bg="white",font=self.font, width=25,show="*")
            confirmpasswordtxt.place(x=140,y=268)

            signupbtn=Button(frame,text="Sign Up",width=20,pady=7, bg="#f6be00",fg="black",border=0,command=signup)
            signupbtn.place(x=110,y=320)            

        signinbtn=Button(frame,text="Sign In",width=35,pady=7, bg="#f6be00",fg="black",border=0,command=signin)
        signinbtn.place(x=50,y=204)

        noaccountlbl=Label(frame,text="Don't have an account?",fg="black",bg="white",font=self.font)
        noaccountlbl.place(x=90,y=270)

        signupbtn=Button(frame,text="Sign Up",width=8,pady=7, bg="#f6be00",fg="black",border=0,command=signuppage,cursor="hand2")
        signupbtn.place(x=238,y=265) 


app=App()
