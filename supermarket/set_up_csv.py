
## THIS PY FILE IS ONLY MEANT TO BE USED TO RESET THE WHOLE DATABASE, DONT TOUCH UNLESS YOU ARE GOING TO
import pandas as pd

print("Do you want to reset the database to blank or add some predetermined test data?")

choice = input("Blank or Predetermined?")
while choice not in ["Blank","Predetermined"]:
    print("Not a valid input")
    choice = input("Blank or Predetermined?")

print("Final choice is", choice)

if choice == "Blank":
    print("reseting all of the database to blank")
    cols = ["ID","Name","Ammount", "Description","ImageURL"]
    data=[]

    items_df = pd.DataFrame(data, index = range(len(data)), columns = cols)
    print(items_df)
    items_df.to_csv('Items.csv', index=False)
else:
    print("Putting some predetermined data into the database")
    df = pd.read_csv("predetermined_data.csv")
    df.to_csv("Items.csv", index=False)
    print(df)

