from os import system, getlogin
from ruamel.yaml import YAML
import shutil
from ctypes import windll
import sys
from winotify import Notification, audio

# Enable Windows Feature

def enable_windows_feature(feature_name: str):
    system(f'dism /Online /Enable-Feature /{feature_name}')
    
# Disable Windows Feature

def enable_windows_feature(feature_name: str):
    system(f'dism /Online /Disable-Feature /{feature_name}')

# Enable Windows Hibernation

def enable_windows_hibernation():
    system('powercfg /hibernate on')

# Disable Windows Hibernation

def disable__windows_hibernation():
    system('powercfg /hibernate off')
    
# Load Yaml

def load_yaml(file: str):
    yaml = YAML(typ='safe')
    with open(file, 'r', encoding='utf-8') as yaml_file:
        yaml_data = yaml.load(yaml_file)
    return yaml_data

# Run command

def run_command(command: str):
    system(command)
    
# Change owner

def change_owner(path: str, user: str=None, group: str=None):
    shutil.chown(path, user, group)
    
# get current user

def get_current_user():
    getlogin()
    
# Check for admin

def check_for_admin():
    try:
        return windll.shell32.IsUserAnAdmin()
    except:
        return False
    
# Get admin

def get_admin():
    return windll.shell32.ShellExecuteW(None, "runas", sys.executable, " ".join(sys.argv), None, 1)
    
# Help dialog

def help_dialog(title: str, text: str, icon: str):
    windll.shell32.ShellAboutA(None, title, text, icon)

# Check if internet is offline

def is_offline():
    return windll.shell32.InetIsOffline(None)

# Windows messagebox

def windows_messagebox(title: str, message: str, type: str):
    # Logic for the type of messagebox
    ws_ex = ''
    return windll.user32.MessageBoxExW(None, message, title, ws_ex)

# Windows notifications

def windows_notifications(app_id:str, title: str, msg: str, icon: str=None):
    notification = Notification(app_id, title, msg, icon)
    notification.set_audio(audio.Default, loop=False)
    notification.show()


