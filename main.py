from kivymd.app import MDApp
from kivymd.uix.list import OneLineListItem, MDList
from kivymd.uix.screen import MDScreen
from kivymd.uix.textfield import MDTextField
from kivymd.uix.button import MDRaisedButton
from kivy.uix.scrollview import ScrollView
import sqlite3

class TodoApp(MDApp):
    def build(self):
        self.theme_cls.theme_style = "Light"
        self.theme_cls.primary_palette = "Indigo"
        screen = MDScreen()
        
        # Campo de entrada de texto
        self.task_input = MDTextField(
            hint_text="Digite uma tarefa",
            size_hint_x=0.8,
            pos_hint={"center_x": 0.5, "top": 0.9}
        )
        
        # Botão para adicionar tarefa
        add_button = MDRaisedButton(
            text="Adicionar",
            pos_hint={"center_x": 0.5, "top": 0.8},
            on_press=self.add_task
        )
        
        # Lista rolável de tarefas
        self.scroll = ScrollView(
            pos_hint={"top": 0.7}, 
            size_hint=(1, 0.7)
        )
        self.task_list = MDList()
        self.scroll.add_widget(self.task_list)
        
        # Adicionando widgets à tela
        screen.add_widget(self.task_input)
        screen.add_widget(add_button)
        screen.add_widget(self.scroll)
        
        # Carregar tarefas do banco de dados
        self.load_tasks()
        
        return screen
    
    def add_task(self, instance):
        task_text = self.task_input.text.strip()
        if task_text:
            # Salvar no banco de dados
            conn = sqlite3.connect('tasks.db')
            cursor = conn.cursor()
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS tasks (
                    id INTEGER PRIMARY KEY, 
                    task TEXT
                )
            ''')
            cursor.execute('INSERT INTO tasks (task) VALUES (?)', (task_text,))
            conn.commit()
            conn.close()
            
            # Atualizar a lista
            self.task_list.add_widget(OneLineListItem(text=task_text))
            self.task_input.text = ""
    
    def load_tasks(self):
        conn = sqlite3.connect('tasks.db')
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS tasks (
                id INTEGER PRIMARY KEY, 
                task TEXT
            )
        ''')
        tasks = cursor.execute('SELECT task FROM tasks').fetchall()
        for task in tasks:
            self.task_list.add_widget(OneLineListItem(text=task[0]))
        conn.close()

if __name__ == "__main__":
    TodoApp().run()