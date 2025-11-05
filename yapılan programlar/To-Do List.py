import tkinter as tk
from tkinter import messagebox, filedialog
import json
import os
import random

DATA_FILE = "todo_data.json"
tasks = []
done_tasks = []

def load_data():
    global tasks, done_tasks
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "r", encoding="utf-8") as f:
            data = json.load(f)
            tasks[:] = data.get("tasks", [])
            done_tasks[:] = data.get("done_tasks", [])

def save_data():
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump({"tasks": tasks, "done_tasks": done_tasks}, f, ensure_ascii=False, indent=2)

def open_add_task_window():
    add_win = tk.Toplevel(root)
    add_win.title("Yeni Görev Ekle")
    add_win.geometry("300x200")

    tk.Label(add_win, text="Görev:").pack()
    entry_task = tk.Entry(add_win)
    entry_task.pack()

    tk.Label(add_win, text="Kategori:").pack()
    entry_category = tk.Entry(add_win)
    entry_category.pack()

    tk.Label(add_win, text="Tarih (GG/AA/YYYY):").pack()
    entry_date = tk.Entry(add_win)
    entry_date.pack()

    def save_task():
        task = entry_task.get()
        category = entry_category.get()
        date = entry_date.get()
        if not task:
            messagebox.showwarning("Uyarı", "Görev giriniz!")
            return
        tasks.append((task, category, date))
        update_list()
        save_data()
        add_win.destroy()

    tk.Button(add_win, text="Kaydet", command=save_task).pack(pady=10)

def update_list():
    listbox.delete(0, tk.END)
    for task, category, date in tasks:
        listbox.insert(tk.END, f"{task} [{category}] ({date})")

def update_done_list():
    done_listbox.delete(0, tk.END)
    for task, category, date in done_tasks:
        done_listbox.insert(tk.END, f"{task} [{category}] ({date})")

def mark_done():
    idx = listbox.curselection()
    if not idx:
        return
    i = idx[0]
    file_path = filedialog.askopenfilename(
        title="Ekran görüntüsü veya fotoğraf yükle (isteğe bağlı)",
        filetypes=[("Resim Dosyaları", "*.png;*.jpg;*.jpeg;*.bmp;*.gif")]
    )
    if not file_path:
        messagebox.showinfo("Bilgi", "Fotoğraf yüklemeden tamamlandı olarak işaretleyemezsin. İstersen tekrar deneyebilirsin.")
        return
    done_tasks.append(tasks[i])
    tasks.pop(i)
    update_list()
    update_done_list()
    save_data()
    kalan = len(tasks)
    messagebox.showinfo("Onaylandı!", f"Tam gaz devam! {kalan} görevin kaldı.")

def undo_done():
    idx = done_listbox.curselection()
    if not idx:
        return
    i = idx[0]
    tasks.append(done_tasks[i])
    done_tasks.pop(i)
    update_list()
    update_done_list()
    save_data()

def delete_task():
    idx = listbox.curselection()
    if not idx:
        return
    i = idx[0]
    tasks.pop(i)
    update_list()
    save_data()

def delete_done_task():
    idx = done_listbox.curselection()
    if not idx:
        return
    i = idx[0]
    done_tasks.pop(i)
    update_done_list()
    save_data()

def get_random_bg_and_text():
    # Rastgele pastel arka plan rengi
    def pastel():
        return random.randint(180, 255)
    r, g, b = pastel(), pastel(), pastel()
    bg_color = f'#{r:02x}{g:02x}{b:02x}'
    # Luminans hesapla, yazı rengi seç
    luminance = (0.299*r + 0.587*g + 0.114*b)
    text_color = "#222222" if luminance > 180 else "#f8f8f8"
    return bg_color, text_color

root = tk.Tk()
root.title("Gelişmiş To-Do List")

# Rastgele arka plan ve uygun yazı rengi ayarla
bg_color, text_color = get_random_bg_and_text()
root.configure(bg=bg_color)

# Tüm widget'larda yazı rengini ayarlamak için yardımcı fonksiyon
def set_fg(widget):
    try:
        widget.configure(fg=text_color, bg=bg_color)
    except Exception:
        pass
    for child in widget.winfo_children():
        set_fg(child)

btn_add = tk.Button(root, text="Yeni Görev Ekle", command=open_add_task_window)
btn_add.pack(pady=10)
listbox = tk.Listbox(root, width=50)
listbox.pack(pady=10)

frame1 = tk.Frame(root, bg=bg_color)
frame1.pack()
btn_done = tk.Button(frame1, text="Tamamlandı (Tik)", command=mark_done)
btn_done.pack(side=tk.LEFT, padx=5)
btn_del = tk.Button(frame1, text="Sil", command=delete_task)
btn_del.pack(side=tk.LEFT, padx=5)

lbl_done = tk.Label(root, text="Yapıldı Listesi:", bg=bg_color)
lbl_done.pack()
done_listbox = tk.Listbox(root, width=50)
done_listbox.pack(pady=5)

frame2 = tk.Frame(root, bg=bg_color)
frame2.pack()
btn_undo = tk.Button(frame2, text="Geri Al", command=undo_done)
btn_undo.pack(side=tk.LEFT, padx=5)
btn_del_done = tk.Button(frame2, text="Sil", command=delete_done_task)
btn_del_done.pack(side=tk.LEFT, padx=5)

# Tüm widget'larda yazı rengini ayarla
set_fg(root)

load_data()
update_list()
update_done_list()

root.mainloop()
