import tkinter as Tkinter
from tkinter import ttk
import pymysql
#import myGame
import GameEngine
from tkinter import *
import tkinter as tk
from tkinter import messagebox




# ----------------------------------------
# DataBase Section
# ----------------------------------------------


#create databaseYah
# already created for now so disable this code :
#
# conn = pymysql.connect(host='localhost', port=3306, user='root',password='0599')
#
# try :
#     with conn.cursor() as cursor:
#         cursor.execute('CREATE DATABASE IF NOT EXISTS Statistics_gameDB ')
# except:
#     print("sth went wrong")
# else:
#     print("created a db")
# finally:
#     conn.close()
#
# # #create tables
#
# conn2 = pymysql.connect(host='localhost', port=3306, user='root',password='0599',db='Statistics_gameDB',cursorclass=pymysql.cursors.DictCursor)
#
# try :
#     with conn2.cursor() as curser :
#         sqlquery = 'CREATE TABLE IF NOT EXISTS high_scores(ID INT NOT NULL AUTO_INCREMENT,Date DATETIME , player_name TEXT ,coins_get INT,enemies_killed INT,dying_times INT,level_reached INT,last_score INT,PRIMARY KEY (ID))'
#         curser.execute(sqlquery)
#
# finally:
#     conn2.close()




def goToAnotherFrame():
    # HiName()
    class Yah(Tkinter.Frame):
        '''
        classdocs
        '''
        def __init__(self, parent):
            '''
            Constructor
            '''
            Tkinter.Frame.__init__(self, parent)
            self.parent=parent
            self.initialize_user_interface()

        def initialize_user_interface(self):

            self.submit_button = Tkinter.Button(self.parent, text = "VIEW High Scores", command = self.load_data)
            self.submit_button.grid(row = 2, column = 1, sticky = Tkinter.W)


            # Set the treeview
            self.tree = ttk.Treeview( self.parent, columns=('Gaming date','Player Name', 'Coins Get','Enemies Killed','Dying Times','Level Reached','Last Score'))
            self.tree.heading('#0', text='Order')
            self.tree.heading('#1', text='Gaming Date')
            self.tree.heading('#2', text='Player Name')
            self.tree.heading('#3', text='Coins Get')
            self.tree.heading('#4', text='Enemies Killed')
            self.tree.heading('#5', text='Dying Times')
            self.tree.heading('#6', text='Level Reached')
            self.tree.heading('#7', text='Last Score')



            self.tree.column('#0',width=80 , stretch=Tkinter.YES)
            self.tree.column('#1',width=150 , stretch=Tkinter.YES)
            self.tree.column('#2',width=100, stretch=Tkinter.YES)
            self.tree.column('#3',width=100, stretch=Tkinter.YES)
            self.tree.column('#4',width=100, stretch=Tkinter.YES)
            self.tree.column('#5',width=100, stretch=Tkinter.YES)
            self.tree.column('#6',width=100, stretch=Tkinter.YES)
            self.tree.column('#7',width=100, stretch=Tkinter.YES)




            self.tree.grid(row=4, columnspan=2, sticky='nsew')
            self.treeview = self.tree
            # Initialize the counter
            self.i = 0


        def load_data(self):

            conn2 = pymysql.connect(host='localhost', port=3306, user='root', password='0599', db='Statistics_gameDB')

            try:
                curs = conn2.cursor()
                SQLquery = "Select * from high_scores"
                curs.execute(SQLquery,)


                cpt = 0  # Counter representing the ID of your code.
                for row in curs:
                    print(row[0])
                    self.tree.insert('', 'end', text=str(cpt), values=(row[1], row[2], row[3], row[4], row[5], row[6],row[7]))
                    cpt += 1  # increment the ID
            finally:
                conn2.close()


    def main():
        root=Tkinter.Tk()
        d=Yah(root)
        root.title("Statistics")
        root.configure(background="#a1dbcd")

        root.mainloop()
            # importing a file will make it excute when we just run the file importing in so :
    if __name__=="__main__":
        main()






