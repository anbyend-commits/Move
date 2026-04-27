import json
import os
import tkinter as tk
from tkinter import ttk, messagebox

MOVIE_FILE = "movies.json"

def load_data():
    if os.path.exists(MOVIE_FILE):
        with open(MOVIE_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    else:
        return []

def save_data(data):
    with open(MOVIE_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=4)

def refresh_table(data):
    tree.delete(*tree.get_children())
    for movie in data:
        tree.insert('', tk.END, values=(movie["title"], movie["genre"], movie["year"], movie["rating"]))

def add_movie():
    title = title_entry.get().strip()
    genre = genre_entry.get().strip()
    year = year_entry.get().strip()
    rating = rating_entry.get().strip()

    # Проверка полей
    if not title or not genre or not year or not rating:
        messagebox.showerror("Ошибка", "Заполните все поля")
        return
    if not year.isdigit() or not (1888 <= int(year) <= 2100):
        messagebox.showerror("Ошибка", "Год должен быть целым числом от 1888 до 2100")
        return
    try:
        rating_val = float(rating)
        if not (0 <= rating_val <= 10):
            raise ValueError
    except:
        messagebox.showerror("Ошибка", "Рейтинг должен быть числом от 0 до 10")
        return
    movie = {
        "title": title,
        "genre": genre,
        "year": int(year),
        "rating": rating_val
    }
    movies.append(movie)
    save_data(movies)
    refresh_table(filter_data())
    title_entry.delete(0, tk.END)
    genre_entry.delete(0, tk.END)
    year_entry.delete(0, tk.END)
    rating_entry.delete(0, tk.END)
    update_filters()

def filter_data():
    genre = filter_genre.get()
    year = filter_year.get()
    res = movies
    if genre and genre != "Все":
        res = [m for m in res if m["genre"] == genre]
    if year and year != "Все":
        res = [m for m in res if str(m["year"]) == year]
    return res

def apply_filters(event=None):
    refresh_table(filter_data())

def update_filters():
    # Обновление опций фильтров после добавления фильмов
    unique_genres = sorted(set(m["genre"] for m in movies))
    unique_years = sorted(set(str(m["year"]) for m in movies))
    filter_genre["values"] = ["Все"] + unique_genres
    filter_year["values"] = ["Все"] + unique_years

root = tk.Tk()
root.title("Movie Library (Личная кинотека)")

# --- Поля для добавления ---
tk.Label(root, text="Название").grid(row=0, column=0)
title_entry = tk.Entry(root, width=20)
title_entry.grid(row=0, column=1)

tk.Label(root, text="Жанр").grid(row=0, column=2)
genre_entry = tk.Entry(root, width=15)
genre_entry.grid(row=0, column=3)

tk.Label(root, text="Год выпуска").grid(row=1, column=0)
year_entry = tk.Entry(root, width=10)
year_entry.grid(row=1, column=1)

tk.Label(root, text="Рейтинг (0–10)").grid(row=1, column=2)
rating_entry = tk.Entry(root, width=10)
rating_entry.grid(row=1, column=3)

add_btn = tk.Button(root, text="Добавить фильм", width=20, command=add_movie)
add_btn.grid(row=2, column=0, columnspan=4, pady=5)

# --- Фильтры ---
tk.Label(root, text="Фильтр по жанру:").grid(row=3, column=0)
filter_genre = ttk.Combobox(root, state="readonly", width=15)
filter_genre.grid(row=3, column=1)
filter_genre.bind("<<ComboboxSelected>>", apply_filters)

tk.Label(root, text="Фильтр по году:").grid(row=3, column=2)
filter_year = ttk.Combobox(root, state="readonly", width=8)
filter_year.grid(row=3, column=3)
filter_year.bind("<<ComboboxSelected>>", apply_filters)

# --- Таблица ---
columns = ("Название", "Жанр", "Год", "Рейтинг")
tree = ttk.Treeview(root, columns=columns, show="headings", height=10)
for col in columns:
    tree.heading(col, text=col)
tree.grid(row=4, column=0, columnspan=4, pady=10)

# --- Загрузка данных ---
movies = load_data()
update_filters()
refresh_table(movies)

root.mainloop()