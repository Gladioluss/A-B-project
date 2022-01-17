import cgi
import os
import tkinter

import requests
import shutil
import glob


from tqdm import tqdm
from pathlib import Path
from tkinter import filedialog
from tkinter import *
from tkinter import messagebox as mbox
from tkinter.ttk import Frame, Button

folder_path = ''


def browse_button():
    filename = filedialog.askdirectory()
    global folder_path
    folder_path = filename


def download_file_and_get_path(url):

    buffer_size = 1024
    response = requests.get(url, stream=True)
    file_size = int(response.headers.get("Content-Length", 0))

    default_filename = url.split("/")[-1]

    content_disposition = response.headers.get("Content-Disposition")
    if content_disposition:
        value, params = cgi.parse_header(content_disposition)

        filename = params.get("filename" + ".exe", default_filename)
    else:
        filename = default_filename + ".exe"
    progress = tqdm(response.iter_content(buffer_size), f"Загрузка {filename}", total=file_size, unit="B",
                    unit_scale=True, unit_divisor=1024)
    with open(filename, "wb") as f:
        for data in progress.iterable:
            f.write(data)
            progress.update(len(data))
    return os.path.abspath(filename)


def find_file_with_urls(path):
    os.chdir(path)
    for file in glob.glob("*.txt"):
        if "ReadMe" not in file:
            return "\\" + file


def pars_file_with_urls():
    path = os.path.abspath(os.curdir)
    file_path = path + find_file_with_urls(path)

    list_installer_names = []
    with open(file_path, "r") as file_with_urls:
        for url in file_with_urls:
            list_installer_names.append(download_file_and_get_path(url.rstrip()))
    return list_installer_names


def main():
    root = Tk()
    root.title("Select download directory")
    root.geometry("200x150")
    lbl1 = Label(master=root, textvariable=folder_path)
    lbl1.grid(row=0, column=1)
    button = Button(text="Select directory", command=browse_button, width=29)
    button.grid(row=1, column=3)
    button_enter = Button(root, text="Продолжить", command=root.quit)
   # button_enter.grid(row=10, column=3)
    button_enter.place(relx=.3, rely=.7)
    mainloop()
    path_folder_apps = Path(folder_path)

    list_installer_names = pars_file_with_urls()
    for name in list_installer_names:
        path_folder_apps.mkdir(parents=True, exist_ok=True)
        shutil.move(name, path_folder_apps)


if __name__ == "__main__":
    main()
