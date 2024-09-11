from tkinter import *
from tkinter import messagebox
from tkinter import filedialog
import os

class main(Frame):
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
        
        # Create frame for text
        self.text_frame = Frame(bg="white", width=600, height=420)
        self.text_frame.place(x=300, y=30)

        # Welcome text
        welcome_text = ("Welcome to the Virtual Hall of Achievement: Your Personal Online Student Grader!\n\n"
                        "Embark on a journey through the realm of organized academics, where managing your students becomes "
                        "not just easy, but a delightful experience. Picture a space where each of your students is not just "
                        "a name on a roster, but a budding story of potential and progress.\n\n"
                        "Enroll the Stars of Tomorrow: Add vibrant profiles for each student. Watch your classroom galaxy "
                        "grow as you input new names, ready to track their academic journey.\n\n"
                        "Craft Their Academic Tale: Every test, a chapter in their story of learning. Add their achievements, "
                        "fine-tune the details with updates, or turn the page by removing tests when needed.\n\n"
                        "Chart Their Growth: Like a skilled gardener, monitor each student's growth. Delve into the average "
                        "scores of individual students, unlocking the secrets to their academic needs and triumphs.\n\n"
                        "The Class Symphony: Tune into the melody of your class's performance. The app doesn’t just stop at "
                        "individual averages; step back to see the harmony of the entire class average.\n\n"
                        "A Graphical Odyssey: Journey through the visual landscapes of performance. Access engaging graphical "
                        "data that paints a picture of each student’s journey in your class.")

        self.welcome_label = Label(self.text_frame, text=welcome_text, font=self.font, bg="white", wraplength=580)
        self.welcome_label.place(x=10, y=40)

        # Set up the menu bar
        self.menu_bar = Menu(self.master)
        self.master.config(menu=self.menu_bar)

        # Add menu items
        self.setup_menu = Menu(self.menu_bar, tearoff=0)
        self.menu_bar.add_cascade(label="User Info", menu=self.setup_menu)
        self.setup_menu.add_command(label="View", command=self.viewuserinfo)
        self.setup_menu.add_command(label="Edit", command=self.edituserinfo)

        self.students_menu = Menu(self.menu_bar, tearoff=0)
        self.menu_bar.add_cascade(label="Students", menu=self.students_menu)
        self.students_menu.add_command(label="Open", command=self.callstudentspage)
        
        self.tests_menu = Menu(self.menu_bar, tearoff=0)
        self.menu_bar.add_cascade(label="Tests", menu=self.tests_menu)
        self.tests_menu.add_command(label="Add Test", command=self.calladdtestpage)
        self.tests_menu.add_command(label="Edit Test", command=self.calledittestpage)
        self.tests_menu.add_command(label="Delete Test", command=self.calldeletetestpage)

        self.report_menu = Menu(self.menu_bar, tearoff=0)
        self.menu_bar.add_cascade(label="Report", menu=self.report_menu)
        self.report_menu.add_command(label="Averages", command=self.callaveragespage)
        self.report_menu.add_command(label="Graph", command=self.callgraphpage)

        self.logout_menu = Menu(self.menu_bar, tearoff=0)
        self.menu_bar.add_cascade(label="Exit", menu=self.logout_menu)
        self.logout_menu.add_command(label="Log Out", command=self.callloginpage)

    """ calls login page """
    def callloginpage(self):
        root.destroy()
        import login_page

    """ calls graphing page """
    def callgraphpage(self):
        root.destroy()
        from graph_page import root_graph
        graph_page_instance = root_graph()

    """ calls page which adds tests"""
    def calladdtestpage(self):
        root.destroy()
        from add_test_page import root_add_test
        add_test_instance = root_add_test()

    """ calls page which edits tests """
    def calledittestpage(self):
        root.destroy()
        from edit_test_page import root_edit_test
        edit_test_instance = root_edit_test()

    """ calls page which deletes tests"""
    def calldeletetestpage(self):
        root.destroy()
        from delete_test_page import root_delete_test
        delete_test_instance = root_delete_test()

    """ calls students page """
    def callstudentspage(self):
        root.destroy()
        from students_page import root_students
        students_page_instance = root_students()

    """ calls page for calculating averages"""
    def callaveragespage(self):
        root.destroy()
        from overall_average_page import root_overall_average
        average_page_instance = root_overall_average()

    """ shows messagebox about all user info """
    def viewuserinfo(self):
        with open("setup.txt","r") as f:
            lines = f.readlines()
            str_lines=""
            info_tags = ["User Full Name : ",
                         "Course Name : ",
                         "Course code : ",
                         "Category 1 : ",
                         "Category 1 % : ",
                         "Category 2 : ",
                         "Category 2 % : ",
                         "Username : ",
                         "Password : ",
                         ]
            index=0
            for i in lines:
                str_lines+=info_tags[index]+i
                index+=1

            messagebox.showinfo("User Info",str_lines)

    """ calls page where user ccan edit their info """
    def edituserinfo(self):
        root.destroy()
        from editinfo_page import root_editinfo
        editinfo_page_instance = root_editinfo()

def root_main():
    global root
    root = Tk()
    app = main()
    app.mainloop()

#root_main()
