from webbrowser import open_new_tab

# Open a list of steam links

def open_steam_link(games: list):
    for game in games:
        open_new_tab(f'steam://run/{game}')

