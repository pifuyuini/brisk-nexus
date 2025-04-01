"""
Welcome Screen for SSH Login - Rich-based Terminal UI

This script generates a colorful, motivational welcome screen when logging into a server via SSH.
It displays a large gradient-style welcome banner, current Beijing time, server resource status,
and a randomly selected motivational quote. Designed for use with Python Rich and pyfiglet.

Dependencies:
- rich
- pyfiglet
- psutil

Author: Your Name (YSY)
"""

import datetime
import random
import psutil
from rich.console import Console
from rich.text import Text
from rich.align import Align
from pyfiglet import Figlet

console = Console()

def gradient_text_centered(text, colors):
    """
    Render a multi-line ASCII text string with a horizontal RGB gradient,
    and center each line in the terminal using Rich formatting.

    Args:
        text (str): Multi-line ASCII text to display.
        colors (list of tuple): Two RGB tuples representing the start and end of the gradient.
    """
    lines = text.splitlines()
    result = []

    for line in lines:
        line_text = Text()
        length = len(line)
        for i, char in enumerate(line):
            # Linear interpolation between the two RGB colors
            r1, g1, b1 = colors[0]
            r2, g2, b2 = colors[1]
            r = int(r1 + (r2 - r1) * i / max(length - 1, 1))
            g = int(g1 + (g2 - g1) * i / max(length - 1, 1))
            b = int(b1 + (b2 - b1) * i / max(length - 1, 1))
            line_text.append(char, style=f"rgb({r},{g},{b}) bold")
        result.append(Align.center(line_text))
    
    for line in result:
        console.print(line)

def print_big_welcome():
    """
    Print a large stylized ASCII "Welcome, YSY!" banner using pyfiglet,
    with a smooth RGB color gradient and centered alignment.
    """
    fig = Figlet(font='slant')
    ascii_banner = fig.renderText("Welcome, YSY!")
    gradient_text_centered(ascii_banner, [(255, 139, 77), (90, 255, 204)])

def get_beijing_time():
    """
    Return the current time in Beijing (UTC+8) formatted as a string.

    Returns:
        str: Formatted time string with a clock emoji.
    """
    utc_now = datetime.datetime.utcnow()
    beijing_time = utc_now + datetime.timedelta(hours=8)
    return f"🕓 Login Time (Beijing): {beijing_time.strftime('%Y-%m-%d %H:%M:%S')}"

def get_server_status():
    """
    Retrieve current server status, including CPU, memory, and disk usage.

    Returns:
        str: A formatted status string with usage percentages.
    """
    cpu = psutil.cpu_percent(interval=0.5)
    mem = psutil.virtual_memory().percent
    disk = psutil.disk_usage('/').percent
    return f"💻 Server Status: CPU {cpu:.0f}%, Mem {mem:.0f}%, Disk {disk:.0f}%"

def random_quote():
    """
    Select a random motivational or inspirational quote (English or Chinese).

    Returns:
        str: A randomly selected quote.
    """
    quotes = [
        "✨ You are braver than you believe.",
        "✨ 今天依旧天气晴朗。",
        "✨ Everything you can imagine is real.",
        "✨ Make it happen, shock everyone.",
        "✨ 你已经走得很远，不要停下。",
        "✨ Do one thing every day that scares you.",
        "✨ 宇宙会回应你的坚定。",
        "✨ Never stop exploring.",
        "✨ 星光不问赶路人，时光不负有心人。",
        "✨ 每一次努力，都是幸运的伏笔。",
        "✨ 博观而约取，厚积而薄发。",
        "✨ 行百里者半九十，慎终如始则无败事。",
        "✨ 锲而不舍，金石可镂；绳锯木断，水滴石穿。",
        "✨ 仰天大笑出门去，我辈岂是蓬蒿人。",
        "✨ 千磨万击还坚劲，任尔东西南北风。",
        "如果我们选择了最能为人类而工作的职业，那么，重担就不能把我们压倒，因为这是为大家作出的牺牲；那时我们所享受的就不是可怜的、有限的、自私的乐趣，我们的幸福将属于千百万人，我们的事业将悄然无声地存在下去，但是它会永远发挥作用，而面对我们的骨灰，高尚的人们将洒下热泪。",
    ]
    return random.choice(quotes)

def print_colorful_info_centered():
    """
    Print three centered lines to the terminal:
    1. Current Beijing time (cyan)
    2. Server status (magenta)
    3. A motivational quote (yellow)
    """
    time_text = Align.center(Text(get_beijing_time(), style="bold cyan"))
    status_text = Align.center(Text(get_server_status(), style="bold magenta"))
    quote_text = Align.center(Text(random_quote(), style="bold yellow"))

    console.print(time_text)
    print()
    console.print(status_text)
    print()
    console.print(quote_text)

if __name__ == "__main__":
    print()
    print_big_welcome()
    print()
    print_colorful_info_centered()
    print()
