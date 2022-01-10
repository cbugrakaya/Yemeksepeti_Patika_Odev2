import pathlib
import csv
import pandas as pd
import json
import datetime

class FileTool():
    
    def __init__(self, path, *args):
        """
        """
        self.path = path
        self.fields = list(*args)

        # get extension of the file
        extension =  pathlib.Path(self.path).suffix 

        if self.fields == []:
            if extension == ".csv" or extension == ".CSV":
                # get the titles of the file
                with open(self.path, 'r') as ft:
                    header = ft.readline() # read only first line; returns string
                    header_list = header.split(',') # returns list

                self.fields = [''.join(e for e in string if e.isalnum()) for string in header_list]
                
            elif extension == ".json" or extension == ".JSON":
                df_file = pd.read_json(self.path)
                self.fields = df_file.columns.values
        
            else:
                raise  Exception("This data type is not a valid data type")
        
    
    def show_first_five(self):
        """
        Show first five row of the file
        """
        extension =  pathlib.Path(self.path).suffix 
        if extension == ".csv" or extension == ".CSV":
            df_file = pd.read_csv(self.path)
            print(df_file.head())
        elif extension == ".json" or extension == ".JSON":
            df_file = pd.read_json(self.path)
            print(df_file.head())
        elif extension == ".txt" or extension == ".TXT":
            df_file = pd.read_csv('output_list.txt', header = None)
            print(df_file.head())
        else:
            raise Exception("This data type is not a valid data type")

    def menu(self):
        """
        Menu for Terminal
        """
        run = 1
     

        while run:
            print("*************")
            print("Press 1 To Search ")
            print("Press 2 To Delete")
            print("Press 3 To Add")
            print("Press 4 To Update")
            print("Press 5 To Add file(json,cvs) to the file")
            print("Press 6 To export one line of the file (json)")
            print("Press 7 To print the file")
            print("Press 0 To exit")
            print("*************")
            user_input = int(input("Enter your choice: "))

            if user_input == 1:
                self.search_in_file()
            elif user_input == 2:
                self.delete_in_file()
            elif user_input == 3:
                self.add_in_file()
            elif user_input == 4:
                self.update_in_file()
            elif user_input == 5:
                filepath = input("Enter file path of the other file : ")
                self.file_to_file(filepath)
            elif user_input == 6:
                self.export_one_json()
            elif user_input == 7:
                self.show_file()
            elif user_input == 0:
                run = 0
                break
            else:
                raise Exception("This is not a valid input.")
        
        
    def search_in_file(self):
        """
            Search in the file with Column name and value that want to look
        """
        extension =  pathlib.Path(self.path).suffix 
        if extension == ".csv" or extension == ".CSV":
            # Show first 5 row
            df_file = pd.read_csv(self.path)
            print(df_file.head())
        
            print("**************")
            value = input("Enter the value to search: ")
            column_name = input("Enter the column name: ")

            if len(df_file[df_file[column_name] == value]) == 0:
                float_value = float(value)
                print(df_file[df_file[column_name] == float_value])
            else:
                print(df_file[df_file[column_name] == value])

        elif extension == ".json" or extension == ".JSON":
            # Show first 5 row
            df_file = pd.read_json(self.path)
            print(df_file.head())
        
            print("**************")
            value = input("Enter the value to search: ")
            column_name = input("Enter the column name: ")

            if len(df_file[df_file[column_name] == value]) == 0:
                float_value = float(value)
                print(df_file[df_file[column_name] == float_value])
            else:
                print(df_file[df_file[column_name] == value])
        else:
            raise Exception("This data type is not a valid data type")

      
    def delete_in_file(self):
        """
            Delete any row with row_number
        """
        # Show first 5 row
        FileTool.show_first_five(self)

        row_number = int(input("Enter the line(row) you want to delete : "))
        with open(self.path, "r+") as f:
            lines = f.readlines() 
            del(lines[row_number])
            with open(self.path,"w") as new_f:
                for line in lines:        
                    new_f.write(line)

    def add_in_file(self):
        """
            Add a new row to the file
        """
        # Show first five row
        FileTool.show_first_five(self)

        if len(self.fields) > 0:
            extension =  pathlib.Path(self.path).suffix 
            if extension == ".csv" or extension == ".CSV":
                print("Enter your values... ")
                input_values = [input("{} : ".format(i)) for i in self.fields]

                with open(self.path,"a") as f:
                    writer_object = csv.writer(f)
                    writer_object.writerow(input_values)
                    
                df_list = pd.read_csv(self.path)
                print(df_list.iloc[-5:,])

            elif extension == ".json" or extension == ".JSON":
                print("Enter your values... ")
                input_val_dict = {i:input("{} :".format(i)) for i in self.fields}

                with open(self.path,"r+") as f:
                    data = json.load(f)
                    data.append(input_val_dict)
                    f.seek(0)
                    json.dump(data,f,indent=4)
                   
                    
                df_list = pd.read_json(self.path)
                print(df_list.iloc[-5:,])

        else:
            
            raise Exception("Labels are not correct! ")

    def update_in_file(self):
        """
            Update any value in the file  
        """
        FileTool.show_first_five(self)

        if len(self.fields) > 0:
            extension =  pathlib.Path(self.path).suffix 
            if extension == ".csv" or extension == ".CSV":
                df_file = pd.read_csv(self.path)

                new_value = input("Enter new value : ")
                row = float(input("Enter the row to change : "))
                column_name = input("Enter the column name : ")

                if df_file.loc[row,column_name] is not None:
                    df_file.loc[row,column_name] = new_value
                    print(df_file.loc[row:row+5])
                    df_file.to_csv(self.path, index=False)
                else:
                    raise  Exception("This value is not valid.")
           
            elif extension == ".json" or extension == ".JSON":
                df_file = pd.read_json(self.path)

                new_value = input("Enter new value : ")
                row = float(input("Enter the row to change : "))
                column_name = input("Enter the column name : ")

                if df_file.loc[row,column_name] is not None:
                    df_file.loc[row,column_name] = new_value
                    print(df_file.loc[row:row+5])
                    df_file.to_json(self.path)
                else:
                    raise  Exception("This value is not valid.")
        else:
            raise  Exception("Labels are not corret !")
    
    def file_to_file(self,other_file_path = ""):
        """
            Merge two file
        """
        other_file_path = pathlib.Path(other_file_path)
        first_extension =  pathlib.Path(self.path).suffix 
        second_extension = pathlib.Path(other_file_path).suffix

        if other_file_path != "":
            if first_extension == second_extension:
                if first_extension == ".csv":
                    with open(other_file_path,"r",encoding="utf-8") as f:
                        lines_list = f.readlines()
                        with open(self.path,"a+",encoding="utf-8") as sfile:
                                sfile.writelines(lines_list)     
                elif first_extension == ".json":
                    pass
                    # a = json.loads(self.path)
                    # b = json.loads(other_file_path)
                    # list_dict = dict(a.items() + b.items())

                    # # To get unique name for each file
                    # suffix = datetime.datetime.now().strftime("%y%m%d_%H%M%S")
                    # filename = "_".join(["file", suffix])
                    
                    # with open(filename+".json","w+",encoding="utf-8") as f:
                    #      f.write("\n".join(str(item) for item in list_dict))
                else:
                    raise Exception("This data type is not a valid data type")      
            else:
                raise Exception("Different Extension! ")
        else:
            raise Exception("Other file path is empty! ")


    def export_one_json(self):
        """
        Export one row of the file as Json file
        """
        extension =  pathlib.Path(self.path).suffix 
        if extension == ".csv" or extension == ".CSV":
            # Show first 5 row
            df_file = pd.read_csv(self.path)
            print(df_file.head())
            total_row = df_file[df_file.columns[0]].count()
        
            print("**************")
            row = int(input("Enter the row to export: "))
            
            if row > total_row:
                raise Exception("This row number is not valid.")
            else:
                # To get unique name for each file
                suffix = datetime.datetime.now().strftime("%y%m%d_%H%M%S")
                filename = "_".join(["file", suffix])
                df_file.loc[row].to_json(filename+".json")
                
           
        elif extension == ".json" or extension == ".JSON":
            # Show first 5 row
            df_file = pd.read_json(self.path)
            print(df_file.head())
            total_row = df_file[df_file.columns[0]].count()

            print("**************")
            row = int(input("Enter the row to export: "))
            
            if row > total_row:
                raise Exception("This row number is not valid.")
            else:
                # To get unique name for each file
                suffix = datetime.datetime.now().strftime("%y%m%d_%H%M%S")
                filename = "_".join(["file", suffix])
                df_file.loc[row].to_json(filename+".json")

        else:
            raise Exception("This data type is not a valid data type")
  
    
    def show_file(self):
        """
            Show the file data 
        """
        
        
        extension =  pathlib.Path(self.path).suffix 
        if extension == ".csv" or extension == ".CSV":
            # Show first 5 row
            df_file = pd.read_csv(self.path)
            with pd.option_context('display.max_rows', None, 'display.max_columns', None):  # more options can be specified also
                print(df_file)

           
        elif extension == ".json" or extension == ".JSON":
            # Show first 5 row
            df_file = pd.read_json(self.path)
            with pd.option_context('display.max_rows', None, 'display.max_columns', None):  # more options can be specified also
                print(df_file)

        else:
            raise Exception("This data type is not a valid data type")
  
        


deneme = FileTool("iris.json")
deneme.menu()