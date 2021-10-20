# Copyright (c) 2021, Lemuria
# This code is licensed under the GNU GPL v3


from typing import Optional
import typer
import json
import random
import rich
import secrets
import planetcalcs as pcal
import os
import uuid

app = typer.Typer()

CONFIG = json.load(open('seed.json'))
FILE_FORMAT = CONFIG['config.OUTPUT_FORMAT']

PLANET_TYPES = CONFIG['planet-types']
GOVERNMENTS  = CONFIG['governments']

PLANET_SURVEYS = CONFIG['planet-surveys']
STAR_SURVEYS   = CONFIG['star-surveys']

if FILE_FORMAT == 'json':
    do_nothing = 0
elif FILE_FORMAT == 'csv':
    do_nothing = 0
else:
    raise Exception(f'File format {FILE_FORMAT} not supported, please use json/csv.')

import csv

# All the good stuff.

@app.command()
def stars(starstomake: int):
    
    stars   = []
    planets = []
    
    for i in range(starstomake):
        
        star_name = pcal.Name.star()
        star = pcal.Calc.star_make(star_name)
        stars.append(star)
        
        for pl in range(random.randint(4,16)):
            dfs = random.randint(230,450)
            habScore    = pcal.Calc.hab_score(distanceFromStar=dfs,star=star)
            planet_type = pcal.Calc.choosePlanet(int(habScore))
            planet_name = f'{star_name}.p{pl}'
            
            dfs += random.randint(65,150)
            
            planet = {'habScore':habScore, 'planetType':planet_type, 'name':planet_name, 'star':star_name}
            planets.append(planet)
            
    print('Stars generated. Now writing star data to disk.')
    
    dirname = f'query-{uuid.uuid4()}'
    
    os.mkdir(f'star-queries/{dirname}')
    with open(f'star-queries/{dirname}/stars.json','x') as f_stars:
        json.dump(stars, f_stars)
        print('Star data written to disk.')
        
    with open(f'star-queries/{dirname}/planets.json','x') as f_planets:
        json.dump(planets, f_planets)
        print('Planet data written to disk.')
        
    print('DONE')
    


# Star systems (legacy)
@app.command()
def legacy_stars(stars: Optional[int] = typer.Argument(10)):
    starid = CONFIG['stars-genned']
    j = []
    for i in range(stars):
        name = f'{random.choice(STAR_SURVEYS)} {starid}'
        x = {}
        x['planets']  = []
        x['name']     = name
        x['spectral'] = random.choice(CONFIG['star-types'])
        starid += 1
        planet_num = 1
        for i in range(random.randint(4,16)):
            planet_list = []
            planet_list.append(pcal.generatePlanet)
        j.append(x)
    with open(f'star-queries/{random.randint(1,100000)}.json','x') as f:
        json.dump(j,f)




# Generate random planets (legacy)
@app.command()
def legacy_planets(planets: Optional[int] = typer.Argument(500)):
    x = {}
    planetList = []
    for i in range(planets):
        x = {}
        num = random.randint(1,9999999999999999999)
        pop = random.randint(499500000,187500000000)
        govt            = random.choice(GOVERNMENTS)
        type_of_planet  = random.choice(PLANET_TYPES)
        planet_diameter = random.randint(14000,55000)
        #rich.print(f'[green][b]>[/b][/green] {random.choice(PLANET_SURVEYS)} {num: >12} {type_of_planet: >12} {pop: >16} {govt: >12}')
        x['name'] = f'LACOP.{random.randint(1,1000)}.{random.randint(1,999999999999999999)}.{secrets.token_hex(8)}'
        x['govt'] = govt
        x['planetType'] = type_of_planet
        x['population'] = pop
        planetList.append(x)
    json_query_file = f'stars-{secrets.token_urlsafe(16)}.json'
    with open(json_query_file,'x') as fileSave:
        rich.print('done')
        json.dump(planetList,fileSave)

# Manual
@app.command()
def man():
    manual = open('man.txt','r')
    print(manual.read())

if __name__ == "__main__":
    app()
