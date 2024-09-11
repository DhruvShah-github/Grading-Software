from tkinter import *
from tkinter import messagebox
from tkinter import ttk
from tkinter import filedialog
import csv

class EditTestModule(Frame):
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

    """ imports required files to run this page """
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

    """ sets up initial screen """
    def main_setup(self):
        self.frame = Frame(self.master, background="white")
        self.frame.place(x=320, y=35, width=550, height=430)

        self.test_categorylbl = Label(self.frame, text="Select a test to edit", font=self.font, bg="white")
        self.test_categorylbl.place(x=150,y=5)
        self.test_category_var = StringVar()
        self.load_test_names()
        self.test_category_menu = OptionMenu(self.frame, self.test_category_var, *self.test_names)
        self.test_category_menu.place(x=280,y=5)

        self.edit_btn = Button(self.frame, text="Edit", font=self.font, command=self.edit)
        self.edit_btn.place(x=280,y=38)

        self.return_main_menu_btn = Button(self.frame, text="Return to Main Menu", font=self.font, command=self.callmainpage, bg="#f6be00", fg="black")
        self.return_main_menu_btn.place(x=260,y=390)

    """ sets up main screen after values are assigned to main screen """
    def setup_screen(self):
        # Test Name
        self.testnamelbl = Label(self.frame, text="Test Name", font=self.font, bg="white")
        self.testnamelbl.place(x=70,y=75)
        self.testname_entry = Entry(self.frame, font=self.font, width=15, bg="white")
        self.testname_entry.place(x=70,y=105)

        # Category Dropdown
        self.categorylbl = Label(self.frame, text="Category", font=self.font, bg="white")
        self.categorylbl.place(x=205,y=75)
        self.category_var = StringVar()
        self.load_categories()
        self.category_menu = OptionMenu(self.frame, self.category_var, *self.categories)
        self.category_menu.place(x=200,y=105)

        # Test Weight
        self.testweightlbl = Label(self.frame, text="Test Weight", font=self.font, bg="white")
        self.testweightlbl.place(x=295,y=75)
        self.test_weight_entry = Entry(self.frame, font=self.font, width=10, bg="white")
        self.test_weight_entry.place(x=295,y=105)

        # Out of
        self.outoflbl = Label(self.frame, text="Out of", font=self.font, bg="white")
        self.outoflbl.place(x=400,y=75)
        self.out_of_entry = Entry(self.frame, font=self.font, width=10, bg="white")
        self.out_of_entry.place(x=400,y=105)

        self.treeview_frame = Frame(self.frame, background="white")
        self.treeview_frame.place(x=170,y=150)
        self.treeview = ttk.Treeview(self.treeview_frame, columns=("Student #", "Mark"), show="headings", height=8)
        self.treeview.pack(side=LEFT)

        # Scrollbar
        scrollbar = Scrollbar(self.treeview_frame, orient="vertical", command=self.treeview.yview)
        scrollbar.pack(side=RIGHT, fill="y")
        self.treeview.configure(yscrollcommand=scrollbar.set)

        for col in ("Student #", "Mark"):
            self.treeview.heading(col, text=col)
            self.treeview.column(col, width=100)

        self.markslbl = Label(self.frame, text="Mark:", font=self.font, bg="white")
        self.markslbl.place(x=160,y=350)
        self.marks_entry = Entry(self.frame, font=self.font, width=10, bg="white")
        self.marks_entry.place(x=200,y=352)

        self.edit_markbtn = Button(self.frame, text="Edit Mark", font=self.font, command=self.edit_mark)
        self.edit_markbtn.place(x=290,y=348)

        self.update_test_btn = Button(self.frame, text="Update Test", font=self.font, command=self.update_test, bg="#f6be00", fg="black")
        self.update_test_btn.place(x=160,y=390)

    """ opens up selected test to edit """
    def edit(self):
        testname = self.test_category_var.get()
        if testname:
            with open(self.test_file_path,"r") as f:
                lines=f.readlines()
                index=0
                for i in lines:
                    if not i=="\n":
                        if index==0:
                            index=1
                            continue
                
                        elements = i.split(",")
                        if index==2:
                            if len(elements)==2:
                                student_number=elements[0]
                                marks=elements[1].strip()
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
                                self.testname_entry.insert(0,name)
                                self.test_weight_entry.insert(0,elements[2])
                                self.out_of_entry.insert(0,elements[3])
                                index=2
        else:
            messagebox.showerror("Error","Please select a test to edit")

    """ updates the test selected by writing the new content in the test file """
    def update_test(self):
        # Retrieve values from the UI elements
        test_name = self.testname_entry.get()
        category = self.category_var.get()
        test_weight = self.test_weight_entry.get()
        out_of = self.out_of_entry.get()
        selected_testname = self.test_category_var.get()

        # Check if any field is empty
        if not (test_name and category and test_weight and out_of):
            messagebox.showerror("Error", "All fields are required.")
            self.testname_entry.focus_set()
            return

        # Validate if test_weight and out_of are floats
        if not self.validate_float(test_weight):
            self.test_weight_entry.focus_set()
            return
        if not self.validate_float(out_of):
            self.out_of_entry.focus_set()
            return

        try:
            new_data = []
                
            with open(self.test_file_path,"r") as f:
                lines = f.readlines()
                index=0
                data = []
                data_index=0
                for item_id in self.treeview.get_children():
                        item_data = self.treeview.item(item_id)['values']
                        item_data = str(item_data[0])+","+str(item_data[1])+"\n"
                        data.append(item_data)
                for i in lines:
                    if not i=="\n":
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
                                new_data.append(data[data_index])
                                data_index+=1
                                continue
                        
                        if not len(elements)==4:
                            new_data.append(i)
                            continue
                        else:
                            name_element = elements[0]
                            if name_element==selected_testname:
                                info = test_name+","+category+","+test_weight+","+out_of
                                new_data.append(info)
                                index=2
                                continue
                            else:
                                new_data.append(i)

            with open(self.test_file_path,"w") as f:
                for i in new_data:
                    f.write(i)

            messagebox.showinfo("Success","Test updated successfully.")
            self.main_setup()

        except:
            messagebox.showerror("Error","tests.txt doesn't exists")

    """ calls main page """
    def callmainpage(self):
        self.master.destroy()
        from main_page import root_main
        main_page_instance = root_main()

    """ changes mark of the student selected in the treeview """
    def edit_mark(self):
        # Get mark value
        mark_value = self.marks_entry.get()
        out_of_value = self.out_of_entry.get()

        # Check if 'out of' is empty
        if not out_of_value:
            messagebox.showerror("Error", "Please fill the 'Out of' field first.")
            self.out_of_entry.focus_set()
            return

        # Validate if mark is a float
        if not self.validate_float(mark_value):
            self.marks_entry.focus_set()
            return

        try:# Convert mark and out_of to float
            if mark_value:
                mark_value = float(mark_value)
        except:
            messagebox.showerror("Error","The mark value should be a float")
            return

        try:
            out_of_value = float(out_of_value)
        except:
            messagebox.showerror("Error","The out of value should be a float")
            return
            
        # Check if the mark is within the valid range
        if mark_value < 0 or mark_value > out_of_value:
            messagebox.showerror("Error", "Mark must be greater than zero and less than or equal to 'Out of' value.")
            self.marks_entry.focus_set()
            return

        # Insert the mark into the selected treeview row
        selected_item = self.treeview.focus()
        if selected_item:  # check if an item is selected
            self.treeview.item(selected_item, values=(*self.treeview.item(selected_item)["values"][:1], mark_value))
        else:
            messagebox.showerror("Error","Please select a student from the list")
            return

        # Clear the marks entry
        self.marks_entry.delete(0, END)

    """ loads test names for the drop down menu """
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

    """ loads the categories of tests from setup file """
    def load_categories(self):
        try:
            with open("setup.txt", "r") as file:
                lines = file.readlines()
                self.categories = [lines[3].strip(), lines[5].strip()]
        except:
            messagebox.showerror("Error", "Failed to load categories from setup.txt")
            self.categories = ["Category1", "Category2"]

    """ validates if a value if float or not """
    def validate_float(self, value):
        if value == "":
            return True
        try:
            float(value)
            return True
        except ValueError:
            messagebox.showerror("Error", "Please enter a valid float value")
            return False

def root_edit_test():
    root = Tk()
    app = EditTestModule(root)
    app.mainloop()

#root_edit_test()
