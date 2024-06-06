import pandas as pd 
import matplotlib.pyplot as plt
import tkinter as tk 
from tkinter import ttk
df = pd.read_csv('netflix_titles.csv') #load data

class Pandas_Matplotlib_examples_CSV():
    def __init__(self):
        df['date_added'] = pd.to_datetime(df['date_added'], format='%B %d, %Y', errors='coerce') #convert to datetime
        #errors='coerce' : NaN (Not A Number) if error occures
        self.top_content_types = df['type'].value_counts().head(10)
        self.top_contents = df['listed_in'].value_counts().head(10)
        self.top_countries = df['country'].value_counts().head(10)
        self.top_dates = df['date_added'].value_counts().head(10)
        
        df['month_added'] = pd.to_datetime(df['date_added']).dt.month #get months
        df.dropna(subset=['month_added'], inplace=True) #remove NaN
        self.top_months = df['month_added'].astype(int).value_counts().head(10) #months with digit
        month_names = ["January","February","March","April","May","June","July","August","September","October","November","December"]
        self.top_months.index = self.top_months.index.map(lambda x: month_names[int(x)-1]) #months with string
        
        df['year_added'] = pd.to_datetime(df['date_added']).dt.year #get years
        df.dropna(subset=['year_added'], inplace=True) #remove NaN
        self.top_years = df['year_added'].astype(int).value_counts().head() #years with digit
        
        self.top_directors = df['director'].value_counts().head(10)
        
        all_cast = df['cast'].str.split(',', expand=True).stack()  #cast data to one row
        all_cast = all_cast.str.strip()  #clear empty
        self.top_actors = all_cast.value_counts().head(10)
    def launcher(self):
        global root
        root = tk.Tk() #create and set window
        root.geometry("450x400")
        root.title("Pandas-Matplotlib-Examples")
        
        #tkinter window buttons
        tk.Button(text="show/hide data",command=lambda:self.load_csv()).pack(anchor="center")
        
        tk.Button(text="top contents & top content types",command=lambda:self.analyze_top_contents_and_content_types()).pack(side=tk.TOP,anchor="n",padx=25,pady=25)
        tk.Button(text="top countries & top contents",command=lambda:self.analyze_top_countries_with_most_contents()).pack(side=tk.TOP,anchor="n",padx=25,pady=25)
        tk.Button(text="top content release months & years",command=lambda:self.analyze_top_content_release_months_and_years()).pack(side=tk.BOTTOM,anchor="s",padx=25,pady=25)
        tk.Button(text="top actors & directors",command=lambda:self.analyze_top_directors_and_actors()).pack(side=tk.BOTTOM,anchor="s",padx=25,pady=25)
        
        root.mainloop()
    
    def load_csv(self):
        file_path = "netflix_titles.csv" 
        df = pd.read_csv(file_path)
        self.display_data(df)
    
    def display_data(self,df): #in a new window
        global frame
        try: frame.destroy()
        except:
            frame = tk.Tk() #create and set new window
            frame.geometry("750x600")
            columns = ["#1", "#2", "#3", "#4", "#5", "#6", "#7", "#8", "#9", "#10", "#11", "#12"] 
            treeview = ttk.Treeview(frame, columns=columns, show="headings") 
            treeview.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)
            #for displaying .csv in tkinter
            for i, column in enumerate(df.columns):
                treeview.heading(f"#{i+1}", text=column)
                treeview.column(f"#{i+1}", anchor="w")

            for index, row in df.iterrows():
                treeview.insert("", "end", values=list(row))

    def analyze_top_contents_and_content_types(self): #PIE-BAR GRAPH
        plt.figure(figsize=(20,9)) #set window size
        
        plt.subplot(2,2,1) #row, column, index
        plt.title('TOP CONTENT TYPES')
        plt.pie(self.top_content_types.values, labels=self.top_content_types.index, autopct='%1.1f%%')
        #autopct is for readability
        plt.subplot(2,2,2)
        plt.title('TOP 10 CONTENTS')
        plt.pie(self.top_contents.values, labels=self.top_contents.index, autopct='%1.1f%%')
        
        plt.subplot(2,2,3)
        plt.bar(self.top_content_types.index, self.top_content_types.values)
        plt.title('TOP CONTENT TYPES')
        plt.xlabel('CONTENT TYPES')
        plt.ylabel('NUMBER OF CONTENT')
        
        plt.subplot(2,2,4)
        plt.bar(self.top_contents.index, self.top_contents.values)
        plt.title('TOP 10 CONTENTS')
        plt.xlabel('CONTENTS')
        plt.ylabel('NUMBER OF CONTENT')
        plt.xticks(rotation=25, ha='right') #rotate texts for readability
        
        plt.tight_layout() #prevent overlapping
        plt.show()

    def analyze_top_countries_with_most_contents(self): #PIE-LINE-BAR GRAPH
        plt.figure(figsize=(20,9))
        
        plt.subplot(1,3,1)
        plt.title('TOP 10 COUNTRIES WITH MOST CONTENTS')
        plt.pie(self.top_countries.values,labels=self.top_countries.index,autopct='%1.1f%%')
        
        _top_countries_names = self.top_countries.index
        reversed_top_countries_names = _top_countries_names[::-1] #reversing for displaying in graph
        _top_countries_number = self.top_countries.values
        reversed_top_countries_number = _top_countries_number[::-1] #reversing for displaying in graph
        plt.subplot(1,3,2)
        plt.title('TOP 10 COUNTRIES WITH MOST CONTENTS')
        plt.plot(reversed_top_countries_names, reversed_top_countries_number)
        plt.xlabel('COUNTRY')
        plt.ylabel('NUMBER OF CONTENT')
        plt.xticks(rotation=35, ha='right')
        
        plt.subplot(1,3,3)
        plt.title('TOP 10 COUNTRIES WITH MOST CONTENTS')
        plt.bar(self.top_countries.index, self.top_countries.values)
        plt.xlabel('COUNTRY')
        plt.ylabel('NUMBER OF CONTENT')
        plt.xticks(rotation=35, ha='right')
        
        plt.tight_layout()
        plt.show()

    def analyze_top_content_release_months_and_years(self): #PIE-LINE-BAR GRAPH
        plt.figure(figsize=(20,9))
        
        plt.subplot(3,2,1)
        plt.pie(self.top_contents.values,labels=self.top_months.index,autopct='%1.1f%%')
        plt.title('TOP 10 MONTHS WITH MOST CONTENT RELEASED')
         
        plt.subplot(3,2,2)
        plt.pie(self.top_years.values,labels=self.top_years.index,autopct='%1.1f%%') #overlapping texts
        plt.title('TOP 10 YEARS WITH MOST CONTENT')
        
        plt.subplot(3,2,3)
        _top_months = self.top_months.index
        reversed_top_months = _top_months[::-1] #reversing for displaying in graph
        _top_contents_values = self.top_contents.values
        reversed_top_contents = _top_contents_values[::-1] #reversing for displaying in graph
        plt.plot(reversed_top_months, reversed_top_contents)
        plt.title('TOP 10 MONTHS WITH MOST CONTENT RELEASED')
        plt.xlabel('MONTHS')
        plt.ylabel('CONTENT RELEASED')
        
        plt.subplot(3,2,4)
        _top_years = self.top_years.index
        reversed_top_years = _top_years[::-1]
        plt.plot(reversed_top_years,reversed_top_contents[:5]) #reverse
        plt.title('TOP 10 YEARS WITH MOST CONTENT RELEASED')
        plt.xlabel('YEARS')
        plt.ylabel('CONTENT RELEASED')
        
        plt.subplot(3,2,5)
        plt.bar(reversed_top_months,reversed_top_contents)
        plt.xlabel('MONTHS')
        plt.ylabel('CONTENT RELEASED')
        
        plt.subplot(3,2,6)
        plt.bar(reversed_top_years,reversed_top_contents[:5]) #reverse
        plt.title('TOP 10 YEARS WITH MOST CONTENT RELEASED')
        plt.xlabel('YEARS')
        plt.ylabel('CONTENT RELEASED')
        
        plt.tight_layout()
        plt.show()

    def analyze_top_directors_and_actors(self): #PIE-BAR GRAPH
        plt.figure(figsize=(20,9))
        plt.subplot(2,2,1)
        plt.title("TOP DIRECTORS")
        plt.pie(self.top_directors.values,labels=self.top_directors.index,autopct='%1.1f%%')
        
        plt.subplot(2,2,2)
        plt.title("TOP CAST")
        plt.pie(self.top_actors.values,labels=self.top_actors.index,autopct='%1.1f%%')
        
        plt.subplot(2,2,3)
        plt.bar(self.top_directors.index,self.top_directors.values)
        plt.title("TOP DIRECTORS")
        plt.xlabel("DIRECTORS")
        plt.ylabel("CONTENTS")
        plt.xticks(rotation=35,ha="right")
        
        plt.subplot(2,2,4)
        plt.bar(self.top_actors.index,self.top_actors.values)
        plt.title("TOP ACTORS")
        plt.xlabel("ACTORS")
        plt.ylabel("CONTENTS")
        plt.xticks(rotation=35,ha="right")
        
        plt.tight_layout()
        plt.show()
        
if __name__ == "__main__":
    pme = Pandas_Matplotlib_examples_CSV()
    pme.launcher()