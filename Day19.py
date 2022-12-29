import itertools
import multiprocessing as mp

geode_min ={}
geode_robots_min = {}
from functools import lru_cache, total_ordering


def find_blueprint_options(ore_robots, clay_robots, obsidian_robots, geode_robots, ore, clay, obsidian, geodes, current_time, blueprint,i):

    # if blueprint['clay_robot']['ore'] + blueprint['obsidian_robot']['clay'] + blueprint['geode_robot']['obsidian'] > 24:
    #     print(f'Blueprint {blueprint}, results {0}')
    #     return 0

    results  = d2(ore_robots, clay_robots, obsidian_robots, geode_robots, ore, clay, obsidian, geodes, current_time, blueprint,i)
    print(f'Blueprint {blueprint}, results {results}')
    return results


def d2(ore_robots, clay_robots, obsidian_robots, geode_robots, ore, clay, obsidian, geodes, current_time, blueprint,i):
        # print(f'NEW ROUND MINUTE: {current_time}')
        # print(f'ore_robots: {ore_robots}')
        # print(f'clay_robots: {clay_robots}')
        # print(f'obsidian_robots: {obsidian_robots}')
        # print(f'geode_robots: {geode_robots}')
        # print(f'ore: {ore}')
        # print(f'clay: {clay}')
        # print(f'obsidian: {obsidian}')
        # print(f'geodes: {geodes}')

        if geode_min.get((current_time,i),0)>geodes:
             return 0
        elif (current_time,i) in geode_min:
             geode_min[(current_time,i)] = max(geodes, geode_min[(current_time,i)]) 
        else:
             geode_min[(current_time,i)] = geodes

        if geode_robots_min.get((current_time,i),0) > geode_robots:
             return 0
        elif (current_time,i) in geode_robots_min:
             geode_robots_min[(current_time,i)] = max(geode_robots, geode_robots_min[(current_time,i)]) 
        else:
             geode_robots_min[(current_time,i)] = geode_robots


        if current_time == 25:
            return geodes

        #find what to mine.
        f_ore = ore + ore_robots
        f_clay = clay + clay_robots
        f_obsidian = obsidian + obsidian_robots
        f_geodes = geodes + geode_robots

        #find what to build
        buy_options = [(1,0,0,0),(0,1,0,0),(0,0,1,0), (0,0,0,1),(0,0,0,0)]

        if ore_robots >= 7:
            buy_options.remove((1,0,0,0))
        if clay_robots >= 8:
            buy_options.remove((0,1,0,0))
        if obsidian_robots >= 8:
            buy_options.remove((0,0,1,0))
    
        final_buy_options = []
        supplies_needed = {}
        for buy_option in buy_options:
            #print(buy_option)
            ore_needed = 0
            clay_needed = 0
            obs_needed = 0

            ore_needed +=  blueprint['ore_robot']['ore'] * buy_option[0] #ore robot

            ore_needed +=  blueprint['clay_robot']['ore'] * buy_option[1] #clay robot

            ore_needed +=  blueprint['obsidian_robot']['ore'] * buy_option[2] #obsidian_robot
            clay_needed += blueprint['obsidian_robot']['clay'] * buy_option[2] #obsidian_robot

            ore_needed +=  blueprint['geode_robot']['ore'] * buy_option[3] #obsidian_robot
            obs_needed +=  blueprint['geode_robot']['obsidian'] * buy_option[3] #obsidian_robot

            
            if ore_needed <= ore and clay_needed <= clay and obs_needed <= obsidian:
                supplies_needed[buy_option] = {'ore': ore_needed, 'clay': clay_needed, 'obs': obs_needed}
                final_buy_options.append(buy_option)

        #get best results for all these buy options
        results = []
        final_buy_options = sorted(final_buy_options, key=lambda x: (x[3], x[2], x[1], x[0]), reverse=True)
        for buy_options in final_buy_options:
            results.append(
            d2(ore_robots + buy_options[0], 
            clay_robots + buy_options[1], 
            obsidian_robots + buy_options[2], 
            geode_robots + buy_options[3], 
            f_ore - supplies_needed[buy_options]['ore'], 
            f_clay - supplies_needed[buy_options]['clay'], 
            f_obsidian - supplies_needed[buy_options]['obs'], 
            f_geodes,
            current_time + 1,
            blueprint,
            i
            )) 

        #print (f'Blueprint: {blueprint}, results {max(results)}') 
        return max(results)

if __name__ == '__main__':
    with open('inputs/day19.txt') as f:
        file = f.read()

        ore_robots = 1
        clay_robots = 0
        obsidian_robots = 0
        geode_robots = 0

        ore = 0
        clay = 0
        obsidian = 0
        geodes = 0

        
        #results = find_blueprint_options(ore_robots, clay_robots, obsidian_robots, geode_robots, ore, clay, obsidian, geodes, 1)

        results = []
        args = []
        i = 1
        for line in file.split('\n'):
            #print(line.split('Each'))
            geode_min ={}
            blueprint = {
                'ore_robot' : {'ore': int(line.split('Each')[1].split()[3])},
                'clay_robot': {'ore': int(line.split('Each')[2].split()[3])},
                'obsidian_robot':{'ore':int(line.split('Each')[3].split()[3]), 'clay':int(line.split('Each')[3].split()[6])},
                'geode_robot':{'ore':int(line.split('Each')[4].split()[3]), 'obsidian':int(line.split('Each')[4].split()[6])}
            }

            #print(blueprint)
            #results.append(find_blueprint_options(ore_robots, clay_robots, obsidian_robots, geode_robots, ore, clay, obsidian, geodes, 1,blueprint))
            args.append((ore_robots, clay_robots, obsidian_robots, geode_robots, ore, clay, obsidian, geodes, 1,blueprint, i))
            i+=1

        with mp.Pool(4) as p:
            results = p.starmap(find_blueprint_options, args)
        
        print(results)
