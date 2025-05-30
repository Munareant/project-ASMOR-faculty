import psutil
import matplotlib
matplotlib.use('TkAgg')
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import logging
import datetime

logging.basicConfig(
    filename='log.txt',
    level=logging.WARNING,
    format='%(asctime)s - ALARMA - %(message)s'
)

PRAG_CPU = 90
PRAG_RAM = 90
puncte_maxime = 60

valori_cpu = []
valori_ram = []
timpuri = []

def verifica_prag(nume_componenta, valoare):
    if nume_componenta == "CPU" and valoare >= PRAG_CPU:
        print(f"[ALARMA] CPU a ajuns la {valoare:.2f}%")
        logging.warning(f"CPU a depasit pragul: {valoare:.2f}%")
    elif nume_componenta == "RAM" and valoare >= PRAG_RAM:
        print(f"[ALARMA] RAM a ajuns la {valoare:.2f}%")
        logging.warning(f"RAM a depasit pragul: {valoare:.2f}%")

def actualizeaza(frame):
    utilizare_cpu = psutil.cpu_percent(interval=None)
    utilizare_ram = psutil.virtual_memory().percent
    ora_curenta = datetime.datetime.now().strftime('%H:%M:%S')

    verifica_prag("CPU", utilizare_cpu)
    verifica_prag("RAM", utilizare_ram)

    timpuri.append(ora_curenta)
    valori_cpu.append(utilizare_cpu)
    valori_ram.append(utilizare_ram)

    if len(valori_cpu) > puncte_maxime:
        valori_cpu.pop(0)
        valori_ram.pop(0)
        timpuri.pop(0)

    ax.clear()
    ax.plot(range(len(valori_cpu)), valori_cpu, label='CPU (%)', color='blue')
    ax.plot(range(len(valori_ram)), valori_ram, label='RAM (%)', color='green')
    ax.set_ylim(0, 100)
    ax.set_ylabel('Utilizare (%)')
    ax.set_title('Monitorizare in timp real a resurselor')
    ax.set_xticks(range(len(timpuri)))
    ax.set_xticklabels(timpuri, rotation=45, ha='right')
    ax.legend()
    ax.grid(True)

psutil.cpu_percent(interval=None)
fig, ax = plt.subplots()
ani = animation.FuncAnimation(fig, actualizeaza, interval=1000, cache_frame_data=False)
plt.tight_layout()
plt.show()
try:
    plt.tight_layout()
    plt.show()
except KeyboardInterrupt:
    print("Monitorizarea a fost întreruptă manual.")
