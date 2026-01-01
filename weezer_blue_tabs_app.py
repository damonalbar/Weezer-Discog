import tkinter as tk
from tkinter import ttk, messagebox
import json
import os
import hashlib

USERS_FILE = "users.json"

# weezer album
weezer_albums = {
    "Weezer (Blue Album)": {
        "release": "1994-05-10", "label": "DGC", "genre": "Alternative rock",
        "description": "Debut album with hits like Buddy Holly and Say It Ain’t So.",
        "songs": [{"name": x, "lyrics": ""} for x in [
            "My Name Is Jonas","No One Else","The World Has Turned and Left Me Here",
            "Buddy Holly","Undone – The Sweater Song","Surf Wax America",
            "Say It Ain’t So","In the Garage","Holiday","Only in Dreams"
        ]]
    },
    "Pinkerton": {
        "release": "1996-09-24", "label": "DGC", "genre": "Alternative rock",
        "description": "Cult favorite second album.",
        "songs": [{"name": x, "lyrics": ""} for x in [
            "Tired of Sex","Getchoo","No Other One","Why Bother?",
            "Across the Sea","The Good Life","El Scorcho","Pink Triangle",
            "Falling for You","Butterfly"
        ]]
    },
    "Weezer (Green Album)": {
        "release": "2001-05-15","label":"Geffen","genre":"Power pop",
        "description":"Comeback album featuring Hash Pipe and Island In The Sun.",
        "songs":[{"name":x,"lyrics":""} for x in [
            "Don’t Let Go","Photograph","Hash Pipe","Island in the Sun",
            "Crab","Knockdown Dragout","Smile","Simple Pages",
            "Glorious Day","O Girlfriend"
        ]]
    },
    "Maladroit": {
        "release":"2002-05-14","label":"Geffen","genre":"Alternative rock",
        "description":"Heavy, guitar‑driven rock.",
        "songs":[{"name":x,"lyrics":""} for x in [
            "American Gigolo","Dope Nose","Keep Fishin’","Take Control",
            "Death and Destruction","Slob","Burndt Jamb","Space Rock",
            "Slave","Fall Together","Possibilities","Love Explosion","December"
        ]]
    },
    "Make Believe": {
        "release":"2005-05-10","label":"Geffen","genre":"Alt rock",
        "description":"Includes gritty and emotional tracks.",
        "songs":[{"name":x,"lyrics":""} for x in [
            "Beverly Hills","Perfect Situation","This Is Such a Pity","Hold Me",
            "Peace","We Are All on Drugs","The Damage in Your Heart","Pardon Me",
            "My Best Friend","The Other Way","Freak Me Out","Haunt You Every Day"
        ]]
    },
    "Weezer (Red Album)": {
        "release":"2008-06-03","label":"DGC / Interscope","genre":"Alternative rock",
        "description":"The band explores varied styles.",
        "songs":[{"name":x,"lyrics":""} for x in [
            "Troublemaker","The Greatest Man That Ever Lived (Variations on a Shaker Hymn)",
            "Pork and Beans","Heart Songs","Everybody Get Dangerous","Dreamin’",
            "Thought I Knew","Cold Dark World","Automatic","The Angel and the One"
        ]]
    },
    "Raditude": {
        "release":"2009-10-30","label":"Geffen","genre":"Pop rock",
        "description":"Playful, upbeat tracks.",
        "songs":[{"name":x,"lyrics":""} for x in [
            "(If You’re Wondering If I Want You To) I Want You To","I’m Your Daddy","The Girl Got Hot",
            "Can’t Stop Partying","Put Me Back Together","Trippin’ Down the Freeway",
            "Love Is the Answer","Let It All Hang Out","In the Mall","I Don’t Want to Let You Go"
        ]]
    },
    "Hurley": {
        "release":"2010-09-14","label":"Epitaph","genre":"Alt rock",
        "description":"Energetic and quirky.",
        "songs":[{"name":x,"lyrics":""} for x in [
            "Memories","Ruling Me","Trainwrecks","Unspoken","Where’s My Sex?",
            "Run Away","Hang On","Smart Girls","Brave New World","Time Flies"
        ]]
    },
    "Everything Will Be Alright in the End": {
        "release":"2014-10-07","label":"Republic","genre":"Alt rock",
        "description":"Melodic, layered compositions.",
        "songs":[{"name":x,"lyrics":""} for x in [
            "Ain’t Got Nobody","Back to the Shack","Eulogy for a Rock Band","Lonely Girl",
            "I’ve Had It Up to Here","The British Are Coming","Da Vinci","Go Away",
            "Cleopatra","Foolish Father","The Futurescope Trilogy: I. The Waste Land",
            "The Futurescope Trilogy: II. Anonymous","The Futurescope Trilogy: III. Return to Ithaka"
        ]]
    },
    "Weezer (White Album)": {
        "release":"2016-04-01","label":"Atlantic / Crush","genre":"Alt rock",
        "description":"Sunny, melodic LP.",
        "songs":[{"name":x,"lyrics":""} for x in [
            "California Kids","Wind in Our Sail","Thank God for Girls",
            "(Girl We Got a) Good Thing","Do You Wanna Get High?",
            "King of the World","Summer Elaine and Drunk Dori",
            "L.A. Girlz","Jacked Up","Endless Bummer"
        ]]
    },
    "Pacific Daydream": {
        "release":"2017-10-27","label":"Atlantic","genre":"Pop rock",
        "description":"Bright, dreamy tunes.",
        "songs":[{"name":x,"lyrics":""} for x in [
            "Mexican Fender","Beach Boys","Feels Like Summer","Happy Hour","Weekend Woman",
            "QB Blitz","Sweet Mary","Get Right","La Mancha Screwjob","Any Friend of Diane’s"
        ]]
    },
    "Weezer (Teal Album)": {
        "release":"2019-01-24","label":"Crush / Atlantic","genre":"Covers",
        "description":"Covers of iconic hits.",
        "songs":[{"name":x,"lyrics":""} for x in [
            "Africa","Everybody Wants to Rule the World","Sweet Dreams (Are Made of This)",
            "Take on Me","Happy Together","Paranoid","Mr. Blue Sky","No Scrubs","Billie Jean","Stand by Me"
        ]]
    },
    "Weezer (Black Album)": {
        "release":"2019-03-01","label":"Crush / Atlantic","genre":"Alt rock",
        "description":"Moody and experimental.",
        "songs":[{"name":x,"lyrics":""} for x in [
            "Can’t Knock the Hustle","Zombie Bastards","High as a Kite","Living in L.A.",
            "Piece of Cake","I’m Just Being Honest","Too Many Thoughts in My Head",
            "The Prince Who Wanted Everything","Byzantine","California Snow"
        ]]
    },
    "OK Human": {
        "release":"2021-01-29","label":"Crush Music / Atlantic","genre":"Chamber pop",
        "description":"Orchestral and introspective.",
        "songs":[{"name":x,"lyrics":""} for x in [
            "All My Favorite Songs","Aloo Gobi","Grapes of Wrath","Numbers","Playing My Piano",
            "Mirror Image","Screens","Bird With a Broken Wing","Dead Roses",
            "Everything Happens for a Reason","Here Comes the Rain","La Brea Tar Pits"
        ]]
    },
    "Van Weezer": {
        "release":"2021-05-07","label":"Crush Music / Atlantic","genre":"Rock",
        "description":"Hard‑rock inspired.",
        "songs":[{"name":x,"lyrics":""} for x in [
            "Hero","All the Good Ones","The End of the Game","I Need Some of That","Beginning of the End",
            "Blue Dream","1 More Hit","Sheila Can Do It","She Needs Me","Precious Metal Girl"
        ]]
    },
    "SZNZ: Spring": { "release":"2022-03-20","label":"Crush / Atlantic","genre":"Seasonal EP",
        "description":"Spring‑time vibes.","songs":[{"name":x,"lyrics":""} for x in [
            "Opening Night","Angels on Vacation","A Little Bit of Love",
            "The Garden of Eden","The Sound of Drums","All This Love","Wild at Heart"
        ]]
    },
    "SZNZ: Summer": { "release":"2022-06-21","label":"Crush / Atlantic","genre":"Seasonal EP",
        "description":"Summer‑time vibes.","songs":[{"name":x,"lyrics":""} for x in [
            "Lawn Chair","Records","Blue Like Jazz","The Opposite of Me",
            "What’s the Good of Being Good","Cuomoville","Thank You and Good Night"
        ]]
    },
    "SZNZ: Autumn": { "release":"2022-09-22","label":"Crush / Atlantic","genre":"Seasonal EP",
        "description":"Autumn‑time vibes.","songs":[{"name":x,"lyrics":""} for x in [
            "Can’t Dance, Don’t Ask Me","Get Off on the Pain",
            "What Happens After You?","Francesca","Should She Stay or Should She Go",
            "The Way I Hate You Now","Close to You"
        ]]
    },
    "SZNZ: Winter": { "release":"2022-12-21","label":"Crush / Atlantic","genre":"Seasonal EP",
        "description":"Winter‑time vibes.","songs":[{"name":x,"lyrics":""} for x in [
            "I Want a Dog","Iambic Pentameter","Basketball","Sheraton Commander",
            "Dark Enough to See the Stars","The One That Got Away","The Deep and Dreamless Sleep"
        ]]
    }
}

