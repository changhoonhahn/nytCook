import os 
import sys 
import urllib2
from bs4 import BeautifulSoup 


def scrapeRecipe(url): 
    ''' scrape nyt url and get ingredients and instructions 
    '''
    page = urllib2.urlopen(url)
    soup = BeautifulSoup(page, "html.parser")

    name = str(soup.find_all('h1', {'class': 'recipe-title title name'})[0])
    name = name.split('">')[1].split('<')[0].lstrip() 

    # ingredients 
    ingredients = [] 
    for i, k in enumerate(soup.find_all('li', {'itemprop': 'recipeIngredient'})[:-1]): 
        quant = str(k.find_all('span', {'class': 'quantity'})[0]).replace('\n', '').replace(' ', '') 
        quant = quant.split('>')[1].split('<')[0] 

        ing = k.find_all('span', {'class': 'ingredient-name'}) 
        ing = (str(ing[0]).replace('\n', '').split('">')[1].split('</')[0]).lstrip().rstrip() 
    
        
        if quant == '': ingredients.append('%s' % ing)
        else: ingredients.append('%s %s' % (quant, ing)) 

    # instructions 
    instructions = [] 
    instruct = str(soup.find_all('ol', {'class': 'recipe-steps'})[0]).split('\n')
    for ii, inst in enumerate(instruct[1:-1]): 
        instructions.append(inst.split('li>')[1].split('</')[0]) 
    return name, ingredients, instructions


def writeRecipe(url): 
    ''' write out ingredients and instructions 
    '''
    name, ingredients, instructions = scrapeRecipe(url) 
    ings = ['- %s' % ing for ing in ingredients]
    inst = ['%i. %s' % (i, instructions[i]) for i in range(len(instructions))]

    recipe = '\n'.join([
        '## %s' % name, 
        '### Ingredients',
        '\n'.join(ings),
        '', 
        '### Instructions',
        '\n'.join(inst)
        ]) 
    name_rec = nameRecipe(name) 

    frecipe = open(os.path.join(_dat_dir(), '%s.md' % name_rec), 'w') 
    frecipe.write(recipe)
    frecipe.close() 
    return None 


def nameRecipe(name): 
    ''' given full name return shortened name 
    '''
    if '(' in name: 
        name = name.split('(')[0] 
    return '_'.join(name.rstrip().lstrip().split(' ')).lower() 


def _dat_dir(): 
    # directory to download recipes 
    if os.environ.get('NYTCOOK_DIR') is None: 
        raise ValueError("set $NYTCOOK_DIR environment varaible!") 
    return os.environ.get('NYTCOOK_DIR') 


if __name__=="__main__": 
    writeRecipe('https://cooking.nytimes.com/recipes/1020203-kuku-sabzi-persian-herb-frittata') 
