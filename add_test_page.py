from tkinter import *
from tkinter import messagebox
from tkinter import ttk
from tkinter import filedialog
import csv

class AddTestModule(Frame):
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

        # Create a frame
        self.frame = Frame(self.master, background="white")
        self.frame.place(x=320, y=40, width=550, height=420)

        self.importlbl = Label(self.frame, text="Please import files to proceed.", font=self.font, bg="white")
        self.importlbl.place(x=180,y=100)

        self.import_btn = Button(self.frame, text="Import Files", font=self.font, command=self.import_files, bg="#f6be00", fg="black")
        self.import_btn.place(x=150,y=360)

        self.return_main_menu_btn = Button(self.frame, text="Return to Main Menu", font=self.font, command=self.callmainpage, bg="#f6be00", fg="black")
        self.return_main_menu_btn.place(x=260,y=360)

    """ places widgets and creates a screen """
    def setup_screen(self):
        # Test Name
        self.testnamelbl = Label(self.frame, text="Test Name", font=self.font, bg="white")
        self.testnamelbl.place(x=70,y=20)
        self.testname_entry = Entry(self.frame, font=self.font, width=15, bg="white")
        self.testname_entry.place(x=70,y=50)

        # Category Dropdown
        self.categorylbl = Label(self.frame, text="Category", font=self.font, bg="white")
        self.categorylbl.place(x=205,y=20)
        self.category_var = StringVar()
        self.load_categories()
        self.category_menu = OptionMenu(self.frame, self.category_var, *self.categories)
        self.category_menu.place(x=200,y=50)

        # Test Weight
        self.testweightlbl = Label(self.frame, text="Test Weight", font=self.font, bg="white")
        self.testweightlbl.place(x=295,y=20)
        self.test_weight_entry = Entry(self.frame, font=self.font, width=10, bg="white")
        self.test_weight_entry.place(x=295,y=50)

        # Out of
        self.outoflbl = Label(self.frame, text="Out of", font=self.font, bg="white")
        self.outoflbl.place(x=400,y=20)
        self.out_of_entry = Entry(self.frame, font=self.font, width=10, bg="white")
        self.out_of_entry.place(x=400,y=50)

        self.treeview_frame = Frame(self.frame, background="white")
        self.treeview_frame.place(x=70,y=100)
        self.treeview = ttk.Treeview(self.treeview_frame, columns=("First Name", "Last Name", "Student #", "Mark"), show="headings", height=8)
        self.treeview.pack(side=LEFT)

        # Scrollbar
        scrollbar = Scrollbar(self.treeview_frame, orient="vertical", command=self.treeview.yview)
        scrollbar.pack(side=RIGHT, fill="y")
        self.treeview.configure(yscrollcommand=scrollbar.set)

        for col in ("First Name", "Last Name", "Student #", "Mark"):
            self.treeview.heading(col, text=col)
            self.treeview.column(col, width=100)

        self.import_csv()

        self.markslbl = Label(self.frame, text="Mark:", font=self.font, bg="white")
        self.markslbl.place(x=150,y=307)
        self.marks_entry = Entry(self.frame, font=self.font, width=10, bg="white")
        self.marks_entry.place(x=190,y=307)

        self.add_markbtn = Button(self.frame, text="Add Mark", font=self.font, command=self.add_mark)
        self.add_markbtn.place(x=300,y=303)

        self.create_test_btn = Button(self.frame, text="Create Test", font=self.font, command=self.create_test, bg="#f6be00", fg="black")
        self.create_test_btn.place(x=160,y=360)

    """ imports required files for this page to run """
    def import_files(self):
        messagebox.showinfo("Info","Import students file")
        self.stu_file_path = filedialog.askopenfilename(filetypes=[("TXT Files", "*.txt*")])
        if self.stu_file_path:
            with open(self.stu_file_path,"r") as f:
                lines=f.readlines()
                for i in lines:
                    elements = i.split(",")
                    if not len(elements)==3:
                        messagebox.showerror("Error","Invalid File : File needs to have only 3 values in each line")
                        self.import_files()
                        return
            messagebox.showinfo("Info","Now please import tests file.")
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
                            self.import_files()
                            return
                self.test_file_path = test_path
                self.import_btn.destroy()
                self.setup_screen()

    """ reads data from student file and places it in treeview """
    def import_csv(self):
        try:
            with open(self.stu_file_path, newline='') as csvfile:
                reader = csv.reader(csvfile)
                next(reader)  # Skip the header
                for row in reader:
                    if row:
                        first_name, last_name, student_number = row
                        self.treeview.insert("", END, values=(first_name, last_name, student_number))
        except Exception as e:
            messagebox.showerror("Error", f"Error reading file: {e}")

    """ validates all the fields and saves a test in the tests file """
    def create_test(self):
        # Retrieve values from the UI elements
        test_name = self.testname_entry.get()
        category = self.category_var.get()
        test_weight = self.test_weight_entry.get()
        out_of = self.out_of_entry.get()

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
            with open(self.test_file_path, "a") as file:
                file.write(f"{test_name}, {category} , {test_weight}, {out_of}\n")

                # Get data from the treeview and write to file
                for child in self.treeview.get_children():
                    student_data = self.treeview.item(child)['values']
                    student_id = student_data[2]

                    # Check if Mark exists, if not assign an empty string
                    if len(student_data) > 3:
                        student_mark = student_data[3]
                    else:
                        student_mark = ""

                    file.write(f"{student_id}, {student_mark}\n")

            # Restart the process
            messagebox.showinfo("Successful","Test addeed successfully")
            self.callmainpage()

        except Exception as e:
            messagebox.showerror("Error", f"Failed to write to tests.txt: {e}")

    """ calls main page """
    def callmainpage(self):
        self.master.destroy()
        from main_page import root_main
        main_page_instance = root_main()

    """ adds mark for the person selected in the treeview """
    def add_mark(self):
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
            self.treeview.item(selected_item, values=(*self.treeview.item(selected_item)["values"][:3], mark_value))
        else:
            messagebox.showerror("Error","Please select a student from the list")
            return

        # Clear the marks entry
        self.marks_entry.delete(0, END)

    """ categories for OptionMenu or Drop down menu """
    def load_categories(self):
        try:
            with open("setup.txt", "r") as file:
                lines = file.readlines()
                self.categories = [lines[3].strip(), lines[5].strip()]
        except:
            messagebox.showerror("Error", "Failed to load categories from setup.txt")
            self.categories = ["Category1", "Category2"]

    """ validates if marks, out of marks are float """
    def validate_float(self, value):
        if value == "":
            return True
        try:
            float(value)
            return True
        except ValueError:
            messagebox.showerror("Error", "Please enter a valid float value")
            return False

def root_add_test():
    root = Tk()
    app = AddTestModule(root)
    app.mainloop()

#root_add_test()
