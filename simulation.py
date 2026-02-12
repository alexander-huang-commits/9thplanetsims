import rebound
import numpy as np
import matplotlib.pyplot as plt

from tqdm import tqdm

import argparse
import os


parser = argparse.ArgumentParser()
parser.add_argument("--job_id", type=int, required=False)
parser.add_argument("--outdir", type=str, required=False)
parser.add_argument("--time_step", type=str, required =True)
parser.add_argument("--total_time", type=str, required =True)
parser.add_argument("--archive_interval", type=str, required =True)
args = parser.parse_args()

job_id = args.job_id
outdir = args.outdir
int_time_step = int(float(args.time_step))
int_total_time = int(float(args.total_time))
int_archive_interval = int(float(args.archive_interval))


class SyntheticDisk:
    tnos = []

    def __init__(self,num=10, amin = 50, amax = 550, qmin = 30, qmax = 50): # 400, a e [50,550], q e [30,50]
        for i in range(num):
            a = np.sqrt(np.random.rand()*(amax**2-amin**2)+amin**2)
            q = np.random.uniform(qmin,qmax)
            w = np.random.uniform(0,2*np.pi)
            self.tnos.append((a,q,w))

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
        w = i[2]
        e = 1-q/a
        sim.add(m=0,a=a,e=e,omega=w)


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
    add_P9(sim)


def save_image(iter,sim,now,tot):
    snapshot = rebound.OrbitPlot(sim)
    snapshot.fig.savefig(f"{outdir}/{int(now)}_orbit_plot.png") #MAKECHANGE
    print(f"{iter}th snapshot saved, it is year {int(now)} out of {tot}!")

#vibe code recommended save style with npz |notes on code are mine
times = []
#These become lists of lists. So a_hist[0] is the semimajor axes of the particles in order. so each one is supposed to correspond to time slot
a_hist     = []
e_hist     = []
inc_hist   = []
Omega_hist = []
omega_hist = []

def update_elements_list(sim):
    sim.move_to_com()

    orbits = sim.particles[1::]

    times.append(sim.t)

    a_hist.append([o.a for o in orbits])
    e_hist.append([o.e for o in orbits])
    inc_hist.append([o.inc for o in orbits])
    Omega_hist.append([o.Omega for o in orbits])
    omega_hist.append([o.omega for o in orbits])

#my code again

def save_sim(sim,time_step):
    sim.save_to_file(f"{outdir}/archive.bin", interval=time_step) 

def simulate_and_save(sim,timestep,total_time,archive):
    save_sim(sim,archive)
    loop = np.arange(0,total_time+100,timestep)

    for i, x in tqdm(enumerate(loop)):
        save_image(i,sim,x,total_time)
        update_elements_list(sim)
        sim.integrate(timestep)

        #vibes
        if i % 250 == 0:
            print(f"Saving snapshot at {x} out of {total_time} years.")
            np.savez(
            f"{outdir}/orbits.npz",
            t=np.array(times),
            a=np.array(a_hist),
            e=np.array(e_hist),
            inc=np.array(inc_hist),
            Omega=np.array(Omega_hist),
            omega=np.array(omega_hist),
            units=dict(time="yr", length="AU", angle="rad")
            )
    
    #vibes
    np.savez(
    f"{outdir}/orbits.npz",
    t=np.array(times),
    a=np.array(a_hist),
    e=np.array(e_hist),
    inc=np.array(inc_hist),
    Omega=np.array(Omega_hist),
    omega=np.array(omega_hist),
    units=dict(time="yr", length="AU", angle="rad")
    )
    #not vibes




sim = rebound.Simulation()
initialize(sim)





#vibe code selecting integrator 

#good inbetween for speed and close encounters (because we have close encounters wiht neptune for scattering kelperian integrator which is default is bad)
sim.integrator = "mercurius"
sim.dt = .296 #1/40 of Jupiter the most inner planet's gravity
sim.testparticle_type = 1 #don't calculate test mass's gravitational interactions m=0 doesn't stop it from being in loop
sim.move_to_com()
sim.ri_whfast.corrector = 11 #don't know yet
sim.ri_mercurius.hillfac = 3 #don't know yet

TNOS = SyntheticDisk(num = 20).tnos
add_disk_to_sim(TNOS,sim)


#vibe code HPC
N_per_job = 20
start = job_id * N_per_job
end = start + N_per_job

print(f"Job {job_id}: simulating particles {start} -> {end-1}")
print(f"Output directory: {outdir}")


#my code again

simulate_and_save(sim,int_time_step,int_total_time,int_archive_interval)

#vibe
#how to load stuff data = np.load("orbits.npz", allow_pickle=True)
# a = data["a"]