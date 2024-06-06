import pandas as pd 
from pandastable import Table
import matplotlib.pyplot as plt
import tkinter as tk 
from tkinter import ttk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
df = pd.read_json('pokemonDB_dataset.json', orient='index')

class Pandas_Matplotlib_examples_JSON():
    def __init__(self):
        self.root = tk.Tk()
        self.screen_width = self.root.winfo_screenwidth()
        self.screen_height = self.root.winfo_screenheight()
        self.root.geometry(f"{self.screen_width}x{self.screen_height}")
        self.root.title("Pandas-Matplotlib-Examples-JSON")
        self.root.state('zoomed') 
        
        home_button = tk.Button(self.root, text="HOME", command=lambda:self.launcher(), bg="#4b4b4b", fg="#FFFFFF")
        home_button.place(x=self.screen_width/2,y=10)
        
        self.graph_frame = tk.Frame(self.root, bg="#2b2b2b")
        self.graph_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=(50,15))
        
        self.top_pokemon_types = df['Type'].value_counts().head(10).sort_values(ascending=True)
        
        self.top_most_common_species = df['Species'].value_counts().head(10).sort_values(ascending=True)
        
        df['Type'] = df['Type'].str.replace(r'\s*\([^()]*\)', '', regex=True)
        self.pokemon_types = sorted(set(j.strip() for i in df['Type'].values for j in i.split(',')))
        self.selected_type = tk.StringVar(value=self.pokemon_types[0])
        
        df['Height'] = df['Height'].str.replace(r'\s*\([^()]*\)', '', regex=True) #clear
        df['Height'] = df['Height'].str.replace('m', '').astype(float) #convert to float
        self.heighest_pokemons = df.nlargest(10, 'Height')
        
        df['Weight'] = df['Weight'].str.replace(r'\s*\([^()]*\)', '', regex=True) #clear
        df['Weight'] = df['Weight'].str.replace('kg', '').str.strip()
        df['Weight'] = pd.to_numeric(df['Weight'], errors='coerce')
        self.heaviest_pokemons = df.nlargest(10, 'Weight')
        
        df['Catch Rate'] = df['Catch Rate'].str.replace(r'\([^()]*\)', '', regex=True)
        df['Catch Rate'] = df['Catch Rate'].str.extract(r'(\d+)').astype(float).fillna(0).astype(int)  #only number, fill NaN
        
        df['Base Friendship'] = df['Base Friendship'].str.replace(r'\s*\([^()]*\)', '', regex=True)
        df['Base Friendship'] = pd.to_numeric(df['Base Friendship'], errors='coerce')
        self.friendliest_pokemons = df.nlargest(25, 'Base Friendship')
        
        self.growth_rate_mapping = {
            'Slow': 1,
            'Medium Slow': 2,
            'Medium Fast': 3,
            'Fast': 4,}
        df['Growth Rate'] = df['Growth Rate'].map(self.growth_rate_mapping)
        df['Growth Rate'] = pd.to_numeric(df['Growth Rate'], errors='coerce')
       
    def launcher(self) -> None:
        self.clear_graph()
        self.bar_frame = tk.Frame(self.graph_frame,bg='#606060')
        self.bar_frame.pack(fill=tk.BOTH, expand=True, padx=150, pady=100)
        
        self.button_texts = [
            "Top Pokemon Types", "Top Most Common Pokemon Species",
            "Top Pokemon Heights", "Top Pokemon Weights", 
            
            "TOP 25 Easiest SELECTED Pokemons To Catch", "TOP 25 Friendliest SELECTED Pokemons",
            "TOP 50 SELECTED Pokemons Growth Rate", "TOP 25 SELECTED Pokemons Base HP",
            "TOP 25 SELECTED Pokemons Base Speed", "TOP 10 SELECTED Attack-Defense Max"]

        self.commands = [
            lambda: self.analyze_top_pokemon_type_distrubition(),
            lambda: self.analyze_top_most_common_species(), 
            lambda: self.analyze_top_tallest_pokemons(),
            lambda: self.analyze_top_heaviest_pokemons(), 
            lambda: self.analyze_selected_type_top_easiest_pokemons_to_catch(self.selected_type.get()),
            lambda: self.analyze_selected_type_top_friendliset_pokemons(self.selected_type.get()), 
            lambda: self.analyze_selected_type_top_growth_rate_pokemons(self.selected_type.get()),
            lambda: self.analyze_selected_type_top_base_hp(self.selected_type.get()), 
            lambda: self.analyze_selected_type_top_speed_base(self.selected_type.get()),
            lambda: self.analyze_selected_type_top_max_attack_defense(self.selected_type.get())]
        
        self.button_frame = tk.Frame(self.bar_frame, width=self.screen_width, height=self.screen_height, bg="#4b4b4b")
        self.button_frame.pack(padx=250)
        
        self.buttons = []
        self.create_buttons()
        
        combobox = ttk.Combobox(self.button_frame, textvariable=self.selected_type, values=self.pokemon_types)  # Varsayılan olarak ilk seçeneği seçer
        combobox.place(x=340, y=320)
        
        combobox.bind("<<ComboboxSelected>>", self.update_button_texts)
        
        self.root.mainloop()
    
    def create_buttons(self) -> None:
        selected_type = self.selected_type.get()
        for i in range(10):
            text = self.button_texts[i].replace("SELECTED", selected_type) if "SELECTED" in self.button_texts[i] else self.button_texts[i]
            button_grid = tk.Button(self.button_frame, bg='#10AA10', height=3, width=35, text=text, command=self.commands[i])
            row = i // 2  #row
            col = i % 2   #column
            button_grid.grid(row=row, column=col, padx=75, pady=50)
            self.buttons.append(button_grid)
    
    def update_button_texts(self, event) -> None:
        selected_type = self.selected_type.get()
        for i, button in enumerate(self.buttons):
            text = self.button_texts[i]
            if "SELECTED" in text:
                new_text = text.replace("SELECTED", selected_type)
                button.config(text=new_text)
    
    def draw_canvas(self,fig) -> None:
        plt.tight_layout()
        canvas = FigureCanvasTkAgg(fig, master=self.graph_frame)
        canvas.draw()
        canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)
        
    def display_data(self) -> None:
        self.clear_graph()
        try: display_frame
        except:
            display_frame = tk.Frame(self.graph_frame)
            display_frame.pack(fill="both", expand=True, pady=(10,10))
            table = Table(display_frame, dataframe=df)
            table.show()
    
    def clear_graph(self) -> None:
        for i in self.graph_frame.winfo_children():
            i.destroy()
 
    def analyze_top_pokemon_type_distrubition(self) -> None: #PIE-BARH
        self.clear_graph()
        fig = plt.figure(figsize=(20, 10))

        ax1 = fig.add_subplot(2, 1, 1) #PIE GRAPH
        ax1.set_title('TOP 10 POKEMON TYPES')
        self.top_pokemon_types.plot(kind='pie', startangle=90, autopct='%1.1f%%')

        ax2 = fig.add_subplot(2, 1, 2) #BARH GRAPH
        ax2.set_title('TOP 10 POKEMON TYPES')
        self.top_pokemon_types.plot(kind='barh')

        self.draw_canvas(fig)

    def analyze_top_most_common_species(self) -> None: #BARH-PIE
        self.clear_graph()
        fig = plt.figure(figsize=(10,6))
        
        ax1 = fig.add_subplot(2,1,1)
        ax1.set_title('TOP 10 MOST COMMON POKEMON SPECIES')
        plt.barh(self.top_most_common_species.index, self.top_most_common_species.values)
        
        ax2 = fig.add_subplot(2,1,2)
        ax2.set_title('TOP 10 MOST COMMON POKEMON SPECIES')
        plt.pie(self.top_most_common_species.values,labels=self.top_most_common_species.index, autopct='%1.1f%%', startangle=90)
        
        self.draw_canvas(fig)
    
    def analyze_top_tallest_pokemons(self) -> None: #BARH
        self.clear_graph()
        fig = plt.figure(figsize=(10,6))
        ax1 = fig.add_subplot(1,1,1)
        ax1.set_title('TOP 10 TALLEST POKEMON')
        plt.barh(self.heighest_pokemons.index[::-1], self.heighest_pokemons['Height'][::-1])
        plt.xlabel('M')
        self.draw_canvas(fig)
    
    def analyze_top_heaviest_pokemons(self) -> None: #BARH
        self.clear_graph()
        fig = plt.figure(figsize=(20,10))
        ax1 = fig.add_subplot(1,1,1)
        ax1.set_title('TOP 10 HEAVIEST POKEMON')
        plt.barh(self.heaviest_pokemons.index[::-1],self.heaviest_pokemons['Weight'][::-1])
        plt.xlabel('KG')
        self.draw_canvas(fig)
    
    def analyze_selected_type_top_easiest_pokemons_to_catch(self,selected_type) -> None: #BARH
        self.clear_graph()
        easiest_10_pokemon_to_catch = df[df['Type'].str.contains(selected_type)].nlargest(25, 'Catch Rate')
        selected_type_top_easiest_pokemons_to_catch = easiest_10_pokemon_to_catch['Catch Rate'].sort_values(ascending=True)

        fig = plt.figure(figsize=(20,10)) 
        ax1 = fig.add_subplot(1,1,1)
        ax1.set_title(f'TOP EASIEST 25 {selected_type.upper()} POKEMONS TO CATCH')
        plt.barh(selected_type_top_easiest_pokemons_to_catch.index, selected_type_top_easiest_pokemons_to_catch.values)
        plt.xlabel('Catch Rate')
        self.draw_canvas(fig)
    
    def analyze_selected_type_top_friendliset_pokemons(self, selected_type) -> None: #BARH
        self.clear_graph()
        friendliest_pokemons = df[df['Type'].str.contains(selected_type)].nlargest(25,'Base Friendship')
        
        fig = plt.figure(figsize=(20,10))
        ax1 = fig.add_subplot(1,1,1)
        ax1.set_title(f'TOP 25 FRIENDLIEST {selected_type} POKEMONS')
        plt.barh(friendliest_pokemons.index[::-1], friendliest_pokemons['Base Friendship'][::-1])
        plt.xlabel('Base Friendship')
        self.draw_canvas(fig)
    
    def analyze_selected_type_top_growth_rate_pokemons(self,selected_type) -> None: #BARH
        self.clear_graph()
        selected_type_top_growth_rate_pokemons = df[df['Type'].str.contains(selected_type)].nlargest(50, 'Growth Rate')
        reverse_growth_rate_mapping = {v: k for k, v in self.growth_rate_mapping.items()}

        fig = plt.figure(figsize=(20,10))
        ax1 = fig.add_subplot(1,1,1)
        ax1.set_title(f'TOP 50 GROWTH RATE IN {selected_type} POKEMONS')
        plt.barh(selected_type_top_growth_rate_pokemons.index[::-1],selected_type_top_growth_rate_pokemons['Growth Rate'].map(reverse_growth_rate_mapping)[::-1])
        plt.xlabel("Growth Rate")
        growth_rate_labels = [reverse_growth_rate_mapping[i] for i in sorted(reverse_growth_rate_mapping.keys()) if i in selected_type_top_growth_rate_pokemons['Growth Rate'].values]
        plt.xticks(ticks=range(0, len(growth_rate_labels)), labels=growth_rate_labels)  
        self.draw_canvas(fig)

    def analyze_selected_type_top_base_hp(self,selected_type) -> None: #BARH
        self.clear_graph()
        selected_type_top_base_hp = df[df['Type'].str.contains(selected_type)].nlargest(25, 'HP Base')
        
        fig = plt.figure(figsize=(20,10))
        ax1 = fig.add_subplot(1,1,1)
        ax1.set_title(f'TOP 20 {selected_type} POKEMON BASE HP')
        plt.barh(selected_type_top_base_hp['HP Base'][::-1].index,selected_type_top_base_hp['HP Base'].values[::-1])        
        plt.xlabel('HP Base')
        self.draw_canvas(fig)
    
    def analyze_selected_type_top_speed_base(self,selected_type) -> None: #PIE
        self.clear_graph()
        selected_type_top_speed_base = df[df['Type'].str.contains(selected_type)].nlargest(25, 'Speed Base')
        
        fig = plt.figure(figsize=(20,10))
        ax1 = fig.add_subplot(1,1,1)
        ax1.set_title(F'TOP 10 {selected_type} POKEMON BASE SPEED')
        plt.barh(selected_type_top_speed_base['Speed Base'].index[::-1], selected_type_top_speed_base['Speed Base'].values[::-1])
        self.draw_canvas(fig)
    
    def analyze_selected_type_top_max_attack_defense(self,selected_type) -> None: #BARH-BARH
        self.clear_graph()
        selected_pokemons = df[df['Type'].str.contains(selected_type)]
        top_selected_type_attack_max = selected_pokemons.nlargest(10, 'Attack Max')
        top_selected_type_defense_max = selected_pokemons.nlargest(10, 'Defense Max')
        
        fig = plt.figure(figsize=(10,6))
        
        ax1 = fig.add_subplot(2,1,1)
        ax1.set_title(f'TOP 10 {selected_type.upper()} POKEMON ATTACK MAX')
        plt.barh(top_selected_type_attack_max['Attack Max'].index[::-1],top_selected_type_attack_max['Attack Max'].values[::-1])
    
        ax2 = fig.add_subplot(2,1,2)
        ax2.set_title(f'TOP 10 {selected_type.upper()} POKEMON DEFENSE MAX')
        plt.barh(top_selected_type_defense_max['Defense Max'].index[::-1],top_selected_type_defense_max['Defense Max'].values[::-1])
        self.draw_canvas(fig)
    
if __name__ == "__main__":
    pme = Pandas_Matplotlib_examples_JSON()
    pme.launcher()