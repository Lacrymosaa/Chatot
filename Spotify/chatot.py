import tkinter as tk
from tkinter import ttk
import spotipy
from spotipy.oauth2 import SpotifyOAuth
import webbrowser

def search_tracks(keyword, client_id, client_secret):
    sp_auth = SpotifyOAuth(
        client_id=client_id,
        client_secret=client_secret,
        redirect_uri="http://localhost:8888/callback",
        scope="user-library-read user-read-private"
    )
    
    token = sp_auth.get_access_token(as_dict=False)
    sp = spotipy.Spotify(auth=token)
    
    results = sp.search(q=keyword, type='track')
    tracks = results['tracks']['items']
    
    track_list = []
    for track in tracks:
        track_info = {
            'name': track['name'],
            'artist': track['artists'][0]['name'],
            'url': track['external_urls']['spotify']
        }
        track_list.append(track_info)
    
    return track_list

class MusicSearcher(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        self.master.title("Chatot")
        self.master.iconbitmap("imgs/chatot.ico")
        self.pack()
        self.create_widgets()

    def create_widgets(self):
        self.key_label = tk.Label(self, text="Keyword:")
        self.key_label.grid(row=0, column=0)
        self.key_entry = tk.Entry(self)
        self.key_entry.grid(row=0, column=1)
        self.search_button = tk.Button(self, text="Search", command=self.search)
        self.search_button.grid(row=0, column=2)

        self.track_table = ttk.Treeview(self, height=10)
        self.track_table["columns"] = ('name', 'artist', 'url')
        self.track_table.column("#0", width=0)  # Define largura 0 e sem stretch para a coluna de "id"
        self.track_table.heading('name', text='Name')
        self.track_table.heading('artist', text='Artist')
        self.track_table.heading('url', text='URL')
        self.track_table.column('name', width=200)
        self.track_table.column('artist', width=200)
        self.track_table.column('url', width=300)
        self.track_table.grid(row=1, column=0, columnspan=3)


        # Bind de evento para abrir a URL correspondente no navegador ao clicar na coluna 'url'
        self.track_table.bind("<Button-1>", self.on_item_click)

    def on_item_click(self, event):
            item_id = self.track_table.identify_row(event.y)
            if item_id:
                url = self.track_table.item(item_id, 'values')[2]
                if url:
                    webbrowser.open(url)

    def search(self):
        keyword = self.key_entry.get()
        client_id = open('id.txt', 'r').read().strip()
        client_secret = open('secret.txt', 'r').read().strip()
        track_list = search_tracks(keyword, client_id, client_secret)

        self.track_table.delete(*self.track_table.get_children())
        for track in track_list:
            self.track_table.insert('', 'end', values=(track['name'], track['artist'], track['url']))
        self.track_table.yview_moveto(1.0)

root = tk.Tk()
app = MusicSearcher(master=root)
app.mainloop()
