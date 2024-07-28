import tkinter as tk
from tkinter import messagebox
import json
import os

RECIPES_FILE = "recipes.json"
recipes = []

def setup_window():
    root = tk.Tk()
    root.title("Recipe Manager")
    root.geometry("400x500")
    return root

def create_input_fields(root):
    tk.Label(root, text="Recipe Name:").pack(pady=5)
    name_entry = tk.Entry(root, width=50)
    name_entry.pack(pady=5)

    tk.Label(root, text="Ingredients:").pack(pady=5)
    ingredients_text = tk.Text(root, width=50, height=5)
    ingredients_text.pack(pady=5)

    tk.Label(root, text="Instructions:").pack(pady=5)
    instructions_text = tk.Text(root, width=50, height=10)
    instructions_text.pack(pady=5)

    return name_entry, ingredients_text, instructions_text

def create_buttons(root, name_entry, ingredients_text, instructions_text, recipe_list):
    add_button = tk.Button(root, text="Add Recipe", command=lambda: add_recipe(name_entry, ingredients_text, instructions_text, recipe_list))
    add_button.pack(pady=5)

    view_button = tk.Button(root, text="View Recipe", command=lambda: view_recipe(recipe_list))
    view_button.pack(pady=5)

    delete_button = tk.Button(root, text="Delete Recipe", command=lambda: delete_recipe(recipe_list))
    delete_button.pack(pady=5)

def create_recipe_list(root):
    recipe_list = tk.Listbox(root, width=50, height=10)
    recipe_list.pack(pady=10)
    return recipe_list

def add_recipe(name_entry, ingredients_text, instructions_text, recipe_list):
    name = name_entry.get().strip()
    ingredients = ingredients_text.get("1.0", tk.END).strip()
    instructions = instructions_text.get("1.0", tk.END).strip()

    if name and ingredients and instructions:
        recipes.append({
            "name": name,
            "ingredients": ingredients,
            "instructions": instructions
        })
        recipe_list.insert(tk.END, name)
        name_entry.delete(0, tk.END)
        ingredients_text.delete("1.0", tk.END)
        instructions_text.delete("1.0", tk.END)
        save_recipes()
    else:
        messagebox.showwarning("Warning", "All fields are required.")

def view_recipe(recipe_list):
    selected_index = recipe_list.curselection()
    if selected_index:
        index = selected_index[0]
        recipe = recipes[index]
        view_window = tk.Toplevel()
        view_window.title(recipe["name"])
        view_window.geometry("400x400")
        tk.Label(view_window, text="Ingredients:").pack(pady=5)
        tk.Label(view_window, text=recipe["ingredients"], wraplength=380, justify="left").pack(pady=5)
        tk.Label(view_window, text="Instructions:").pack(pady=5)
        tk.Label(view_window, text=recipe["instructions"], wraplength=380, justify="left").pack(pady=5)
    else:
        messagebox.showwarning("Warning", "Please select a recipe to view.")

def delete_recipe(recipe_list):
    selected_index = recipe_list.curselection()
    if selected_index:
        index = selected_index[0]
        recipe_list.delete(index)
        del recipes[index]
        save_recipes()
    else:
        messagebox.showwarning("Warning", "Please select a recipe to delete.")

def save_recipes():
    with open(RECIPES_FILE, "w") as file:
        json.dump(recipes, file)

def load_recipes():
    if os.path.exists(RECIPES_FILE):
        with open(RECIPES_FILE, "r") as file:
            return json.load(file)
    return []

def main():
    global recipes
    root = setup_window()
    
    name_entry, ingredients_text, instructions_text = create_input_fields(root)
    recipe_list = create_recipe_list(root)
    create_buttons(root, name_entry, ingredients_text, instructions_text, recipe_list)
    
    recipes = load_recipes()
    for recipe in recipes:
        recipe_list.insert(tk.END, recipe["name"])
    
    root.mainloop()

if __name__ == "__main__":
    main()
