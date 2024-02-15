#IMPORTS------------------------------------------
from PyQt5 import QtCore, QtGui, QtWidgets
from functools import partial
import pandas as pd
import requests

#small variable that allows two parts of the code to communicate inbetween eachother
transmiting = [False,None]
global current_ui

#FUNCTIONS ------------------------------------

def online_download(url,ID):

    with open("supermarket/downloaded_images/"+ID+".jpg", 'wb') as handle:
        response = requests.get(str(url), stream=True)

        if not response.ok:
            print(response)

        for block in response.iter_content(1024):
            if not block:
                break

            handle.write(block)

def re_write_database(current_data):
    #This function adds the desired data to the csv file

    items_dataframe = pd.read_csv("Items.csv")#creates a datafram from the csv file
    new_row_df = pd.DataFrame([current_data], columns=["ID","Name","Ammount", "Description", "ImageURL"])#Makes the data become a new dataframe
    items_dataframe = pd.concat([items_dataframe, new_row_df])    #Combines both dataframes into one final one
    items_dataframe.sort_values("ID", axis=0, ascending=True,inplace=True, na_position='first')#It sorts the dataframe so that it is in ID order
    items_dataframe.to_csv('Items.csv', index=False)#It converts the dataframe back to a csv file and overwrites the old one

def select_item(curr_id):
    #Assigs the current ID to a variable for later use
    curr_id = curr_id[0]
    #Opening the csv file so it can be read
    with open("Items.csv","r") as csvfile:
        #Count variable to look at how far down the item is found in the csv file
        count = 0

        for row in csvfile:
            #For loop that loops through untill the desired ID is found (or not found)
            if row[0:4] == curr_id:
                        return [row,count]
            count += 1
        print("Not found")
        return[None,None]
    
#validation check to makes sure that the inputs are correct when submiting an item, if not, it creates an error window:

def validation_check(item):
        #Validation check for each item inputed when trying to input data:
        #The item list goes as follows: ID, Name, Ammount, description, URL/image directory

        current_id = item[0]
        #sets an item to current ID:
        try:
            #Makes sure that the current ID is in the wanted format, if its not, it will return an error code used to generate an error window
            while current_id[0].isupper() == False or current_id[1:4].isnumeric() == False or len(current_id) != 4:
                return("Error 1:Input ID again, the current input is wrong. The correct format is A001")
        except:
            return("Error 1:Input ID again, the current input is wrong. The correct format is A001")

        current_name = item[1]
        #Simple validation check for the name, just len() of 1 or longer to make sure that the item has a name
        while len(current_name)<1:
            return("Error 2: There must be a name for the item")


        current_ammount = item[2]
        #Validation check to make sure that there is a number bigger than 1 in the items and to know that the number is an integer
        while True:
            try:
                if int(current_ammount) < 0:
                    raise("Less than 0")
                else:
                    break
            except:
                return("Error 3: The Ammount must be a number and greater than 0")

        #The description has to be bigger than 1 since if not there is no description, cant really validate it any further
        current_description = item[3]
        while len(current_description)<1:
            return("Error 4: There must be a description included to keep data integrity")

        #The image URL has to be longer than 1 (so that the program knows there is something there)
        #For testing purposes, this has been changed, but in a final verison this could me made so that only valid images work

        current_url = item[4]
        while len(current_url)<1:
            return("Error 5: Input the URL again, its too short (for testing purposes, any string loger than 1 works)")
        
        #Finally, this checks if the item already exists in the data base by asking the "Select function above"
        if select_item(item) != [None,None]:
            return("Error 6: The ID inputed already exists in the database")


#Function used all throughout the code
def swap_screens(ui):
    current_ui = ui
    current_ui.setupUi(MainWindow)


