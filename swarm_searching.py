from swarm_agents import *


def random_walk_only(pop_n, simulation_times=5, p=None, sense_food=False):
    time_step_ls = []
    movement_ls = []
    for n in range(simulation_times):
        time_step = 0
        movement = 0
        pop = [Ant(world) for _ in range(pop_n)]

        food_loc = set()

        while len(food_loc) < 89:
            time_step += 1
            movement += pop_n
            for ant in pop:
                food = ant.sense_food()
                if sense_food and food:
                    ant.forward()
                else:
                    if not p:
                        ant.random_walk(np.random.random()/2)
                    else:
                        ant.random_walk(p)
                    food_loc = food_loc.union(ant.location_food)


        time_step_ls.append(time_step)
        movement_ls.append(movement)

    return time_step_ls, movement_ls


def random_walk_v2(pop_n=None, start_n=1, simulation_times=5, sense_food=False):

    time_step_ls = []
    movement_ls = []
    pool_len = []

    if not pop_n:
        pop_n = np.inf

    for n in range(simulation_times):

        pool = [Ant(world) for _ in range(start_n)]

        food_loc = set()
        time_step = 0
        movement = 0

        while len(food_loc) < 89:
            time_step += 1
            movement += len(pool)

            for ant in pool:
                food = ant.sense_food()

                if sense_food and food:
                    print(food)
                    print(ant.position())
                    ant.forward()
                    print(ant.position())

                else:
                    ant.random_walk(np.random.random()/2)

                new_food_loc = ant.location_food - food_loc

                food_loc = food_loc.union(ant.location_food)


                if new_food_loc and len(pool) < pop_n:
                    pool.append(Ant(world))
                    pool[-1].row, pool[-1].col = new_food_loc.pop()


        pool_len.append(len(pool))
        movement_ls.append(movement)
        time_step_ls.append(time_step)

    return np.mean(time_step_ls), np.mean(pool_len), np.mean(movement_ls)


