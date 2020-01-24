"""
nytimes cooking recipe scraper
"""
import os 
import sys 
import requests
from bs4 import BeautifulSoup 
# -- toga -- 
import toga
from toga.style import Pack
from toga.style.pack import COLUMN, ROW



class nytCook(toga.App):

    def startup(self):
        """
        Construct and show the Toga application.

        Usually, you would add your application to a main content box.
        We then create a main window (with a name matching the app), and
        show the main window.
        """
        main_box = toga.Box(style=Pack(direction=COLUMN))

        #url_label = toga.Label('recipe url: ', style=Pack(padding=(0, 5)))
        #self.url_input = toga.TextInput(style=Pack(flex=1))

        self.url_input = toga.MultilineTextInput(
                placeholder='Recipe URL',
                style=Pack(flex=1))

        self.recipe_input =  toga.MultilineTextInput(
                readonly=True,
                placeholder='Recipe URL',
                style=Pack(flex=1))

        #toga.TextInput(readonly=True)

        url_box = toga.Box(style=Pack(direction=ROW, padding=10))
        #url_box.add(url_label)
        url_box.add(self.url_input)

        button = toga.Button(
                'Get Recipe',
                on_press=self.get_recipe,
                style=Pack(padding=5)
                )
        
        recipe_container = toga.ScrollContainer(style=Pack(height=400, direction=COLUMN, padding=10),
                horizontal=False, vertical=False)
        recipe_box = toga.Box(style=Pack(width=600, height=400))
        recipe_box.add(self.recipe_input)
        recipe_container.content = recipe_box

        main_box.add(url_box)
        main_box.add(button)
        main_box.add(recipe_container)

        self.main_window = toga.MainWindow(title=self.formal_name)
        self.main_window.content = main_box
        self.main_window.show()

    def get_recipe(self, widget):
        self.recipe_input.value = self.scrape_recipe(self.url_input.value) 

    def scrape_recipe(self, url): 
        ''' scrape nyt url and get ingredients and instructions 
        '''
        r = requests.get(url) 
        soup = BeautifulSoup(r.content, 'html.parser')

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
        return recipe 


def main():
    return nytCook()