#START OF THE UI OF THE CODE----------------------------------------------------------

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        #Initialization of the main window (the firs tone that pops up whenever you press run)
        MainWindow.setObjectName("MainWindow")
        #setting the name and size of the window (it can be changed if you want)
        MainWindow.resize(800, 600)
        font = QtGui.QFont()
        font.setFamily("Impact")
        MainWindow.setFont(font)
        MainWindow.setCursor(QtGui.QCursor(QtCore.Qt.ArrowCursor))
        MainWindow.setStyleSheet("background-color: rgb(22, 26, 48);")

        #Here starts the part where every part of the first UI gets inizialized, all of the labels, images, buttons...
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.label_4 = QtWidgets.QLabel(self.centralwidget)
        self.label_4.setGeometry(QtCore.QRect(10, 10, 781, 161))
        font = QtGui.QFont()
        font.setPointSize(48)
        self.label_4.setFont(font)
        self.label_4.setStyleSheet("color: rgb(255, 255, 255);")
        self.label_4.setTextFormat(QtCore.Qt.AutoText)
        self.label_4.setScaledContents(False)
        self.label_4.setAlignment(QtCore.Qt.AlignCenter)
        self.label_4.setWordWrap(False)
        self.label_4.setObjectName("label_4")


        #This is the inizialization for the button of removing items from the database
        self.add_remove_button = QtWidgets.QPushButton(self.centralwidget)
        self.add_remove_button.setEnabled(True)
        self.add_remove_button.setGeometry(QtCore.QRect(30, 240, 211, 211))
        self.add_remove_button.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))

        #Sets the image of the first button fo the UI
        self.add_remove_button.setStyleSheet("background-image : \"supermarket/buttonuis/add_remove button.png\";")
        self.add_remove_button.setText("")
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap("supermarket/buttonuis/add_remove button.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.add_remove_button.setIcon(icon)
        self.add_remove_button.setIconSize(QtCore.QSize(200, 250))
        self.add_remove_button.setObjectName("add_remove_button")

        #makes it so that when the button is clicked, it activates the swap to add remove screen method
        self.add_remove_button.clicked.connect(self.swap_to_add_remove_screen)


        #This is the initialization of the edit button, as seen above
        self.edit_button = QtWidgets.QPushButton(self.centralwidget)
        self.edit_button.setEnabled(True)
        self.edit_button.setGeometry(QtCore.QRect(300, 240, 211, 211))
        self.edit_button.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.edit_button.setStyleSheet("background-image : \"supermarket/buttonuis/edit_button.png\";")
        self.edit_button.setText("")
        icon1 = QtGui.QIcon()
        icon1.addPixmap(QtGui.QPixmap("supermarket/buttonuis/edit_button.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.edit_button.setIcon(icon1)
        self.edit_button.setIconSize(QtCore.QSize(200, 250))
        self.edit_button.setObjectName("edit_button")

        #When the button is clicked, it activates swap to edit screen method
        self.edit_button.clicked.connect(self.swap_to_edit_screen)

        #Same as above two buttons, connects and sends to custom method:
        self.search_button = QtWidgets.QPushButton(self.centralwidget)
        self.search_button.setEnabled(True)
        self.search_button.setGeometry(QtCore.QRect(570, 240, 211, 211))
        self.search_button.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.search_button.setStyleSheet("background-image : \"supermarket/buttonuis/search_button.png\";")
        self.search_button.setText("")

        self.search_button.clicked.connect(self.swap_to_search_screen)

        icon2 = QtGui.QIcon()
        icon2.addPixmap(QtGui.QPixmap("supermarket/buttonuis/search_button.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.search_button.setIcon(icon2)
        self.search_button.setIconSize(QtCore.QSize(200, 250))
        self.search_button.setObjectName("search_button")

        MainWindow.setCentralWidget(self.centralwidget)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    #Boiler plate code that alows pyqt5 to open windows
    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.label_4.setText(_translate("MainWindow", "Supermarket database"))

    #Functions for the buttons mentioned above, could have used partials for this part but static methods are a bit less messy
    @staticmethod
    def swap_to_add_remove_screen(self):
        swap_screens(Ui_add_remove_screen())
    
    @staticmethod
    def swap_to_edit_screen(self):
        swap_screens(Ui_edit_screen())
    
    @staticmethod
    def swap_to_search_screen(self):
        swap_screens(Ui_search_screen())


class Ui_add_remove_screen(object):

    def setupUi(self, add_remove_screen):

        #Function to initialize the add_remove screen (The one that has a plus and a minus)
        add_remove_screen.setObjectName("add_remove_screen")
        add_remove_screen.resize(800, 600)
        font = QtGui.QFont()
        font.setFamily("Impact")
        add_remove_screen.setFont(font)
        add_remove_screen.setCursor(QtGui.QCursor(QtCore.Qt.ArrowCursor))
        add_remove_screen.setStyleSheet("background-color: rgb(22, 26, 48);")
        self.centralwidget = QtWidgets.QWidget(add_remove_screen)
        self.centralwidget.setObjectName("centralwidget")

        #Creation of the add button

        self.add_button = QtWidgets.QPushButton(self.centralwidget)
        self.add_button.setEnabled(True)
        self.add_button.setGeometry(QtCore.QRect(100, 190, 211, 211))
        self.add_button.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.add_button.setStyleSheet("background-image : \"supermarket/buttonuis/add_button.png\";")
        self.add_button.setText("")
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap("supermarket/buttonuis/add_button.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.add_button.setIcon(icon)
        self.add_button.setIconSize(QtCore.QSize(200, 250))
        self.add_button.setObjectName("add_button")

        #Connects to the functions that swap the screen
        self.add_button.clicked.connect(self.swap_to_add_screen)


        #Creation of the remove button, same as above
        self.remove_button = QtWidgets.QPushButton(self.centralwidget)
        self.remove_button.setEnabled(True)
        self.remove_button.setGeometry(QtCore.QRect(500, 190, 211, 211))
        self.remove_button.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.remove_button.setStyleSheet("background-image : \"supermarket/buttonuis/remove button.png\";")
        self.remove_button.setText("")
        icon1 = QtGui.QIcon()
        icon1.addPixmap(QtGui.QPixmap("supermarket/buttonuis/remove button.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.remove_button.setIcon(icon1)
        self.remove_button.setIconSize(QtCore.QSize(200, 250))
        self.remove_button.setObjectName("remove_button")

        self.remove_button.clicked.connect(self.swap_to_remove_screen)


        #Function for the back button that takes you to the main page
        self.back_button = QtWidgets.QPushButton(self.centralwidget)
        self.back_button.setGeometry(QtCore.QRect(10, 10, 91, 41))
        self.back_button.setStyleSheet("color: rgb(255, 255, 255);\n"
"background-color: rgb(170, 0, 0);")
        self.back_button.setObjectName("back_button")

        self.back_button.clicked.connect(self.back_button_clicked)

        add_remove_screen.setCentralWidget(self.centralwidget)
        self.statusbar = QtWidgets.QStatusBar(add_remove_screen)
        self.statusbar.setObjectName("statusbar")
        add_remove_screen.setStatusBar(self.statusbar)

        self.retranslateUi(add_remove_screen)
        QtCore.QMetaObject.connectSlotsByName(add_remove_screen)

    def retranslateUi(self, add_remove_screen):
        _translate = QtCore.QCoreApplication.translate
        add_remove_screen.setWindowTitle(_translate("add_remove_screen", "MainWindow"))
        self.back_button.setText(_translate("add_remove_screen", "<-- Back"))

    #Functions used to swap screens:
    
    @staticmethod
    def swap_to_add_screen(self):
        swap_screens(Ui_add_screen())

    @staticmethod
    def swap_to_remove_screen(self):
        swap_screens(Ui_remove_screen())

    @staticmethod
    def back_button_clicked(self):
        swap_screens(Ui_MainWindow())

class Ui_add_screen(object):

    #This whole class is used as both the adding items screen and the editing screen hence it has both of the functions for it
    def set_up_for_edit(self,id_edited):
        #This functuion replaces the ID that is wanted to be edited with the ID that it is currently editing

        current_df = pd.read_csv("Items.csv")
        #This line creates a dataframe that can be read by the following code

        select_row = current_df[current_df["ID"] == id_edited]
        #Selects the row that is currently being inspected/edited
        print("Select row is:",select_row)
        print("Select row[ID]:",select_row["ID"])

        self.input_id_box.setText(str(select_row["ID"].iloc[0]))
        self.input_name_box.setText(str(select_row["Name"].iloc[0]))
        self.input_ammount_box.setText(str(select_row["Ammount"].iloc[0]))
        self.input_description_box.setPlainText(str(select_row["Description"].iloc[0]))
        self.input_url_box.setText(str(select_row["ImageURL"].iloc[0]))
        
        print("Supermarket image:","supermarket/dowloaded_images/"+str(select_row["ID"].iloc[0]+".jpg"))
        try:
            self.replace_with_url.setPixmap(QtGui.QPixmap("supermarket\\downloaded_images\\" + str(select_row["ID"].iloc[0]) + ".jpg"))
        except:
            print("Image not found")
        #These past 5 lines take the information that has been added to the boxes and sets the data frame with them

        current_df = current_df.drop(current_df[current_df["ID"] == id_edited].index)
        current_df = current_df.reset_index(drop=True)
        #Once that is done, the ID that was previously holding the values for it is removed

        print("Dropped the ID")
        current_df.to_csv("Items.csv", index=False)
        transmiting = [False,None]
        #Then this converts the data frame back to a csv

    def open_error_screen(self,error_code):
        #This function recives an error code and the creates an error pop up acording to the message that was provided

        self.Error_window = QtWidgets.QMainWindow()
        current_ui = Ui_error_screen()
        current_ui.setupUi(self.Error_window)
        current_ui.set_error(error_code)
        self.Error_window.show()

    @staticmethod
    def add_values(ui_instance):
        #This function is the function that adds the values and also makes an error message if the values arent what the program expects
        created_item = [
            ui_instance.input_id_box.text(),
            ui_instance.input_name_box.text(),
            ui_instance.input_ammount_box.text(),
            ui_instance.input_description_box.toPlainText(),
            ui_instance.input_url_box.text()
        ]
        #created_item is a list where the data is taken from the input boxes and stored as text

        validation_check_ans = validation_check(created_item)
        #This line of code sends the list to be validated with the validation check function

        if validation_check_ans == None:
            #then if the response from the validation check is none (meaning there are no errors) it writes the item into the database
            try:
                online_download(str(ui_instance.input_url_box.text()),str(ui_instance.input_id_box.text()))
            except:
                print("The download of the image was unssucessful")
            re_write_database(created_item)
        else:
            #If its not it uses a partial function to create a error message
            open_error_screen_partial = partial(Ui_add_screen.open_error_screen, ui_instance)
            open_error_screen_partial(validation_check_ans)
        
    #Just a small function for when the back button is clicked
    
    @staticmethod
    def back_button_clicked(self):
        swap_screens(Ui_add_remove_screen())


    def setupUi(self, add_screen):
        #Just the part of the code that starts up the add screen
        global transmiting

        add_screen.setObjectName("add_screen")
        add_screen.resize(800, 600)
        font = QtGui.QFont()
        font.setFamily("Impact")
        add_screen.setFont(font)
        add_screen.setCursor(QtGui.QCursor(QtCore.Qt.ArrowCursor))
        add_screen.setStyleSheet("background-color: rgb(22, 26, 48);")
        self.centralwidget = QtWidgets.QWidget(add_screen)
        self.centralwidget.setObjectName("centralwidget")

        self.replace_with_url = QtWidgets.QLabel(self.centralwidget)
        self.replace_with_url.setGeometry(QtCore.QRect(130, 30, 271, 271))
        self.replace_with_url.setText("")
        self.replace_with_url.setPixmap(QtGui.QPixmap("supermarket/buttonuis/no_image.png"))
        self.replace_with_url.setScaledContents(True)
        self.replace_with_url.setObjectName("replace_with_url")
        self.input_ammount_label = QtWidgets.QLabel(self.centralwidget)
        self.input_ammount_label.setGeometry(QtCore.QRect(50, 480, 161, 41))
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(26)
        font.setBold(False)
        font.setWeight(50)

        self.input_ammount_label.setFont(font)
        self.input_ammount_label.setStyleSheet("color: rgb(255, 255, 255);")
        self.input_ammount_label.setObjectName("input_ammount_label")
        self.input_ammount_box = QtWidgets.QLineEdit(self.centralwidget)
        self.input_ammount_box.setGeometry(QtCore.QRect(220, 480, 251, 41))
        font = QtGui.QFont()
        font.setPointSize(26)
        self.input_ammount_box.setFont(font)
        self.input_ammount_box.setAutoFillBackground(False)
        self.input_ammount_box.setStyleSheet("border-color: rgb(255, 255, 255);\n"
"color: rgb(255, 255, 255);")
        self.input_ammount_box.setText("")
        self.input_ammount_box.setObjectName("input_ammount_box")

        self.input_name_label = QtWidgets.QLabel(self.centralwidget)
        self.input_name_label.setGeometry(QtCore.QRect(50, 410, 111, 41))
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(26)
        font.setBold(False)
        font.setWeight(50)
        self.input_name_label.setFont(font)
        self.input_name_label.setStyleSheet("color: rgb(255, 255, 255);")
        self.input_name_label.setObjectName("input_name_label")
        self.input_name_box = QtWidgets.QLineEdit(self.centralwidget)
        self.input_name_box.setGeometry(QtCore.QRect(170, 410, 301, 41))
        font = QtGui.QFont()
        font.setPointSize(26)
        self.input_name_box.setFont(font)
        self.input_name_box.setAutoFillBackground(False)
        self.input_name_box.setStyleSheet("border-color: rgb(255, 255, 255);\n"
"color: rgb(255, 255, 255);")
        self.input_name_box.setText("")
        self.input_name_box.setObjectName("input_name_box")

        self.input_id_label = QtWidgets.QLabel(self.centralwidget)
        self.input_id_label.setGeometry(QtCore.QRect(50, 340, 51, 41))
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(26)
        font.setBold(False)
        font.setWeight(50)
        self.input_id_label.setFont(font)
        self.input_id_label.setStyleSheet("color: rgb(255, 255, 255);")
        self.input_id_label.setObjectName("input_id_label")


        self.input_id_box = QtWidgets.QLineEdit(self.centralwidget)
        self.input_id_box.setGeometry(QtCore.QRect(110, 340, 361, 41))
        font = QtGui.QFont()
        font.setPointSize(26)
        self.input_id_box.setFont(font)
        self.input_id_box.setAutoFillBackground(False)
        self.input_id_box.setStyleSheet("border-color: rgb(255, 255, 255);\n"
"color: rgb(255, 255, 255);")
        self.input_id_box.setText("")
        self.input_id_box.setObjectName("input_id_box")


        self.input_description_label = QtWidgets.QLabel(self.centralwidget)
        self.input_description_label.setGeometry(QtCore.QRect(520, 140, 201, 41))
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(26)
        font.setBold(False)
        font.setWeight(50)
        self.input_description_label.setFont(font)
        self.input_description_label.setStyleSheet("color: rgb(255, 255, 255);")
        self.input_description_label.setObjectName("input_description_label")


        self.input_url_label = QtWidgets.QLabel(self.centralwidget)
        self.input_url_label.setGeometry(QtCore.QRect(410, 30, 321, 41))
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(26)
        font.setBold(False)
        font.setWeight(50)
        self.input_url_label.setFont(font)
        self.input_url_label.setStyleSheet("color: rgb(255, 255, 255);")
        self.input_url_label.setObjectName("input_url_label")


        self.input_url_box = QtWidgets.QLineEdit(self.centralwidget)
        self.input_url_box.setGeometry(QtCore.QRect(410, 90, 361, 41))
        font = QtGui.QFont()
        font.setPointSize(26)
        self.input_url_box.setFont(font)
        self.input_url_box.setAutoFillBackground(False)
        self.input_url_box.setStyleSheet("border-color: rgb(255, 255, 255);\n"
"color: rgb(255, 255, 255);")
        self.input_url_box.setText("")
        self.input_url_box.setObjectName("input_url_box")


        self.input_description_box = QtWidgets.QPlainTextEdit(self.centralwidget)
        self.input_description_box.setGeometry(QtCore.QRect(520, 190, 261, 211))
        font = QtGui.QFont()
        font.setPointSize(22)
        self.input_description_box.setFont(font)
        self.input_description_box.setStyleSheet("color: rgb(255, 255, 255);")
        self.input_description_box.setPlainText("")
        self.input_description_box.setObjectName("input_description_box")
        self.submit_addition = QtWidgets.QPushButton(self.centralwidget)
        self.submit_addition.setGeometry(QtCore.QRect(520, 432, 261, 91))
        font = QtGui.QFont()
        font.setPointSize(24)
        self.submit_addition.setFont(font)
        self.submit_addition.setStyleSheet("color: rgb(255, 255, 255);\n"
"background-color: rgb(0, 170, 0);")
        self.submit_addition.setObjectName("submit_addition")

        #This part of the code connects the button being clicked with the add values function
        self.submit_addition.clicked.connect(partial(Ui_add_screen.add_values, self))

        self.back_button = QtWidgets.QPushButton(self.centralwidget)
        self.back_button.setGeometry(QtCore.QRect(10, 30, 91, 41))
        self.back_button.setStyleSheet("color: rgb(255, 255, 255);\n"
"background-color: rgb(170, 0, 0);")
        self.back_button.setObjectName("back_button")


        #Connects the function to the back button clicked
        self.back_button.clicked.connect(self.back_button_clicked)

        add_screen.setCentralWidget(self.centralwidget)
        self.statusbar = QtWidgets.QStatusBar(add_screen)
        self.statusbar.setObjectName("statusbar")
        add_screen.setStatusBar(self.statusbar)

        self.retranslateUi(add_screen)
        QtCore.QMetaObject.connectSlotsByName(add_screen)

        #This part of the code helps my code communicate with eachother and sends messages between diffrent classes
        if transmiting[0] == True:
            print("Transmitting = True therefore edit code must be recived soon")
            self.set_up_for_edit(transmiting[1])
            transmiting[0] = False

    def retranslateUi(self, add_screen):
        _translate = QtCore.QCoreApplication.translate
        add_screen.setWindowTitle(_translate("add_screen", "MainWindow"))
        self.input_ammount_label.setText(_translate("add_screen", "Ammount:"))
        self.input_name_label.setText(_translate("add_screen", "Name:"))
        self.input_id_label.setText(_translate("add_screen", "ID:"))
        self.input_description_label.setText(_translate("add_screen", "Description:"))
        self.input_url_label.setText(_translate("add_screen", "Input URL for image:"))
        self.submit_addition.setText(_translate("add_screen", "Submit addition"))
        self.back_button.setText(_translate("add_screen", "<-- Back"))



class Ui_remove_screen(object):
    #This is the class that makes the removing 


    def remove_from_df(self):
        #This first function is used to remove items from the database
        current_df = pd.read_csv("Items.csv")
        #creates a dataframe from the csv

        current_deleate_entry = self.input_id_box.text()
        #Looks at the ID that wants to be deleated and converts it into a string variable

        if current_deleate_entry in current_df["ID"].values:
            #Checks if the ID requested to be deleated is inside the current dataframe and if it is, it removes it
            current_df = current_df.drop(current_df[current_df["ID"] == current_deleate_entry].index)
            current_df = current_df.reset_index(drop=True)
        else:
            self.Error_window = QtWidgets.QMainWindow()
            current_ui = Ui_error_screen()
            current_ui.setupUi(self.Error_window)
            current_ui.set_error("Error 7: The ID you wanted to edit wasn't found")
            self.Error_window.show()

        current_df.to_csv("Items.csv", index=False)
        #Converts the dataframe back to csv

    def load_data(self):
        #This function loads data from the csv file into the search table (a table that allow you to search through all items)

        current_df = pd.read_csv("Items.csv")
        #loads the CSV into a dataframe

        row_count = len(current_df)
        #Small variable to hold the length of the current dataframe

        self.search_table.setRowCount(row_count)

        
        #Creates a row table with the amount of rows in the current dataframe
        for row in range(row_count):
            print("Current dataframe id is:",str(current_df["ID"].iloc[0]))
            try:
                item = QtWidgets.QTableWidgetItem()
                item.setIcon(QtGui.QIcon("supermarket\\downloaded_images\\" + str(current_df["ID"].iloc[row]+ ".jpg")))
                self.search_table.setItem(row, 0, item)
            except:
                self.search_table.setItem(row, 0, QtWidgets.QTableWidgetItem(str(current_df.loc[row]["ImageURL"])))

            self.search_table.setItem(row, 1, QtWidgets.QTableWidgetItem(str(current_df.loc[row]["Name"])))
            self.search_table.setItem(row, 2, QtWidgets.QTableWidgetItem(str(current_df.loc[row]["ID"])))
            self.search_table.setItem(row, 3, QtWidgets.QTableWidgetItem(str(current_df.loc[row]["Ammount"])))
            self.search_table.setItem(row, 4, QtWidgets.QTableWidgetItem(str(current_df.loc[row]["Description"])))


    @staticmethod
    def back_button_clicked(self):
        swap_screens(Ui_add_remove_screen())

    def setupUi(self, remove_screen):
        #Initialization of the remove screen
        remove_screen.setObjectName("remove_screen")
        remove_screen.resize(800, 609)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(remove_screen.sizePolicy().hasHeightForWidth())
        remove_screen.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setFamily("Impact")
        remove_screen.setFont(font)
        remove_screen.setCursor(QtGui.QCursor(QtCore.Qt.ArrowCursor))
        remove_screen.setStyleSheet("background-color: rgb(22, 26, 48);")
        self.centralwidget = QtWidgets.QWidget(remove_screen)
        self.centralwidget.setObjectName("centralwidget")
        self.back_button = QtWidgets.QPushButton(self.centralwidget)
        self.back_button.setGeometry(QtCore.QRect(9, 9, 75, 23))
        self.back_button.setStyleSheet("color: rgb(255, 255, 255);\n"
"background-color: rgb(170, 0, 0);")
        self.back_button.setObjectName("back_button")

        self.back_button.clicked.connect(self.back_button_clicked)

        self.search_table = QtWidgets.QTableWidget(self.centralwidget)
        self.search_table.setGeometry(QtCore.QRect(9, 38, 781, 471))
        self.search_table.setStyleSheet("color: rgb(255, 255, 255);\n"
"font: 13pt \"Arial\";\n"
"background-color: rgb(49, 48, 77);\n"
"\n"
"\n"
"alternate-background-color: rgb(127, 255, 120);")
        self.search_table.setLineWidth(1)
        self.search_table.setSizeAdjustPolicy(QtWidgets.QAbstractScrollArea.AdjustIgnored)
        self.search_table.setIconSize(QtCore.QSize(50, 50))
        self.search_table.setVerticalScrollMode(QtWidgets.QAbstractItemView.ScrollPerItem)
        self.search_table.setShowGrid(True)
        self.search_table.setColumnCount(5)
        self.search_table.setObjectName("search_table")
        self.search_table.setRowCount(0)
        item = QtWidgets.QTableWidgetItem()
        item.setTextAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignVCenter)
        brush = QtGui.QBrush(QtGui.QColor(0, 0, 0))
        brush.setStyle(QtCore.Qt.SolidPattern)
        item.setForeground(brush)
        self.search_table.setHorizontalHeaderItem(0, item)
        item = QtWidgets.QTableWidgetItem()
        brush = QtGui.QBrush(QtGui.QColor(0, 0, 0))
        brush.setStyle(QtCore.Qt.SolidPattern)
        item.setForeground(brush)
        self.search_table.setHorizontalHeaderItem(1, item)
        item = QtWidgets.QTableWidgetItem()
        brush = QtGui.QBrush(QtGui.QColor(0, 0, 0))
        brush.setStyle(QtCore.Qt.SolidPattern)
        item.setForeground(brush)
        self.search_table.setHorizontalHeaderItem(2, item)
        item = QtWidgets.QTableWidgetItem()
        brush = QtGui.QBrush(QtGui.QColor(0, 0, 0))
        brush.setStyle(QtCore.Qt.SolidPattern)
        item.setForeground(brush)
        self.search_table.setHorizontalHeaderItem(3, item)
        item = QtWidgets.QTableWidgetItem()
        brush = QtGui.QBrush(QtGui.QColor(0, 0, 0))
        brush.setStyle(QtCore.Qt.SolidPattern)
        item.setForeground(brush)
        self.search_table.setHorizontalHeaderItem(4, item)
        self.search_table.horizontalHeader().setCascadingSectionResizes(False)
        self.search_table.horizontalHeader().setDefaultSectionSize(100)
        self.search_table.horizontalHeader().setMinimumSectionSize(20)
        self.search_table.horizontalHeader().setSortIndicatorShown(False)
        self.search_table.horizontalHeader().setStretchLastSection(True)
        self.search_table.verticalHeader().setCascadingSectionResizes(False)
        self.search_table.verticalHeader().setDefaultSectionSize(100)
        self.search_table.verticalHeader().setMinimumSectionSize(100)
        self.search_table.verticalHeader().setSortIndicatorShown(False)

        #Calls the load data procedure to make the search table have information
        self.load_data()

        self.input_id_box = QtWidgets.QLineEdit(self.centralwidget)
        self.input_id_box.setGeometry(QtCore.QRect(470, 520, 161, 51))
        font = QtGui.QFont()
        font.setPointSize(24)
        self.input_id_box.setFont(font)
        self.input_id_box.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.input_id_box.setStyleSheet("color: rgb(255, 255, 255);")
        self.input_id_box.setObjectName("input_id_box")
        self.input_item_label = QtWidgets.QLabel(self.centralwidget)
        self.input_item_label.setGeometry(QtCore.QRect(10, 520, 451, 51))
        font = QtGui.QFont()
        font.setPointSize(20)
        self.input_item_label.setFont(font)
        self.input_item_label.setStyleSheet("color: rgb(255, 255, 255);")
        self.input_item_label.setObjectName("input_item_label")
        self.submit_button = QtWidgets.QPushButton(self.centralwidget)
        self.submit_button.setGeometry(QtCore.QRect(650, 530, 131, 41))
        self.submit_button.setStyleSheet("color: rgb(255, 255, 255);\n"
"background-color: rgb(0, 170, 0);")
        self.submit_button.setObjectName("submit_button")


        #Connects with the removing ID function above whenever the submit button is clicked
        self.submit_button.clicked.connect(partial(Ui_remove_screen.remove_from_df, self))

        remove_screen.setCentralWidget(self.centralwidget)
        self.statusbar = QtWidgets.QStatusBar(remove_screen)
        self.statusbar.setObjectName("statusbar")
        remove_screen.setStatusBar(self.statusbar)

        self.retranslateUi(remove_screen)
        QtCore.QMetaObject.connectSlotsByName(remove_screen)

    def retranslateUi(self, remove_screen):
        _translate = QtCore.QCoreApplication.translate
        remove_screen.setWindowTitle(_translate("remove_screen", "MainWindow"))
        self.back_button.setText(_translate("remove_screen", "<-- Back"))
        self.search_table.setSortingEnabled(False)
        item = self.search_table.horizontalHeaderItem(0)
        item.setText(_translate("remove_screen", "Picture"))
        item = self.search_table.horizontalHeaderItem(1)
        item.setText(_translate("remove_screen", "Name"))
        item = self.search_table.horizontalHeaderItem(2)
        item.setText(_translate("remove_screen", "ID"))
        item = self.search_table.horizontalHeaderItem(3)
        item.setText(_translate("remove_screen", "Ammount"))
        item = self.search_table.horizontalHeaderItem(4)
        item.setText(_translate("remove_screen", "Description"))
        self.input_id_box.setText(_translate("remove_screen", ""))
        self.input_item_label.setText(_translate("remove_screen", "Input ID of item you want to remove:"))
        self.submit_button.setText(_translate("remove_screen", "Submit"))


class Ui_search_screen(object):

    #Same load function as in the previous class, just loads all of the information from the csv file into the search table
    def load_data(self):
        current_df = pd.read_csv("Items.csv")
        row_count = len(current_df)
        self.search_table.setRowCount(row_count)

        for row in range(row_count):
            try:
                item = QtWidgets.QTableWidgetItem()
                item.setIcon(QtGui.QIcon("supermarket\\downloaded_images\\" + str(current_df["ID"].iloc[row]+ ".jpg")))
                self.search_table.setItem(row, 0, item)
            except:
                self.search_table.setItem(row, 0, QtWidgets.QTableWidgetItem(str(current_df.loc[row]["ImageURL"])))
            self.search_table.setItem(row, 1, QtWidgets.QTableWidgetItem(str(current_df.loc[row]["Name"])))
            self.search_table.setItem(row, 2, QtWidgets.QTableWidgetItem(str(current_df.loc[row]["ID"])))
            self.search_table.setItem(row, 3, QtWidgets.QTableWidgetItem(str(current_df.loc[row]["Ammount"])))
            self.search_table.setItem(row, 4, QtWidgets.QTableWidgetItem(str(current_df.loc[row]["Description"])))

    @staticmethod
    def back_button_clicked(self):
        swap_screens(Ui_MainWindow())

    def setupUi(self, search_screen):
        search_screen.setObjectName("search_screen")
        search_screen.resize(800, 609)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(search_screen.sizePolicy().hasHeightForWidth())
        search_screen.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setFamily("Impact")
        search_screen.setFont(font)
        search_screen.setCursor(QtGui.QCursor(QtCore.Qt.ArrowCursor))
        search_screen.setStyleSheet("background-color: rgb(22, 26, 48);")
        self.centralwidget = QtWidgets.QWidget(search_screen)
        self.centralwidget.setObjectName("centralwidget")
        self.back_button = QtWidgets.QPushButton(self.centralwidget)
        self.back_button.setGeometry(QtCore.QRect(9, 9, 75, 23))
        self.back_button.setStyleSheet("color: rgb(255, 255, 255);\n"
"background-color: rgb(170, 0, 0);")
        self.back_button.setObjectName("back_button")

        self.back_button.clicked.connect(self.back_button_clicked)

        self.search_table = QtWidgets.QTableWidget(self.centralwidget)
        self.search_table.setGeometry(QtCore.QRect(9, 38, 781, 471))
        self.search_table.setStyleSheet("color: rgb(255, 255, 255);\n"
"font: 13pt \"Arial\";\n"
"background-color: rgb(49, 48, 77);\n"
"\n"
"\n"
"alternate-background-color: rgb(127, 255, 120);")
        self.search_table.setLineWidth(1)
        self.search_table.setSizeAdjustPolicy(QtWidgets.QAbstractScrollArea.AdjustIgnored)
        self.search_table.setIconSize(QtCore.QSize(50, 50))
        self.search_table.setVerticalScrollMode(QtWidgets.QAbstractItemView.ScrollPerItem)
        self.search_table.setShowGrid(True)
        self.search_table.setColumnCount(5)
        self.search_table.setObjectName("search_table")
        self.search_table.setRowCount(0)
        item = QtWidgets.QTableWidgetItem()
        item.setTextAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignVCenter)
        brush = QtGui.QBrush(QtGui.QColor(0, 0, 0))
        brush.setStyle(QtCore.Qt.SolidPattern)
        item.setForeground(brush)
        self.search_table.setHorizontalHeaderItem(0, item)
        item = QtWidgets.QTableWidgetItem()
        brush = QtGui.QBrush(QtGui.QColor(0, 0, 0))
        brush.setStyle(QtCore.Qt.SolidPattern)
        item.setForeground(brush)
        self.search_table.setHorizontalHeaderItem(1, item)
        item = QtWidgets.QTableWidgetItem()
        brush = QtGui.QBrush(QtGui.QColor(0, 0, 0))
        brush.setStyle(QtCore.Qt.SolidPattern)
        item.setForeground(brush)
        self.search_table.setHorizontalHeaderItem(2, item)
        item = QtWidgets.QTableWidgetItem()
        brush = QtGui.QBrush(QtGui.QColor(0, 0, 0))
        brush.setStyle(QtCore.Qt.SolidPattern)
        item.setForeground(brush)
        self.search_table.setHorizontalHeaderItem(3, item)
        item = QtWidgets.QTableWidgetItem()
        brush = QtGui.QBrush(QtGui.QColor(0, 0, 0))
        brush.setStyle(QtCore.Qt.SolidPattern)
        item.setForeground(brush)
        self.search_table.setHorizontalHeaderItem(4, item)
        self.search_table.horizontalHeader().setCascadingSectionResizes(False)
        self.search_table.horizontalHeader().setDefaultSectionSize(100)
        self.search_table.horizontalHeader().setMinimumSectionSize(20)
        self.search_table.horizontalHeader().setSortIndicatorShown(False)
        self.search_table.horizontalHeader().setStretchLastSection(True)
        self.search_table.verticalHeader().setCascadingSectionResizes(False)
        self.search_table.verticalHeader().setDefaultSectionSize(100)
        self.search_table.verticalHeader().setMinimumSectionSize(100)
        self.search_table.verticalHeader().setSortIndicatorShown(False)

        self.load_data()

        search_screen.setCentralWidget(self.centralwidget)
        self.statusbar = QtWidgets.QStatusBar(search_screen)
        self.statusbar.setObjectName("statusbar")
        search_screen.setStatusBar(self.statusbar)

        self.retranslateUi(search_screen)
        QtCore.QMetaObject.connectSlotsByName(search_screen)

    def retranslateUi(self, search_screen):
        _translate = QtCore.QCoreApplication.translate
        search_screen.setWindowTitle(_translate("search_screen", "MainWindow"))
        self.back_button.setText(_translate("search_screen", "<-- Back"))
        self.search_table.setSortingEnabled(False)
        item = self.search_table.horizontalHeaderItem(0)
        item.setText(_translate("search_screen", "Picture"))
        item = self.search_table.horizontalHeaderItem(1)
        item.setText(_translate("search_screen", "Name"))
        item = self.search_table.horizontalHeaderItem(2)
        item.setText(_translate("search_screen", "ID"))
        item = self.search_table.horizontalHeaderItem(3)
        item.setText(_translate("search_screen", "Ammount"))
        item = self.search_table.horizontalHeaderItem(4)
        item.setText(_translate("search_screen", "Description"))

class Ui_edit_screen(object):


    def edit_entry(self):
        #This function is used to know what ID is going to be edited and requests the edit of the ID
        global transmiting

        current_edit_entry = self.input_id_box.text()

        #Checks if the ID is inside the CSV if its not it brings up an error message
        df = pd.read_csv("Items.csv")
        if current_edit_entry in df["ID"].values:
            #This is set to true so that it can communicate with the add_screen ui
            transmiting = [True,current_edit_entry]
            swap_screens(Ui_add_screen())
        else:
            #Creates an error window if the ID wasnt found
            self.Error_window = QtWidgets.QMainWindow()
            current_ui = Ui_error_screen()
            current_ui.setupUi(self.Error_window)
            current_ui.set_error("Error 7: The ID you wanted to edit wasn't found")
            self.Error_window.show()

    #Same function as above classes, used to set up the search table
    def load_data(self):
        current_df = pd.read_csv("Items.csv")
        row_count = len(current_df)
        self.search_table.setRowCount(row_count)

        for row in range(row_count):
            try:
                item = QtWidgets.QTableWidgetItem()
                item.setIcon(QtGui.QIcon("supermarket\\downloaded_images\\" + str(current_df["ID"].iloc[row]+ ".jpg")))
                self.search_table.setItem(row, 0, item)
            except:
                self.search_table.setItem(row, 0, QtWidgets.QTableWidgetItem(str(current_df.loc[row]["ImageURL"])))

            self.search_table.setItem(row, 1, QtWidgets.QTableWidgetItem(str(current_df.loc[row]["Name"])))
            self.search_table.setItem(row, 2, QtWidgets.QTableWidgetItem(str(current_df.loc[row]["ID"])))
            self.search_table.setItem(row, 3, QtWidgets.QTableWidgetItem(str(current_df.loc[row]["Ammount"])))
            self.search_table.setItem(row, 4, QtWidgets.QTableWidgetItem(str(current_df.loc[row]["Description"])))

    @staticmethod
    def back_button_clicked(self):
        swap_screens(Ui_MainWindow())

    def setupUi(self, edit_screen):
        edit_screen.setObjectName("edit_screen")
        edit_screen.resize(800, 609)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(edit_screen.sizePolicy().hasHeightForWidth())
        edit_screen.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setFamily("Impact")
        edit_screen.setFont(font)
        edit_screen.setCursor(QtGui.QCursor(QtCore.Qt.ArrowCursor))
        edit_screen.setStyleSheet("background-color: rgb(22, 26, 48);")
        self.centralwidget = QtWidgets.QWidget(edit_screen)
        self.centralwidget.setObjectName("centralwidget")
        self.back_button = QtWidgets.QPushButton(self.centralwidget)
        self.back_button.setGeometry(QtCore.QRect(9, 9, 75, 23))
        self.back_button.setStyleSheet("color: rgb(255, 255, 255);\n"
"background-color: rgb(170, 0, 0);")
        self.back_button.setObjectName("back_button")

        self.back_button.clicked.connect(self.back_button_clicked)

        self.search_table = QtWidgets.QTableWidget(self.centralwidget)
        self.search_table.setGeometry(QtCore.QRect(9, 38, 781, 471))
        self.search_table.setStyleSheet("color: rgb(255, 255, 255);\n"
"font: 13pt \"Arial\";\n"
"background-color: rgb(49, 48, 77);\n"
"\n"
"\n"
"alternate-background-color: rgb(127, 255, 120);")
        self.search_table.setLineWidth(1)
        self.search_table.setSizeAdjustPolicy(QtWidgets.QAbstractScrollArea.AdjustIgnored)
        self.search_table.setIconSize(QtCore.QSize(50, 50))
        self.search_table.setVerticalScrollMode(QtWidgets.QAbstractItemView.ScrollPerItem)
        self.search_table.setShowGrid(True)
        self.search_table.setColumnCount(5)
        self.search_table.setObjectName("search_table")
        self.search_table.setRowCount(0)
        item = QtWidgets.QTableWidgetItem()
        item.setTextAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignVCenter)
        brush = QtGui.QBrush(QtGui.QColor(0, 0, 0))
        brush.setStyle(QtCore.Qt.SolidPattern)
        item.setForeground(brush)
        self.search_table.setHorizontalHeaderItem(0, item)
        item = QtWidgets.QTableWidgetItem()
        brush = QtGui.QBrush(QtGui.QColor(0, 0, 0))
        brush.setStyle(QtCore.Qt.SolidPattern)
        item.setForeground(brush)
        self.search_table.setHorizontalHeaderItem(1, item)
        item = QtWidgets.QTableWidgetItem()
        brush = QtGui.QBrush(QtGui.QColor(0, 0, 0))
        brush.setStyle(QtCore.Qt.SolidPattern)
        item.setForeground(brush)
        self.search_table.setHorizontalHeaderItem(2, item)
        item = QtWidgets.QTableWidgetItem()
        brush = QtGui.QBrush(QtGui.QColor(0, 0, 0))
        brush.setStyle(QtCore.Qt.SolidPattern)
        item.setForeground(brush)
        self.search_table.setHorizontalHeaderItem(3, item)
        item = QtWidgets.QTableWidgetItem()
        brush = QtGui.QBrush(QtGui.QColor(0, 0, 0))
        brush.setStyle(QtCore.Qt.SolidPattern)
        item.setForeground(brush)
        self.search_table.setHorizontalHeaderItem(4, item)
        self.search_table.horizontalHeader().setCascadingSectionResizes(False)
        self.search_table.horizontalHeader().setDefaultSectionSize(100)
        self.search_table.horizontalHeader().setMinimumSectionSize(20)
        self.search_table.horizontalHeader().setSortIndicatorShown(False)
        self.search_table.horizontalHeader().setStretchLastSection(True)
        self.search_table.verticalHeader().setCascadingSectionResizes(False)
        self.search_table.verticalHeader().setDefaultSectionSize(100)
        self.search_table.verticalHeader().setMinimumSectionSize(100)
        self.search_table.verticalHeader().setSortIndicatorShown(False)

        self.load_data()

        self.input_id_box = QtWidgets.QLineEdit(self.centralwidget)
        self.input_id_box.setGeometry(QtCore.QRect(430, 520, 201, 51))
        font = QtGui.QFont()
        font.setPointSize(24)
        self.input_id_box.setFont(font)
        self.input_id_box.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.input_id_box.setStyleSheet("color: rgb(255, 255, 255);")
        self.input_id_box.setObjectName("input_id_box")
        self.input_item_label = QtWidgets.QLabel(self.centralwidget)
        self.input_item_label.setGeometry(QtCore.QRect(10, 520, 411, 51))
        font = QtGui.QFont()
        font.setPointSize(20)
        self.input_item_label.setFont(font)
        self.input_item_label.setStyleSheet("color: rgb(255, 255, 255);")
        self.input_item_label.setObjectName("input_item_label")
        self.submit_button = QtWidgets.QPushButton(self.centralwidget)
        self.submit_button.setGeometry(QtCore.QRect(650, 530, 131, 41))
        self.submit_button.setStyleSheet("color: rgb(255, 255, 255);\n"
"background-color: rgb(0, 170, 0);")
        self.submit_button.setObjectName("submit_button")

        self.submit_button.clicked.connect(partial(Ui_edit_screen.edit_entry, self))

        edit_screen.setCentralWidget(self.centralwidget)
        self.statusbar = QtWidgets.QStatusBar(edit_screen)
        self.statusbar.setObjectName("statusbar")
        edit_screen.setStatusBar(self.statusbar)

        self.retranslateUi(edit_screen)
        QtCore.QMetaObject.connectSlotsByName(edit_screen)

    def retranslateUi(self, edit_screen):
        _translate = QtCore.QCoreApplication.translate
        edit_screen.setWindowTitle(_translate("edit_screen", "MainWindow"))
        self.back_button.setText(_translate("edit_screen", "<-- Back"))
        self.search_table.setSortingEnabled(False)
        item = self.search_table.horizontalHeaderItem(0)
        item.setText(_translate("edit_screen", "Picture"))
        item = self.search_table.horizontalHeaderItem(1)
        item.setText(_translate("edit_screen", "Name"))
        item = self.search_table.horizontalHeaderItem(2)
        item.setText(_translate("edit_screen", "ID"))
        item = self.search_table.horizontalHeaderItem(3)
        item.setText(_translate("edit_screen", "Ammount"))
        item = self.search_table.horizontalHeaderItem(4)
        item.setText(_translate("edit_screen", "Description"))
        self.input_id_box.setText(_translate("edit_screen", ""))
        self.input_item_label.setText(_translate("edit_screen", "Input ID of item you want to edit:"))
        self.submit_button.setText(_translate("edit_screen", "Submit"))

class Ui_error_screen(object):

    def set_error(self,error_code):
        #Sets up an error window and also reports the error to the terminal for debuggin porpouses
        print("The error code has been reached", error_code)
        self.textBrowser.setPlainText(error_code)

    def setupUi(self, error_screen):
        error_screen.setObjectName("error_screen")
        error_screen.resize(563, 332)
        font = QtGui.QFont()
        font.setFamily("Impact")
        font.setPointSize(14)
        error_screen.setFont(font)
        error_screen.setCursor(QtGui.QCursor(QtCore.Qt.ArrowCursor))
        error_screen.setStyleSheet("background-color: rgb(22, 26, 48);")
        self.centralwidget = QtWidgets.QWidget(error_screen)
        self.centralwidget.setObjectName("centralwidget")
        self.gridLayout = QtWidgets.QGridLayout(self.centralwidget)
        self.gridLayout.setObjectName("gridLayout")
        self.label = QtWidgets.QLabel(self.centralwidget)
        font = QtGui.QFont()
        font.setPointSize(20)
        self.label.setFont(font)
        self.label.setStyleSheet("color: rgb(255, 0, 0);")
        self.label.setObjectName("label")
        self.gridLayout.addWidget(self.label, 0, 0, 1, 1)
        self.textBrowser = QtWidgets.QTextBrowser(self.centralwidget)
        font = QtGui.QFont()
        font.setPointSize(12)
        self.textBrowser.setFont(font)
        self.textBrowser.setStyleSheet("color: rgb(255, 255, 255);")
        self.textBrowser.setObjectName("textBrowser")
        self.gridLayout.addWidget(self.textBrowser, 1, 0, 1, 1)
        error_screen.setCentralWidget(self.centralwidget)
        self.statusbar = QtWidgets.QStatusBar(error_screen)
        self.statusbar.setObjectName("statusbar")
        error_screen.setStatusBar(self.statusbar)

        self.retranslateUi(error_screen)
        QtCore.QMetaObject.connectSlotsByName(error_screen)

    def retranslateUi(self, error_screen):
        _translate = QtCore.QCoreApplication.translate
        error_screen.setWindowTitle(_translate("error_screen", "MainWindow"))
        self.label.setText(_translate("error_screen", "There has been an error!"))
        self.textBrowser.setHtml(_translate("error_screen", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'MS Shell Dlg 2\'; font-size:12pt; font-weight:400; font-style:normal;\">\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:8.25pt;\">PLACE_HOLDER ERROR (if you are seeing this, something has gone helllaaaaa wrong)</span></p></body></html>"))

#Boiler plate code that starts PYQT5
if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    current_ui = Ui_MainWindow()
    current_ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())