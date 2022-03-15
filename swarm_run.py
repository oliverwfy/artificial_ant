from swarm_searching import *
import numpy as np
import matplotlib.pyplot as plt

# simulation times
simulation_times = 100
# font size
size = 13

file_name = 'fig/'


pop_n = np.arange(1,21,2)

time_rand_mean = []
time_rand_std = []
movement_rand_mean = []
movement_rand_std = []

for n in pop_n:

    time_step_ls, movement_ls  = random_walk_only(n, simulation_times=simulation_times)

    time_mean, time_std = np.mean(time_step_ls), np.std(time_step_ls)
    movement_mean, movement_std =  np.mean(movement_ls), np.std(movement_ls)

    time_rand_mean.append(time_mean)
    time_rand_std.append(time_std)

    movement_rand_mean.append(movement_mean)
    movement_rand_std.append(movement_std)



plt.figure()
plt.errorbar(pop_n, time_rand_mean, time_rand_std, ecolor='lightgray', elinewidth=2, capsize=1)
plt.xlabel('number of agents', fontsize=size)
plt.ylabel('convergence time', fontsize=size)
plt.legend(['p ~ Uni(0, 0.5)'], fontsize=size)
plt.savefig(file_name + 'v1_time.png')


plt.figure()
plt.errorbar(pop_n, movement_rand_mean, movement_rand_std, ecolor='lightgray', elinewidth=2, capsize=1)
plt.xlabel('number of agents', fontsize=size)
plt.ylabel('movement to reach convergence', fontsize=size)
plt.legend(['p ~ Uni(0, 0.5)'], fontsize=size)

plt.savefig(file_name + 'v1_movement.png')





plt.figure('v1_time')
plt.figure('v1_movement')
prob_ls = [0, 0.3, 0.5]

for p in prob_ls:

    time_mean = []
    time_std = []
    movement_mean = []
    movement_std = []
    for n in pop_n:

        time_step_ls, movement_ls  = random_walk_only(n, simulation_times=simulation_times)
        time_mean.append(np.mean(time_step_ls))
        movement_mean.append(np.mean(movement_ls))

    plt.figure('v1_time')
    plt.plot(pop_n, time_mean)

    plt.figure('v1_movement')
    plt.plot(pop_n, movement_mean)


plt.figure('v1_time')
plt.plot(pop_n, time_rand_mean)


legend = ['p='+ str(round(p, 2)) for p in prob_ls]
plt.xlabel('number of agents', fontsize=size)
plt.legend(legend+['p~Uni(0,0.5)'], fontsize=size)
plt.ylabel('convergence time', fontsize=size)


plt.savefig(file_name + 'v1_time_p.png')




plt.figure('v1_movement')
plt.plot(pop_n, movement_rand_mean)


legend = ['p = '+ str(round(p, 2)) for p in prob_ls]
plt.xlabel('number of agents', fontsize=size)
plt.legend(legend+['p~Uni(0,0.5)'], fontsize=size)
plt.ylabel('movement to reach convergence', fontsize=size)


plt.savefig(file_name + 'v1_movement_p.png')


# define the maximum number of ants
pop_n = np.linspace(10, 90, 9)

time_step_ls = []
movement_ls = []
pool_len_ls = []

time_step_rand_mean = []
movement_rand_mean = []


for n in pop_n:

    time_step, pool_len, movement = random_walk_v2(n, simulation_times=simulation_times)
    time_step_ls.append(time_step)
    pool_len_ls.append(pool_len)
    movement_ls.append(movement)

    time_step_rand_ls, movement_rand_ls  = random_walk_only(int(n), simulation_times=simulation_times)
    time_step_rand_mean.append(np.mean(time_step_rand_ls))
    movement_rand_mean.append(np.mean(movement_rand_ls))




plt.figure('v2_time')

plt.plot(pool_len_ls, time_step_rand_mean)
plt.plot(pool_len_ls, time_step_ls)

plt.xlabel('number of agents', fontsize=size)
plt.ylabel('convergence time', fontsize=size)
plt.legend(['V1', 'V2'], fontsize=size)

print('Random Walk V1\nThe minimum time to find all pieces of food is \n {}'.format(int(np.min(time_step_rand_mean))))
print('Random Walk V2\nThe minimum time to find all pieces of food is \n {}'.format(int(np.min(time_step_ls))))

plt.savefig(file_name + 'v2_time.png')


plt.figure('v2_movement')

plt.plot(pool_len_ls, movement_rand_mean)
plt.plot(pool_len_ls, movement_ls)

plt.xlabel('number of agents', fontsize=size)
plt.ylabel('movement to reach convergence', fontsize=size)
plt.legend(['V1', 'V2'], fontsize=size)

print('Random Walk V1\nThe minimum movement to find all pieces of food is \n {}'.format(int(np.min(movement_rand_mean))))
print('Random Walk V2\nThe minimum movement to find all pieces of food is \n {}'.format(int(np.min(movement_ls))))

plt.savefig(file_name + 'v2_movement.png')




# # define the number of ants at beginning
# start_n = np.arange(1, 10, 2)
#
# time_step_ls = []
# pool_len_ls = []
# movement_ls = []
#
#
# for init_n in start_n:
#     time_step, pool_len, movement = random_walk_v2(start_n=init_n, simulation_times=simulation_times)
#     time_step_ls.append(time_step)
#     movement_ls.append(movement)
#     pool_len_ls.append(pool_len)
#
# fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(15,15))
# plt.subplots_adjust(top = 0.9, bottom=0.1, hspace=0.6, wspace=0.2)
#
# ax1.plot(start_n, time_step_ls)
#
# ax1.set_xlabel('number of ants at beginning', fontsize=size)
# ax1.set_ylabel('convergence time', fontsize=size)
#
# ax2.plot(start_n, movement_ls)
# ax2.set_xlabel('number of ants at beginning', fontsize=size)
# ax2.set_ylabel('movement to reach convergence', fontsize=size)
#
# plt.savefig(file_name + 'init_n.png')
