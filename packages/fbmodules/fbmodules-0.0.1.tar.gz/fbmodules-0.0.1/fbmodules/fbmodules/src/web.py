from webbrowser import open_new_tab
from os import system

# Download files over http/https

def download_file(link: str):
    system(f'curl -O {link}')
    
# Open a link in a new tab

def open_link(link: str):
    open_new_tab(link)