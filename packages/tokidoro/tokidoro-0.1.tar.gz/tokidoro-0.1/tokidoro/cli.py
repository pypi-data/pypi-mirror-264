#!/usr/bin/env python3
import click
import os,sys
from rich import print
from rich.console import Console
import time
from datetime import datetime
from playsound import playsound
import json
import shutil


@click.group()
def cli():
    pass

# Terminal width for output designing.
terminal_width=int(shutil.get_terminal_size().columns)

# =============functions to load a save configuration files=============
def load_config(file):
    try:
        with open(file,"r") as f:
            return json.load(f)
    except FileNotFoundError:
        return None
def save_config(file,config):
    with open(file,"w") as f:
        json.dump(config,f)

# ============= function to update and save both the configuration files at the beginning  =============
def update_json():
    config = load_config(os.path.join(os.path.dirname(__file__), "config.json"))
    directory = os.path.join(os.path.dirname(__file__), "sounds")
    files = os.listdir(directory)   
    data = {str(i+1): os.path.join(os.path.dirname(__file__), "sounds", file) for i, file in enumerate(files)}
    with open(os.path.join(os.path.dirname(__file__), "audio.json"), 'w') as f:
        json.dump(data,f,indent=4)
    if directory:
        if not os.listdir(directory):
            click.echo('Please save an audio file in the sounds directory')
            sys.exit()
    if str(config["a"]) not in data:
        config["a"]="1"
    save_config((os.path.join(os.path.dirname(__file__), "config.json")),config)
    
update_json()

# =============function to play given audio, given number of times =============
def play_sound(audio, count):
    audioconfig = load_config(os.path.join(os.path.dirname(__file__), "audio.json"))
    audio_path = audioconfig[str(audio)]
    for i in range(count):
        playsound(audio_path)
        
    
# ============= Timer Duration  =============
def timer(duration):
    while duration > 0:
        m, s = divmod(duration, 60)
        timer_str = "{:02d}:{:02d}".format(int(m), int(s))
        print(timer_str,end='\r')
        time.sleep(1)
        duration -= 1


# ============= COMMANDS FOR TOKIDORO =============
@click.command()
@click.option('-d',prompt='Duration of the pomodoro ',type=float)
@click.option('-s',prompt='Duration of short break',type=float)
@click.option('-l',prompt='Duration of the long break',type=float)
@click.option('-c',prompt='Number of cycles',type=float)
@click.option('-a',prompt='Serial no. of the audio',type=int)
@click.option('-r',prompt='Number of times you want the audio to repeat',type=int)
def configure(d,s,l,c,a,r):
    update_json()
    config = load_config(os.path.join(os.path.dirname(__file__), "config.json")) or {"d":25,"s":5,"l":15,"c":4,"a":1,"r":3}
    if d:
        config["d"]=d
    if s:
        config["s"]=s
    if l:
        config["l"]=l
    if c:
        config["c"]=c
    if a:
        config["a"]=a
    if r:
        config["r"]=r
    save_config((os.path.join(os.path.dirname(__file__), "config.json")),config)
    update_json()
    print("Configuration saved successfully")


@cli.command()
@click.option('-d', '--duration',default=None, help='Duration of pomodoro in minutes', type=float)
@click.option('-s', '--short',default=None, help='Duration of short break in minutes', type=float)
@click.option('-l', '--long',default=None, help='Duration of long break in minutes', type=float)
@click.option('-c', '--cycles',default=None, help='Number of pomodoro cycles',type=int)
@click.option('-a','--audio',default=None,help='Serial number of the audio',type=int)
@click.option('-r','--repeat',default=None,help='The number of times the audio needs to repeat',type=int,required=0)
def start(duration, short, long, cycles,audio,repeat):
    config=load_config((os.path.join(os.path.dirname(__file__), "config.json"))) or {"d":25, "s":5,"l":15,"c":4,"a":1,"r":3}
    if duration is None:
        duration=(config["d"])
    if short is None:
        short=(config["s"])
    if long is None:
        long=(config["l"])
    if cycles is None:
        cycles=int(config["c"])
    if audio is None:
        audio=int(config["a"])
    if repeat is None:
        repeat=int(config["r"])
    while True:
        for cycle in range(1, int(cycles) + 1):
            print("─"*int((terminal_width/2)-10),end='')
            print(f"[#ff85ed]Pomodoro Cycle:[/#ff85ed] {cycle}/{cycles}",end='')
            print("─"*int((terminal_width/2)-9))
            timer(duration * 60)
            play_sound(audio,repeat)
            if cycle < int(cycles):
                print("[#0ff0fc]Short Break![/#0ff0fc]")
                timer(short * 60)
                play_sound(audio,repeat)
                print("-"*(terminal_width-17),end='')
                print(f"Ended at {datetime.now().strftime('%I:%M %p')}")
            else:
                print("[blue]Long Break !![/blue]")
                timer(long * 60)
                play_sound(audio,repeat)
                print("-"*(terminal_width-17),end='')
                print(f"Ended at {datetime.now().strftime('%I:%M %p')}")
        new=input("do you want to start over? : (y/n) ")
        if new=="n":
            break
        
@click.command()
def showconfig():
    update_json()
    with open(os.path.join(os.path.dirname(__file__), "audio.json"),'r') as f:
        data=json.load(f)
    config=load_config(os.path.join(os.path.dirname(__file__), "config.json"))
    audio=load_config(os.path.join(os.path.dirname(__file__), "audio.json"))
    console=Console()
    
    directr=(os.path.join(os.path.dirname(__file__), "sounds"))
    directrln=len(directr)
    config_string = "\n".join([
    f"Pomodoro duration       : {config['d']}",
    f"Short break duration    : {config['s']}",
    f"Long break duration     : {config['l']}",
    f"Number of cycles        : {config['c']}",
    f"Current audio           : {audio[str(config['a'])][directrln+1:]}",
    f"Repeat audio            : {config['r']}"
])
    console.print("[bold white]Configuration:[/bold white]")
    console.print("┌" + "─" * (terminal_width-2) + "┐", style="blue")  
    for line in config_string.split('\n'):
        console.print(f"│ {line:<{terminal_width-4}} │", style="blue")
    console.print(f"│ {'[white]Audio List[/white]':<{terminal_width+11}} │", style="blue")
    for number,path in data.items():
         console.print(f"│ {number} {path[directrln+1:]:<{terminal_width-5}}│", style="blue")
    console.print("└" + "─" * (terminal_width-2) + "┘", style="blue")
    


cli.add_command(start)
cli.add_command(configure)
cli.add_command(showconfig)
if __name__ == "__main__":
    cli()
