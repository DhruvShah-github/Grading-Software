from tkinter import *
from tkinter import ttk
from tkinter import messagebox
from tkinter import filedialog
import sys

class AverageModule(Frame):
    """ default init function """
    def __init__(self,root):
        super().__init__()
        self.master = root
        self.font = ("arial", 10)
        self.screenwidth = 925
        self.screenheight = 500
        self.screenx = 300
        self.screeny = 100
        self.screenname = ""
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

        self.import_files()

    """ imports required files """
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
                self.main_setup()

    """ sets up the main screen after importing files """
    def main_setup(self):
        self.frame = Frame(self.master, background="white")
        self.frame.place(x=320, y=40, width=550, height=400)

        self.treeview_frame = Frame(self.frame,background="white")
        self.treeview_frame.place(x=70,y=70)

        self.title_lbl = Label(self.frame, text="Student Averages", font=("arial",12), bg="white")
        self.title_lbl.place(x=210,y=20)

        # Create a Treeview to display student information
        self.student_tree = ttk.Treeview(self.treeview_frame, columns=("First Name", "Last Name", "Student #", "Average"), show="headings")
        self.student_tree.pack(side=LEFT)

        for col in ("First Name", "Last Name", "Student #", "Average"):
            self.student_tree.heading(col, text=col)
            self.student_tree.column(col, width=100)

        scrollbar = Scrollbar(self.treeview_frame, orient="vertical", command=self.student_tree.yview)
        scrollbar.pack(side=RIGHT, fill=Y)

        # Configure the Treeview to update the scrollbar
        self.student_tree.configure(yscrollcommand=scrollbar.set)

        # Add "Calculate Class Average" button
        self.class_average_lbl = Label(self.frame, text="Class Average :", font=self.font, bg="white")
        self.class_average_lbl.place(x=190, y=310)

        self.return_main_btn = Button(self.frame, text="Return to Main Menu", command=self.callmainpage, bg="#f6be00", fg="black")
        self.return_main_btn.place(x=205, y=350)

        student_file_path = self.stu_file_path
        self.read_student_file(student_file_path)

        # Replace 'tests.txt' with the actual path to your file
        test_file_path = self.test_file_path
        self.student_test_data = {}  # Dictionary to store test data for each student
        self.test_info_data = {}  # Dictionary to store test information
        self.read_test_file(test_file_path)

        # Replace 'setup.txt' with the actual path to your file
        setup_file_path = 'setup.txt'
        self.category1_weight, self.category2_weight = self.read_setup_file(setup_file_path)

        self.calculate_student()

    """ calls main page """
    def callmainpage(self):
        self.master.destroy()
        from main_page import root_main
        main_page_instance = root_main()

    """ calls edit page when categories are not matching """
    def calledittestspage(self):
        self.master.destroy()
        from edit_test_page import root_edit_test
        edit_page_instance = root_edit_test()

    """ reads inserts student information in the treeview """
    def read_student_file(self, file_path):
        try:
            with open(file_path, 'r') as file:
                # Read all lines from the file
                file_data = file.readlines()

                # Process the collected data (insert it into Treeview)
                student_data = []
                for line in file_data[1:]:  # Skip the first line (headers)
                    parts = line.strip().split(',')
                    if len(parts) == 3:
                        student_data.append((parts[0].strip(), parts[1].strip(), parts[2].strip()))

                # Sort students by last name and first name
                student_data.sort(key=lambda x: (x[1], x[0]))

                # Insert sorted data into the Treeview
                for student_info in student_data:
                    self.student_tree.insert("", "end", values=student_info)

        except FileNotFoundError as error:
            print(f"File not found: {file_path}")
            print("Error:", error, "Line:{}".format(sys.exc_info()[-1].tb_lineno))
        except Exception as error:
            print("Error:", error, "Line:{}".format(sys.exc_info()[-1].tb_lineno))

    """ reads marks from tests file to calculate average """
    def read_test_file(self, file_path):
        try:
            with open(file_path, 'r') as file:
                # Read all lines from the file
                file_data = file.readlines()

                test_info = None  
                for line in file_data[1:]:  
                    if line.strip():  
                        parts = line.strip().split(',')
                        if len(parts) == 4:  
                            test_info = (parts[1].strip(), parts[2].strip(), parts[3].strip())  
                            self.test_info_data[parts[0].strip()] = test_info  
                        elif len(parts) == 2:  
                            student_number = parts[0].strip()
                            grade = parts[1].strip()
                            test_title = parts[0].strip()

                            # Update student_test_data dictionary
                            if student_number not in self.student_test_data:
                                self.student_test_data[student_number] = []
                            self.student_test_data[student_number].append((test_title, grade, *test_info))

        except FileNotFoundError as error:
            print(f"File not found: {file_path}")
            print("Error:", error, "Line:{}".format(sys.exc_info()[-1].tb_lineno))
        except Exception as error:
            print("Error:", error, "Line:{}".format(sys.exc_info()[-1].tb_lineno))

    """ reads setup file for category weight """
    def read_setup_file(self, file_path):
        try:
            with open(file_path, 'r') as file:
                # Read all lines from the file
                file_data = file.readlines()

                # Extract the 5th and 7th lines
                category1_weight = float(file_data[4].strip()) / 100  # Convert percentage to decimal
                category2_weight = float(file_data[6].strip()) / 100  # Convert percentage to decimal
                self.category1 = file_data[3]
                self.category2 = file_data[5]

                return category1_weight, category2_weight

        except FileNotFoundError as error:
            print(f"File not found: {file_path}")
            print("Error:", error, "Line:{}".format(sys.exc_info()[-1].tb_lineno))
            return None, None
        except Exception as error:
            print("Error:", error, "Line:{}".format(sys.exc_info()[-1].tb_lineno))
            return None, None      

    """ calculates individual student average """
    def calculate_student(self):
        try:
            # Loop through all students in the treeview
            for student in self.student_tree.get_children():
                student_number = self.student_tree.item(student, 'values')[2]
                if str(student_number) not in self.student_test_data:
                    # If no data, set average to 0 or some placeholder value in the treeview
                    self.student_tree.set(student, column="average_column", value="No Data")
                    continue

                category1_totals = {}
                category2_totals = {}

                for test_data in self.student_test_data[student_number]:
                    test_title, grade, category, weight, out_of = test_data
                    grade = float(grade) if grade else 0  # Convert to float, assuming empty string as 0
                    weight = float(weight)
                    out_of = float(out_of)

                    test_average = (grade / out_of) * weight

                    if category == self.category1.strip():
                        category1_totals[category] = category1_totals.get(category, 0) + test_average
                    elif category == self.category2.strip():
                        category2_totals[category] = category2_totals.get(category, 0) + test_average
                    else:
                        messagebox.showerror("Error","Tests while doesn't have same test categories as setup file.\nPlease edit the test files to make the categories same")
                        self.calledittestspage()
                        return

                category1_average = category1_totals[self.category1.strip()]
                category2_average = category2_totals[self.category2.strip()]
                
                total_category1_weight = self.calculate_total_weight(self.category1.strip())
                total_category2_weight = self.calculate_total_weight(self.category2.strip())

                #print(total_category1_weight)
                #print(total_category2_weight)

                overall_category1_average = category1_average / total_category1_weight if total_category1_weight != 0 else 0
                overall_category2_average = category2_average / total_category2_weight if total_category2_weight != 0 else 0

                overall_average = (overall_category1_average * self.category1_weight) + (overall_category2_average * self.category2_weight)
                
                # Update the 4th column (average) in the treeview for the current student
                self.student_tree.set(student, column="Average", value=f"{overall_average:.2%}")

            self.calculate_class_average()

        except Exception as error:
            print("Error:", error, "Line:{}".format(sys.exc_info()[-1].tb_lineno))
            messagebox.showinfo("Error", "An unexpected error occurred. Details: {}".format(str(error)))

    """ calculates entire classes average """
    def calculate_class_average(self):
        #try: 
        num_students = 0
        total_class_average = 0

        for student_item_id in self.student_tree.get_children():
            student_values = self.student_tree.item(student_item_id, 'values')
            # Assuming the 4th column contains a numeric value representing the student's average
            if student_values[3]:
                student_average = float(student_values[3].strip("%"))
            else:
                student_average = 0

            total_class_average += student_average
            num_students += 1

        if num_students > 0:
            class_average = round(total_class_average / num_students,2)
            self.display_class_average_lbl = Label(self.frame, text=f"{class_average}%", font=self.font, bg="white")
            self.display_class_average_lbl.place(x=290, y=310)
        else:
            self.display_class_average_lbl = Label(self.frame, text="", font=self.font, bg="white")
            self.display_class_average_lbl.place(x=290, y=310)

        #except Exception as error:
            #print("Error:", error, "Line:{}".format(sys.exc_info()[-1].tb_lineno))
            #messagebox.showinfo("Error", "An unexpected error occurred. Details: {}".format(str(error)))

    """ calculates total weight of a category """
    def calculate_total_weight(self, category):
        total_weight = 0
        for test_info in self.test_info_data.values():
            test_category, weight, _ = test_info
            if test_category.lower() == category.lower():
                total_weight += float(weight)
        return total_weight


def root_overall_average():
    root = Tk()
    app = AverageModule(root)
    app.mainloop()

#root_overall_average()
