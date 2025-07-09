import tkinter as tk
from tkinter import messagebox, font
import os
import subprocess

LABS_DIR = "labs"

def run_script(script_path):
    if not os.path.exists(script_path):
        messagebox.showerror("Eroare", f"Fișierul nu există:\n{script_path}")
        return
    try:
        result = subprocess.run(["bash", script_path], capture_output=True, text=True)
        messagebox.showinfo("Rezultat", result.stdout or "Executat cu succes.")
    except Exception as e:
        messagebox.showerror("Eroare la execuție", str(e))

def open_flag(flag_path):
    if not os.path.exists(flag_path):
        messagebox.showerror("Flag lipsă", f"Nu există: {flag_path}")
        return
    with open(flag_path) as f:
        flag = f.read()
    messagebox.showinfo("FLAG", flag)

def prompt_and_run_command(ex_path):
    def execute_command():
        cmd = entry.get()
        try:
            result = subprocess.run(cmd, shell=True, capture_output=True, text=True, cwd=ex_path)
            messagebox.showinfo("Rezultat comandă", result.stdout or result.stderr or "Comandă executată.")

            # Rulează check.sh automat
            check_path = os.path.join(ex_path, "check.sh")
            if os.path.exists(check_path):
                check_result = subprocess.run(["bash", "check.sh"], capture_output=True, text=True, cwd=ex_path)
                messagebox.showinfo("Verificare", check_result.stdout or check_result.stderr)
        except Exception as e:
            messagebox.showerror("Eroare la rulare", str(e))

    cmd_window = tk.Toplevel()
    cmd_window.title("Execută o comandă în shell")
    cmd_window.geometry("600x150")
    tk.Label(cmd_window, text="Introdu comanda:", font=("Helvetica", 11)).pack(pady=10)
    entry = tk.Entry(cmd_window, width=80)
    entry.pack(pady=5)
    tk.Button(cmd_window, text="Rulează", command=execute_command).pack(pady=10)

def load_gui():
    root = tk.Tk()
    root.title("CTF Manager")
    root.geometry("900x600")
    root.configure(bg="#f0f0f0")

    header_font = font.Font(family="Helvetica", size=16, weight="bold")
    btn_font = font.Font(family="Helvetica", size=10)

    tk.Label(root, text="Alege un laborator și un exercițiu:", font=header_font, bg="#f0f0f0").pack(pady=15)


    canvas = tk.Canvas(root, borderwidth=0, background="#f0f0f0")
    scrollbar = tk.Scrollbar(root, orient="vertical", command=canvas.yview)
    scrollable_frame = tk.Frame(canvas, background="#f0f0f0")

    scrollable_frame.bind(
        "<Configure>",
        lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
    )

    canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
    canvas.configure(yscrollcommand=scrollbar.set)

    canvas.pack(side="left", fill="both", expand=True)
    scrollbar.pack(side="right", fill="y")

    def _on_mousewheel(event):
        canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")
    canvas.bind_all("<MouseWheel>", _on_mousewheel)

    row_index = 0
    for lab in sorted(os.listdir(LABS_DIR)):
        lab_path = os.path.join(LABS_DIR, lab)
        if not os.path.isdir(lab_path):
            continue

        lab_label = tk.Label(scrollable_frame, text=lab, font=("Helvetica", 12, "bold"), bg="#d0d0d0")
        lab_label.grid(row=row_index, column=0, sticky="w", pady=8, padx=5, columnspan=7)
        row_index += 1

        exs = sorted(os.listdir(lab_path))
        for ex in exs:
            ex_path = os.path.join(lab_path, ex)
            if not os.path.isdir(ex_path):
                continue

            col_index = 0

            ex_label = tk.Label(scrollable_frame, text=ex, font=("Helvetica", 11), bg="#f0f0f0")
            ex_label.grid(row=row_index, column=col_index, sticky="w", padx=5)
            col_index += 1

            for action in ["setup", "check", "reset"]:
                script_path = os.path.join(ex_path, f"{action}.sh")
                btn = tk.Button(
                    scrollable_frame, text=action.capitalize(),
                    font=btn_font,
                    width=8,
                    bg="#ffffff",
                    relief="raised",
                    command=lambda p=script_path: run_script(p)
                )
                btn.grid(row=row_index, column=col_index, padx=3, pady=5)
                col_index += 1

            # Buton Deschide FLAG
            flag_path = os.path.join(ex_path, "flag.txt")
            flag_btn = tk.Button(
                scrollable_frame, text="Deschide FLAG",
                font=btn_font,
                width=12,
                bg="#e1f5fe",
                relief="groove",
                command=lambda p=flag_path: open_flag(p)
            )
            flag_btn.grid(row=row_index, column=col_index, padx=8, pady=5)
            col_index += 1

            # Buton Rulează Comandă
            run_cmd_btn = tk.Button(
                scrollable_frame, text="Rulează Comandă",
                font=btn_font,
                width=14,
                bg="#d0ffd0",
                relief="groove",
                command=lambda p=ex_path: prompt_and_run_command(p)
            )
            run_cmd_btn.grid(row=row_index, column=col_index, padx=8, pady=5)

            row_index += 1

    root.mainloop()

if __name__ == "__main__":
    load_gui()
