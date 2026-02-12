import rebound
import numpy as np
import matplotlib.pyplot as plt

from tqdm import tqdm
class SyntheticDisk:
    tnos = []

    def __init__(self,num=10, amin = 50, amax = 550, qmin = 30, qmax = 50): # 400, a e [50,550], q e [30,50]
        for i in range(num):
            a = np.random.uniform(amin,amax)
            q = np.random.uniform(qmin,qmax)
            self.tnos.append((a,q))

    def get_tnos(self):
        return self.tnos
    
    def add(self,a,q):
        self.tnos.append((a,q))

    def get(self,i):
        return self.tnos[i]
    

def add_disk_to_sim(disk,sim):
    for i in disk:
        a = i[0]
        q = i[1]

        e = 1-q/a
        sim.add(m=0,a=a,e=e)


def make_solar_system(sim):
    rebound.data.add_outer_solar_system(sim)

    sim.remove(5)

    sim.move_to_com() #does it once 

def print_semimajor_axes(sim):
    for i, p in enumerate(sim.particles):
        if i != 0:
            print(f"{i}th particle with semimajor axis of: {p.a}")

def add_P9(sim):
    sim.add(a = 700, e = .6, m = 3.0033e-5)


#start of code

def initialize(sim):

    make_solar_system(sim)
    TNOS = SyntheticDisk(num = 20).tnos
    add_disk_to_sim(TNOS,sim)
    add_P9(sim)

def save_image(iter,sim,now,tot):
    snapshot = rebound.OrbitPlot(sim)
    snapshot.fig.savefig(f"./plot_saves/{int(now)}_orbit_plot.png")
    print(f"{iter}th snapshot saved, it is year {int(now)} out of {tot}!")

def save_sim(sim,time_step):
    sim.save_to_file("archive.bin", interval=time_step) 

def simulate_and_save(sim,timestep,total_time,archive):
    save_sim(sim,archive)
    loop = np.arange(0,total_time+100,timestep)

    for i, x in tqdm(enumerate(loop)):
        save_image(i,sim,x,total_time)
        sim.integrate(timestep)



sim = rebound.Simulation()
initialize(sim)

simulate_and_save(sim,1e5,1e6,1e3)



