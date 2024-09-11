from tkinter import *
from tkinter import ttk
from tkinter import messagebox
from tkinter import filedialog
import os

class GraphingModule(Frame):
    """ default init function """
    def __init__(self, root):
        super().__init__(root)
        self.master = root
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
                self.setup_widgets()

    """ sets up main screen """
    def setup_widgets(self):
        self.mainframe = Frame(bg="white", width=850, height=440)
        self.mainframe.place(x=35,y=30)

        self.treeframe = Frame(self.mainframe)
        self.treeframe.place(x=240,y=10)
        
        self.tree = ttk.Treeview(self.treeframe, columns=('FirstName', 'LastName', 'StudentNumber'), show="headings", height=5)
        self.tree.pack(side=LEFT)

        scrollbar = Scrollbar(self.treeframe, orient="vertical", command=self.tree.yview)
        scrollbar.pack(side=RIGHT, fill="y")
        self.tree.configure(yscrollcommand=scrollbar.set)

        #self.tree.heading('#0', text='ID')
        self.tree.heading('FirstName', text='First Name')
        self.tree.heading('LastName', text='Last Name')
        self.tree.heading('StudentNumber', text='Student #')
        #self.tree.column('#0', width=0, stretch=tk.NO)
        self.tree.column('FirstName', width=100)
        self.tree.column('LastName', width=100)
        self.tree.column('StudentNumber', width=100)

        self.load_students()

        self.show_graph_button = Button(self.mainframe, text="Show Graph", command=self.show_graph, bg="#f6be00", fg="black")
        self.show_graph_button.place(x=580,y=70)

        self.mainmenu_button = Button(self.mainframe, text="Return to Main Menu", command=self.callmainpage, bg="#f6be00", fg="black")
        self.mainmenu_button.place(x=580,y=110)

    """ calls main page """
    def callmainpage(self):
        self.master.destroy()
        from main_page import root_main
        main_page_instance = root_main()

    """ loads student information and inserts in treeview """
    def load_students(self):
        with open(self.stu_file_path, 'r') as file:
            next(file)  # Skip the first line
            for line in file:
                if line.strip():
                    first_name, last_name, student_number = line.strip().split(',')
                    self.tree.insert('', END, values=(first_name, last_name, student_number))

    """ gets required values for graphing """
    def show_graph(self):
        try:
            selected_item = self.tree.focus()
            if not selected_item:
                messagebox.showerror("Error","Please select a student")
                return

            student_data = self.tree.item(selected_item)['values']
            student_number = student_data[2]

            test_names = []
            scores = []
            total_marks = None

            with open(self.test_file_path, 'r') as file:
                index=0
                for line in file:
                    if line:
                        if index==0:
                            index=1
                            continue
                        if line:
                            parts = line.split(',')
                            if len(parts) == 4:
                                test_name, _, _, total_marks = parts
                                test_names.append(test_name)
                                total_marks = float(total_marks)
                            elif len(parts) == 2 and total_marks is not None:
                                if parts[0] == str(student_number):
                                    if not parts[1]=="\n" and not parts[1].strip()=="":
                                        mark = float(parts[1].strip())
                                    else:
                                        mark = 0
                                    percentage = (mark / total_marks) * 100
                                    scores.append(percentage)
                            else:
                                # Reset total_marks for the next test
                                total_marks = None

        except:
            messagebox.showerror("Error","Marks should be float")
            return

        self.plot_graph(test_names, scores)

    """ creates actual graph using canvas module """
    def plot_graph(self, test_names, scores):
        try:
            canvas_width = len(test_names) * 100
            canvas_height = 300
            canvas = Canvas(self.mainframe, width=canvas_width, height=canvas_height, bg="white")
            canvas.place(x=0, y=150)

            # Calculate bar width and spacing
            bar_width = 40
            spacing = 40
            offset = 50

            max_score = 100  # Max score is 100% for the y-axis
            graph_height = 200  # Height of the graph area for bars

            x0 = offset + 10  # Starting x-coordinate for the first bar

            for i in range(len(test_names)):
                test_name = test_names[i]
                score = scores[i]

                # Calculate y-coordinate based on score
                y0 = canvas_height - 50 - (graph_height * score / max_score)
                y1 = canvas_height - 50  # Base line of the graph

                # Draw the bar for the test
                canvas.create_rectangle(x0, y0, x0 + bar_width, y1, fill="#f6be00")

                # Draw test name. Adjust position if needed.
                canvas.create_text(x0 + bar_width / 2, y1 + 10, text=test_name, anchor="n")

                # Draw the score above the bar
                score_text = "{:.1f}%".format(score)  # Format the score to one decimal place
                canvas.create_text(x0 + bar_width / 2, y0 - 10, text=score_text, anchor="s")

                # Move to the next bar's x-coordinate
                x0 += bar_width + spacing

            extension = 10

            # Draw the axes
            canvas.create_line(offset, canvas_height - 50, canvas_width - offset, canvas_height - 50)  # X-axis
            canvas.create_line(offset, 50 - extension, offset, canvas_height - 50)  # Y-axis

            # Adding Y-axis labels (0% to 100%)
            for i in range(11):
                y_label = "{}% -".format(i * 10)
                y_position = canvas_height - 51 - (i * graph_height / 10)
                canvas.create_text(offset, y_position, text=y_label, anchor="e")

        except:
            messagebox.showerror("Error","An error occured")
        
def root_graph():
    root = Tk()
    app = GraphingModule(root)
    app.mainloop()

#root_graph()
