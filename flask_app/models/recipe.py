from flask_app.config.mysqlconnection import MySQLConnection, connectToMySQL
from flask import flash
import re
from flask_app.models import user

class Recipe: 
    def __init__(self, data): 
        self.id = data['id']
        self.name = data['name']
        self.description = data['description']
        self.instructions = data['instructions']
        self.time = data['time']
        self.date = data['date']
        self.created_at =  data['created_at']
        self.updated_at = data['updated_at']
        self.creator_id = data['creator_id']

    @classmethod
    def input_recipe(cls, data):
        query = "INSERT INTO recipes (name, description, instructions, time, date, creator_id) VALUES(%(name)s, %(description)s, %(instructions)s, %(time)s, %(date)s, %(creator_id)s);"

        results = connectToMySQL('recipes_schema').query_db(query, data)

        return results
    
    @classmethod
    def get_all_recipes(cls):

        query = "SELECT * FROM recipes"

        results = connectToMySQL('recipes_schema').query_db(query)

        recipes = []

        for item in results:
            recipes.append(Recipe(item))

        print (recipes)
        return recipes

    @classmethod
    def get_one_recipe(cls, data):
        query = "SELECT * FROM recipes WHERE id = %(id)s"

        results = connectToMySQL('recipes_schema').query_db(query, data)
        recipe = Recipe(results[0])
        print (recipe.date)
        return recipe 

    @classmethod
    def revise_recipe(cls, data):
        query = "UPDATE recipes SET name = %(name)s, description = %(description)s, instructions = %(instructions)s, time = %(time)s, date = %(date)s WHERE id = %(id)s;"

        connectToMySQL('recipes_schema').query_db(query, data)

    @classmethod
    def remove_recipe(cls,data):
        query = "DELETE FROM recipes WHERE id = %(id)s;"

        connectToMySQL('recipes_schema').query_db(query, data)

    @staticmethod
    def recipe_validator(data):

        is_valid= True

        if len(data['name']) < 2 or len(data['name']) > 45:
            is_valid = False
            flash('Meal name must be between 2 and 45 characters')

        if len(data['description']) < 5:
            is_valid = False
            flash("Help your fellow chefs out a bit. Describe the dish in more detail.")

        if len(data['instructions']) < 5:
            is_valid = False
            flash("That's it? Please help us know how to properly cook this dish.")
        

        if len(data['date']) < 10:
            is_valid = False
            flash('Please choose a valid date')

        return is_valid