# ============================================================
def open_settings():

    window = tk.Toplevel(root)
    window.configure(background="#a1dbcd")
    window.title("Welcome , Settings Tab")
    window.geometry("400x400")

    # photo = hi.PhotoImage(file="img/title.gif")
    # w = hi.Label(window, image=photo)

    label = tk.Label(window, text="You can Change some settings here:", fg="#383a39", bg="#a1dbcd",
                     font=("Helvetica", 14))
    label.grid(row=2, column=0, columnspan=2)
    ActiveSoundsLbl = tk.Label(window, text="Enable Sounds :", fg="#383a39", bg="#a1dbcd", font=("Helvetica", 14))
    ActiveSoundsLbl.grid(row=4, column=0, )

    v = tk.IntVar()


    def ChangeOnOff():
        if (v.get() == 1):
            myGame.staticsVars.setSounds = True
            text = "Sounds is Enabled "
            print(text, v.get())
        elif (v.get() == 0):
            myGame.staticsVars.setSounds = False
            text = "Sounds is Disabled "
            print(text, v.get())
        messagebox.showinfo('Sounds Settings ', "You Set Option to : %s " % (str(text)))


    rb = tk.Radiobutton(window, text="On", variable=v, value=1, command=ChangeOnOff)
    rb.grid(row=5, column=0,columnspan=2)
    rb.select()
    rb2 = tk.Radiobutton(window, text="Off", variable=v, value=0, command=ChangeOnOff)
    rb2.grid(row=6, column=0,columnspan=2)
    rb2.deselect()

    pl_1 = tk.Label(window, text="------------------------------------------------------------------", fg="#383a39", bg="#a1dbcd", font=("Helvetica", 14))
    pl_1.grid(row=7, column=0 , columnspan=2)


    pl_jump = tk.Label(window, text="Choose Player's Jump's height :", fg="#383a39", bg="#a1dbcd", font=("Helvetica", 14))
    pl_jump.grid(row=8, column=0, )

    def main_change(*args):
        myGame.staticsVars.setJumpingLev = int(main_selected.get())
        print("ur jump has been set to ",myGame.staticsVars.setJumpingLev)
        messagebox.showinfo('Changing Done ', "Your jump has been set to = %s " % (myGame.staticsVars.setJumpingLev))
    main_selected = StringVar()
    main_selected.trace('w',main_change)
    combo = tk.ttk.Combobox(window,textvariable=main_selected)
    combo.grid(row=10,column=0)
    combo['values'] = (5, 6, 7, 8, 9, 10)


    pl_ = tk.Label(window, text="----------------------------------------------------------------", fg="#383a39", bg="#a1dbcd", font=("Helvetica", 14))
    pl_.grid( column=0 , columnspan=2)


    label_B = tk.Label(window, text="How many Bullets you'd love \n to shoot 'same screen':", fg="#383a39", bg="#a1dbcd", font=("Helvetica", 14))
    label_B.grid(row=15, column=0 )


    def main_spin(*args):
        myGame.staticsVars.SetBulletsSameTime = int(selectedBulltes.get())
        print('Changing Done ', "Your bullets has been set to = %s " % (myGame.staticsVars.SetBulletsSameTime))

    selectedBulltes = IntVar()
    selectedBulltes.set("8")
    selectedBulltes.trace('w',main_spin)

    spin = Spinbox(window, from_=1, to=25, width=5,textvariable=selectedBulltes)
    spin.grid(column=0, row=16)

    pl_ = tk.Label(window, text="----------------------------------------------------------------", fg="#383a39", bg="#a1dbcd", font=("Helvetica", 14))
    pl_.grid(row=17, column=0 , columnspan=2)


    choose = tk.Label(window, text="Choose Easy Mode or Hard ':", fg="#383a39", bg="#a1dbcd", font=("Helvetica", 14))
    choose.grid(row=18, column=0 )

    def EasyMode():
        myGame.staticsVars.EasyToKill = True;
        messagebox.showinfo('Easy Mode ', "Your bullets is now bigger and Enemies can be killed with only 10 hits")


    def HardMode():
        res = messagebox.askyesno('Hard Mode', "So Small Bullets | Enemies are 2 times faster now | 1 enemy needs 100 hits | 3 bullets same time, Are you sure??" );
        myGame.staticsVars.EasyToKill = not (res);
        selectedBulltes.set("3")

    easy_mode = Button(window,text="Easy Mode",command=EasyMode)
    easy_mode.grid(row=19,column=0)

    easy_mode = Button(window,text="Hard Mode",command=HardMode)
    easy_mode.grid(row=19,column=1)

    window.mainloop()


def create_window():
    window = tk.Toplevel(root)



def start_game():
    if (name.get("0.0", 'end-1c') == ""):
        inputName = "Guest"
    else :
        inputName = name.get("0.0", 'end-1c')

    myGame.staticsVars.player_name = inputName

    print("Hello Mr. ",myGame.staticsVars.player_name)
    myGame.myGameFun()
    if(myGame.staticsVars.Finished==True):
        myGame.staticsVars.Finished = False
        if(myGame.staticsVars.score<-150):
            myGame.staticsVars.score = 0


root = Tk()
root.title("Main Menu")
root.geometry("240x300")
root.configure(background="#a1dbcd")
root.wm_iconbitmap('img/Icon.ico')

photo = PhotoImage(file="img/title.gif")
w = Label(root, image=photo)
w.grid(row = 0,column = 0 , columnspan = 2)
# w.pack()

start = Button(root, text="Start the game", command=start_game)
start.grid(row = 1 , column = 0,columnspan= 2)

lblname = Label(root, text="Please Enter your name:", fg="#383a39", bg="#a1dbcd", font=("Helvetica", 16))
lblname.grid(row = 2 , column = 0,columnspan= 2)
name = Text(root,width=15,height=2)

name.grid(row = 3 , column = 0,columnspan= 2)


options = Button(root, text="Go Statistics ", command=goToAnotherFrame)
options.grid(row = 4 , column = 0,columnspan= 2)


options2 = Button(root, text=".. Settings .. ", command=open_settings)
options2.grid(row = 6 , column = 0,columnspan= 2)

def exit():
    res = messagebox.askyesno('Are You Sure?',
                              "Thanks for trying the game Mr. %s " % (str(name.get("0.0", 'end-1c'))));
    if(res):
        quit()
    else :
        print("welcome back ")


Exit = Button(root, text=".. Exit to Desktop .. ", command=exit)
Exit.grid(row = 7 , column = 0,columnspan= 2)



root.mainloop()