# app
class WeezerApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Weezer Discography Explorer")
        self.geometry("1000x700")
        self.configure(bg="#0b3d91")

        self.current_user = None
        self.users = self.load_users()
        self.selected_album = None
        self.selected_song = None
        self.tree = None
        self.lbl_song_info = None
        self.txt_lyrics = None

        self.show_login_signup()

    # user manage
    def load_users(self):
        if os.path.exists(USERS_FILE):
            with open(USERS_FILE, "r", encoding="utf-8") as f:
                return json.load(f)
        return {}

    def save_users(self):
        with open(USERS_FILE, "w", encoding="utf-8") as f:
            json.dump(self.users, f, ensure_ascii=False, indent=2)

    def hash_password(self, password):
        return hashlib.sha256(password.encode()).hexdigest()

    # login sign
    def show_login_signup(self):
        popup = tk.Toplevel(self)
        popup.title("Login / Sign Up")
        popup.geometry("400x250")
        popup.configure(bg="#0b3d91")
        popup.grab_set()

        tk.Label(popup, text="Username:", bg="#0b3d91", fg="white").pack(pady=(20,5))
        entry_user = tk.Entry(popup)
        entry_user.pack(pady=5)

        tk.Label(popup, text="Password:", bg="#0b3d91", fg="white").pack(pady=5)
        entry_pass = tk.Entry(popup, show="*")
        entry_pass.pack(pady=5)

        def login():
            username = entry_user.get().strip()
            password = entry_pass.get().strip()
            if username in self.users and self.users[username]["password"] == self.hash_password(password):
                self.current_user = username
                self.load_user_lyrics()
                popup.destroy()
                self.build_main_ui()
            else:
                messagebox.showerror("Error", "Invalid username or password.")

        def signup():
            username = entry_user.get().strip()
            password = entry_pass.get().strip()
            if username in self.users:
                messagebox.showerror("Error", "Username exists.")
            elif not username or not password:
                messagebox.showerror("Error", "Enter valid credentials.")
            else:
                self.users[username] = {"password": self.hash_password(password), "lyrics": {}}
                self.save_users()
                messagebox.showinfo("Success", "Sign up complete. Please log in.")

        tk.Button(popup, text="Login", command=login).pack(pady=10)
        tk.Button(popup, text="Sign Up", command=signup).pack()

    # load and save lyric
    def load_user_lyrics(self):
        saved = self.users.get(self.current_user, {}).get("lyrics", {})
        for album_name, album in weezer_albums.items():
            if album_name in saved:
                for song in album["songs"]:
                    name = song["name"]
                    if name in saved[album_name]:
                        song["lyrics"] = saved[album_name][name]

    def save_user_lyrics(self):
        lyrics_data = {}
        for album_name, album in weezer_albums.items():
            lyrics_data[album_name] = {}
            for song in album["songs"]:
                lyrics_data[album_name][song["name"]] = song.get("lyrics", "")
        self.users[self.current_user]["lyrics"] = lyrics_data
        self.save_users()
        messagebox.showinfo("Saved", "All lyrics saved to your profile!")

    # logout
    def logout(self):
        if messagebox.askyesno("Log Out", "Log out and save lyrics?"):
            self.save_user_lyrics()
            self.destroy()
            app = WeezerApp()
            app.mainloop()

    # main ui
    def build_main_ui(self):
        top_frame = tk.Frame(self, bg="#0b3d91")
        top_frame.pack(fill="x", pady=(5,0))

        btn_save = tk.Button(top_frame, text="Save Work", command=self.save_user_lyrics,
                             bg="#0b66d1", fg="white")
        btn_save.pack(side="left", padx=10, pady=5)

        btn_logout = tk.Button(top_frame, text="Log Out", command=self.logout,
                               bg="#d11c3b", fg="white")
        btn_logout.pack(side="left", padx=10, pady=5)

        tk.Label(top_frame, text="Search:", bg="#0b3d91", fg="white").pack(side="left", padx=(20,5))
        self.search_var = tk.StringVar()
        search_entry = tk.Entry(top_frame, textvariable=self.search_var)
        search_entry.pack(side="left")
        search_entry.bind("<KeyRelease>", self.search_song)

        main_frame = tk.Frame(self, bg="#0b3d91")
        main_frame.pack(fill="both", expand=True, padx=5, pady=5)

        left_frame = tk.Frame(main_frame, bg="#0b3d91", width=300)
        left_frame.pack(side="left", fill="y")

        self.tree = ttk.Treeview(left_frame)
        self.tree.pack(fill="y", expand=True)
        self.populate_tree()
        self.tree.bind("<<TreeviewSelect>>", self.on_song_select)

        right_frame = tk.Frame(main_frame, bg="#0b3d91")
        right_frame.pack(side="left", fill="both", expand=True, padx=10)

        self.lbl_song_info = tk.Label(right_frame, text="Select a song to view details",
                                      bg="#0b3d91", fg="white", font=("Helvetica", 14),
                                      justify="left", wraplength=650)
        self.lbl_song_info.pack(anchor="nw", pady=(10,5))

        self.txt_lyrics = tk.Text(right_frame, wrap="word", bg="white", fg="black")
        self.txt_lyrics.pack(fill="both", expand=True, pady=5)

        btn_save_lyrics = tk.Button(right_frame, text="Save Lyrics", command=self.save_lyrics,
                                    bg="#0b66d1", fg="white")
        btn_save_lyrics.pack(pady=(0,10))

    # tree
    def populate_tree(self):
        self.tree.delete(*self.tree.get_children())
        for album, data in weezer_albums.items():
            album_id = self.tree.insert("", "end", text=album, open=True)
            for song in data["songs"]:
                self.tree.insert(album_id, "end", text=song["name"])

    # search w filter
    def search_song(self, event=None):
        q = self.search_var.get().lower()
        self.tree.delete(*self.tree.get_children())
        for album, data in weezer_albums.items():
            album_id = self.tree.insert("", "end", text=album, open=True)
            for song in data["songs"]:
                name = song["name"]
                if q in name.lower():
                    self.tree.insert(album_id, "end", text=name)

    # song selection
    def on_song_select(self, event):
        sel = self.tree.selection()
        if not sel:
            return
        item = sel[0]
        parent = self.tree.parent(item)
        if not parent:
            return
        album_name = self.tree.item(parent, "text")
        song_name = self.tree.item(item, "text")

        self.selected_album = album_name
        self.selected_song = None
        for s in weezer_albums[album_name]["songs"]:
            if s["name"] == song_name:
                self.selected_song = s
                break

        if self.selected_song:
            self.lbl_song_info.config(
                text=f"Song: {song_name}\nAlbum: {album_name}\nReleased: {weezer_albums[album_name]['release']}"
            )
            self.txt_lyrics.delete("1.0", "end")
            self.txt_lyrics.insert("1.0", self.selected_song.get("lyrics",""))

    # -saving lyrics
    def save_lyrics(self):
        if self.selected_song is None:
            messagebox.showwarning("No Song Selected", "Please select a song first.")
            return
        self.selected_song["lyrics"] = self.txt_lyrics.get("1.0", "end-1c")
        self.save_user_lyrics()


if __name__ == "__main__":
    app = WeezerApp()
    app.mainloop()
