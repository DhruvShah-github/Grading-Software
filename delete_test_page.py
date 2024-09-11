from tkinter import *
from tkinter import messagebox
from tkinter import ttk
from tkinter import filedialog
import csv

class DeleteTestModule(Frame):
    """ default init function """
    def __init__(self, root):
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

        self.import_csv()

    """ imports required files for the code to run """
    def import_csv(self):
        messagebox.showinfo("Info","Please import tests file")
        test_path = filedialog.askopenfilename(filetypes=[("TXT Files", "*.txt*")])
        if test_path:
            with open(test_path,"r") as f:
                lines=f.readlines()
                for i in lines:
                    elements=i.split(",")
                    if len(elements)==2 or len(elements)==4:
                        continue
                    else:
                        messagebox.showerror("Error","Invalid File : File needs to have only 2 or 4 values in each line")
                        self.import_csv()
                        return
            self.test_file_path = test_path
            self.main_setup()

    """ basic setup for the screen """  
    def main_setup(self):
        self.frame = Frame(self.master, background="white")
        self.frame.place(x=320, y=40, width=550, height=420)

        self.test_categorylbl = Label(self.frame, text="Select a test to edit", font=self.font, bg="white")
        self.test_categorylbl.place(x=150,y=20)
        self.test_category_var = StringVar()
        self.load_test_names()
        self.test_category_menu = OptionMenu(self.frame, self.test_category_var, *self.test_names)
        self.test_category_menu.place(x=280,y=20)

        self.ok_btn = Button(self.frame, text="OK", font=self.font, command=self.ok)
        self.ok_btn.place(x=280,y=60)

        self.return_main_menu_btn = Button(self.frame, text="Return to Main Menu", font=self.font, command=self.callmainpage, bg="#f6be00", fg="black")
        self.return_main_menu_btn.place(x=260,y=350)

    """ main setup after values are assigned in basic setup """
    def setup_screen(self):
        # Test Name
        self.testnamelbl = Label(self.frame, text="Test Name : ", font=self.font, bg="white")
        self.testnamelbl.place(x=70,y=150)

        # Category Dropdown
        self.categorylbl = Label(self.frame, text="Category : ", font=self.font, bg="white")
        self.categorylbl.place(x=80,y=180)

        # Test Weight
        self.testweightlbl = Label(self.frame, text="Test Weight : ", font=self.font, bg="white")
        self.testweightlbl.place(x=60,y=210)

        # Out of
        self.outoflbl = Label(self.frame, text="Out of : ", font=self.font, bg="white")
        self.outoflbl.place(x=95,y=240)

        self.treeview_frame = Frame(self.frame, background="white")
        self.treeview_frame.place(x=250,y=130)
        self.treeview = ttk.Treeview(self.treeview_frame, columns=("Student #", "Mark"), show="headings", height=8)
        self.treeview.pack(side=LEFT)

        # Scrollbar
        scrollbar = Scrollbar(self.treeview_frame, orient="vertical", command=self.treeview.yview)
        scrollbar.pack(side=RIGHT, fill="y")
        self.treeview.configure(yscrollcommand=scrollbar.set)

        for col in ("Student #", "Mark"):
            self.treeview.heading(col, text=col)
            self.treeview.column(col, width=100)

        self.delete_test_btn = Button(self.frame, text="Delete Test", font=self.font, command=self.delete_test, bg="#f6be00", fg="black")
        self.delete_test_btn.place(x=160,y=350)

    """ displays information of test when it is selected """
    def ok(self):
        testname = self.test_category_var.get()
        if testname:
            with open(self.test_file_path,"r") as f:
                lines=f.readlines()
                index=0
                for i in lines:
                    if index==0:
                        index=1
                        continue
            
                    elements = i.split(",")
                    if index==2:
                        if len(elements)==2:
                            student_number=elements[0]
                            marks=elements[1]
                            self.treeview.insert("", END, values=(student_number,marks))
                            continue
                        else:
                            index=1
                            
                    if not len(elements)==4:
                        continue
                    else:
                        name = elements[0]
                        if name == testname:
                            self.setup_screen()
                            self.test_name = name.split("(")
                            self.testname_lbl = Label(self.frame, text=self.test_name[0], font=self.font, width=10, bg="white")
                            self.testname_lbl.place(x=150,y=150)
                            
                            self.category_name = elements[1]
                            self.category_lbl = Label(self.frame, text=self.category_name, font=self.font,width=10, bg="white")
                            self.category_lbl.place(x=150,y=180)
                            
                            self.test_weight = elements[2]
                            self.test_weight_lbl = Label(self.frame, text=self.test_weight, font=self.font, width=10, bg="white")
                            self.test_weight_lbl.place(x=150,y=210)
                            
                            self.out_of = elements[3]
                            self.out_of_lbl = Label(self.frame, text=self.out_of, font=self.font, width=10, bg="white")
                            self.out_of_lbl.place(x=150,y=240)
                            
                            index=2
        else:
            messagebox.showerror("Error","Please select a test to edit")

    """ deletes selected test from the tests file for all students """
    def delete_test(self):
        selected_testname = self.test_category_var.get()
        check = 0

        try:
            new_data = []
                
            with open(self.test_file_path,"r") as f:
                lines = f.readlines()
                index=0
                data = []
                data_index=0
                for i in lines:
                    if index==0:
                        index=1
                        new_data.append(i)
                        continue
                    elements = i.split(",")
                    if index==2:
                        if len(elements)==4:
                            new_data.append(i)
                            index=1
                            continue
                        else:
                            continue
                    
                    if not len(elements)==4:
                        new_data.append(i)
                        continue
                    else:
                        name_element = elements[0]
                        if name_element==selected_testname:
                            index=2
                            continue
                        else:
                            new_data.append(i)

            with open(self.test_file_path,"w") as f:
                for i in new_data:
                    f.write(i)

                messagebox.showinfo("Success","Test deleted successfully.")
                check=1

            if check==1:
                self.main_setup()

        except:
            messagebox.showerror("Error","Error deleting test.")

    """ calss main page """
    def callmainpage(self):
        self.master.destroy()
        from main_page import root_main
        main_page_instance = root_main()

    """ load test names for drop down menu """
    def load_test_names(self):
        try:
            with open(self.test_file_path, "r") as file:
                lines = file.readlines()
                self.test_names = []
                index=0
                for i in lines:
                    if index==0:
                        index=1
                        continue
                    elements = i.split(",")
                    if not len(elements)==4:
                        continue
                    else:
                        name = elements[0]
                        self.test_names.append(name)
        except:
            messagebox.showerror("Error", "Failed to load test names from tests.txt")
            return

def root_delete_test():
    root = Tk()
    app = DeleteTestModule(root)
    app.mainloop()

#root_delete_test()
