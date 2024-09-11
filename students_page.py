import csv
import os
from tkinter import *
from tkinter import ttk
from tkinter import filedialog
from tkinter import messagebox
import sys

class StudentsModule(Frame):
    """ default init function """
    def __init__(self, master):
        super().__init__(master)
        self.master = master
        self.font = ("arial", 12)
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

        self.used_student_numbers = set()  # Set to store used student numbers
        self.import_files()

    """ imports all required files """
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
                self.setup_ui()

    """ sets up main screen after importing files """
    def setup_ui(self):
        self.index=0
        # Menu
        menubar = Menu(self.master)
        self.master.config(menu=menubar)

        exit_menu = Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Exit", menu=exit_menu)
        exit_menu.add_command(label="Main Page", command=self.callmainpage)

        self.mainframe = Frame(bg="white", width=500, height=400)
        self.mainframe.place(x=350, y=40)
        
        self.frame = Frame(self.mainframe)
        self.frame.place(x=98, y=30)

        self.treeview = ttk.Treeview(self.frame, columns=("First Name", "Last Name", "Student Number"), show="headings")
        self.treeview.pack(side=LEFT)

        # Scrollbar
        scrollbar = Scrollbar(self.frame, orient="vertical", command=self.treeview.yview)
        scrollbar.pack(side=RIGHT, fill="y")
        self.treeview.configure(yscrollcommand=scrollbar.set)

        for col in ("First Name", "Last Name", "Student Number"):
            self.treeview.heading(col, text=col)
            self.treeview.column(col, width=100)
            
        frame_entrybox = Frame(self.mainframe,bg="white")
        frame_entrybox.place(x=35,y=265)

        label_first_name = Label(frame_entrybox, text="First Name", font=self.font, bg="white", fg="black")
        label_first_name.grid(row=0, column=0, padx=5, pady=5)
        self.txt_first_name = Entry(frame_entrybox, bg="white", font=self.font, width=15)
        self.txt_first_name.grid(row=1, column=0, padx=5, pady=5)
        self.txt_first_name.focus()

        label_last_name = Label(frame_entrybox, text="Last Name", font=self.font, bg="white", fg="black")
        label_last_name.grid(row=0, column=1, padx=5, pady=5)
        self.txt_last_name = Entry(frame_entrybox, bg="white", font=self.font, width=15)
        self.txt_last_name.grid(row=1, column=1, padx=5, pady=5)

        label_student_number = Label(frame_entrybox, text="Student Number", font=self.font, bg="white", fg="black")
        label_student_number.grid(row=0, column=2, padx=5, pady=5)
        self.txt_student_number = Entry(frame_entrybox, bg="white", font=self.font, width=15)
        self.txt_student_number.grid(row=1, column=2, padx=5, pady=5)

        # Buttons
        frame_buttons = Frame(self.mainframe,bg="white")
        frame_buttons.place(x=155, y=350)

        self.add_btn = Button(frame_buttons, text="Add", font=self.font, fg="black", bg="#f6be00", command=self.add)
        self.add_btn.pack(side=LEFT, padx=5)

        self.update_btn = Button(frame_buttons, text="Update", font=self.font, fg="black", bg="#f6be00", command=self.update)
        self.update_btn.pack(side=LEFT, padx=5)

        self.delete_btn = Button(frame_buttons, text="Delete", font=self.font, fg="black", bg="#f6be00", command=self.delete)
        self.delete_btn.pack(side=LEFT, padx=5)

        self.import_csv()

    """ displays information in the treeview """
    def import_csv(self):
        try:
            with open(self.stu_file_path, newline='') as csvfile:
                reader = csv.reader(csvfile)
                next(reader)  # Skip the header
                for row in reader:
                    if row:
                        first_name, last_name, student_number = row
                        if not self.is_valid_student_number(student_number):
                            messagebox.showerror("Invalid Student Number", "Student number must be unique.")
                            return
                        self.treeview.insert("", END, values=(first_name, last_name, student_number))
                        self.used_student_numbers.add(student_number)
        except Exception as e:
            messagebox.showerror("Error", f"Error reading file: {e}")

    """ adds student information to students file and student# to the tests file """
    def add(self):
        try:
            first_name = self.txt_first_name.get().strip()
            last_name = self.txt_last_name.get().strip()
            student_number = self.txt_student_number.get().strip()

            if not first_name or not last_name or not student_number:
                messagebox.showerror("Empty Fields", "All fields must be filled.")
                return

            if "," in first_name or "," in last_name or "," in student_number:
                messagebox.showerror("Comma Detected","Cannot have a comma in any field")
                return
            
            if not self.is_valid_student_number(student_number):
                messagebox.showerror("Invalid Student Number", "Student number must be unique.")
                self.txt_student_number.focus()
                return

            if first_name and last_name and student_number:
                self.treeview.insert("", END, values=(first_name, last_name, student_number))
                self.used_student_numbers.add(student_number)
                self.clear_entry_boxes()

            with open(self.stu_file_path,"r") as f:
                lines=f.readlines()
                if lines and lines[-1].endswith("\n"):
                    line = first_name+","+last_name+","+student_number+"\n"
                else:
                    line = "\n"+first_name+","+last_name+","+student_number+"\n"

            with open(self.stu_file_path,"a") as f:
                f.write(line)

            # Process tests.txt
            new_lines = []
            line_count = 0
            with open(self.test_file_path, "r") as file:
                for line in file:
                    if line_count < 2:  # Append first two lines
                        new_lines.append(line)
                        line_count += 1
                    else:
                        elements = line.split(',')
                        if len(elements) == 4:
                            new_lines.append(student_number + ","+"\n")
                            new_lines.append(line)
                        else:
                            new_lines.append(line)
                            
            if new_lines[-1].endswith("\n"):
                new_lines.append(student_number + ","+"\n")  # Append after the last line
            else:
                new_lines.append("\n" + student_number + ","+"\n")

            # Write the new contents to tests.txt
            with open(self.test_file_path, "w") as file:
                file.writelines(new_lines)

            messagebox.showinfo("Success", f"New student information added in {os.path.basename(self.stu_file_path)}.\n")

        except Exception as error:
            messagebox.showerror("Error:","An error occured in add")
            return

    """ Updates student information in the students file and updates student# in the tests file if it is changed """
    def update(self):
        try:
            if self.treeview.selection():
                row = self.treeview.selection()[0]
                first_name = self.txt_first_name.get().strip()
                last_name = self.txt_last_name.get().strip()
                student_number = self.txt_student_number.get().strip()

                current_first_name = self.treeview.item(row, 'values')[0]
                current_last_name = self.treeview.item(row, 'values')[1]
                current_student_number = self.treeview.item(row, 'values')[2]
                if not first_name or not last_name or not student_number:
                    messagebox.showerror("Empty Fields", "All fields must be filled.")
                    return

                if student_number != current_student_number and not self.is_valid_student_number(student_number):
                    messagebox.showerror("Invalid Student Number", "Student number must be unique.")
                    self.txt_student_number.focus()
                    return

                if first_name and last_name and student_number:
                    self.treeview.item(row, values=(first_name, last_name, student_number))
                    self.used_student_numbers.remove(current_student_number)
                    self.used_student_numbers.add(student_number)
                    self.clear_entry_boxes()
        
                with open(self.stu_file_path,"r") as f:
                        lines = f.readlines()
                        index=0
                        if lines:
                            for i in lines:
                                if i=="\n":
                                    continue
                                else:
                                    j=i
                                    if index==0:
                                        index=1
                                        continue
                                    new = j.split(",")
                                    new[2]=new[2].replace("\n","")
                                    if new[0]==current_first_name and new[1]==current_last_name and new[2]==current_student_number:
                                        text = first_name+","+last_name+","+student_number+"\n"
                                        index = lines.index(i)
                                        lines[index] = text
                                        break
                                        
                with open(self.stu_file_path,"w") as f:
                    f.writelines(lines)

                if not student_number==current_student_number:
                    with open(self.test_file_path,"r") as f:
                        lines=f.readlines()
                        new_data = []
                        for i in lines:
                            elements=i.split(",")
                            if len(elements)==2:
                                if elements[0]==str(current_student_number):
                                    new_row = student_number+","+elements[1]
                                    new_data.append(new_row)
                                else:
                                    new_data.append(i)
                            else:
                                new_data.append(i)

                    with open(self.test_file_path,"w") as f:
                        for j in new_data:
                            f.write(j)
                                    
                messagebox.showinfo("Success",f"Student information updated in {os.path.basename(self.stu_file_path)}.\n")

            else:
                messagebox.showerror("Error","Please select a student from the treeview to update.")

        except Exception as error:
            messagebox.showerror("Error:","An error occurede in update.")

    """ deletes student information from students file and deletes student# form tests file """   
    def delete(self):
        try:
            if self.treeview.selection():
                row = self.treeview.selection()[0]
                current_first_name = self.treeview.item(row, 'values')[0]
                current_last_name = self.treeview.item(row, 'values')[1]
                current_student_number = self.treeview.item(row, 'values')[2]
                self.treeview.delete(row)
                self.used_student_numbers.remove(current_student_number)
                self.clear_entry_boxes()
            
                with open(self.stu_file_path,"r") as f:
                        lines = f.readlines()
                        index=0
                        for i in lines:
                            if i=="\n":
                                continue
                            else:
                                j=i
                                if index==0:
                                    index=1
                                    continue
                                new = j.split(",")
                                new[2]=new[2].replace("\n","")
                                if new[0]==current_first_name and new[1]==current_last_name and new[2]==current_student_number:
                                    index = lines.index(i)
                                    lines[index] = ""
                                    break
                                        
                with open(self.stu_file_path,"w") as f:
                    f.writelines(lines)

                with open(self.test_file_path,"r") as f:
                    file_data = f.readlines()
                    new_data = []
                    for i in file_data:
                        elements = i.split(",")
                        if not len(elements)==2:
                            new_data.append(i)
                            continue
                        else:
                            if str(elements[0])==str(current_student_number):
                                continue
                            else:
                                new_data.append(i)

                with open(self.test_file_path,"w") as f:
                    for i in new_data:
                        f.write(i)
                        
                messagebox.showinfo("Success",f"Student information deleted from {os.path.basename(self.stu_file_path)}.\n")

            else:
                messagebox.showerror("Error","Please select a student from the treeview to delete.")
                    
        except Exception as error:
            messagebox.showerror("Error:","An error occured in delete.")

    """ checks is student number already exists or not """
    def is_valid_student_number(self, student_number):
        return student_number not in self.used_student_numbers

    """ clears all entry boxes when a button a function is executed """
    def clear_entry_boxes(self):
        self.txt_first_name.delete(0, END)
        self.txt_last_name.delete(0, END)
        self.txt_student_number.delete(0, END)

    """ calls main page """
    def callmainpage(self):
        self.master.destroy()
        from main_page import root_main
        main_page_instance = root_main()

def root_students():
    root = Tk()
    app = StudentsModule(root)
    app.mainloop()

#root_students()
