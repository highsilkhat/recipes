from flask_app import app
from flask import render_template, redirect, request, session, flash
from flask_bcrypt import Bcrypt

from flask_app.models.user import User
from flask_app.models.recipe import Recipe
from flask_app.controllers import recipes


@app.route('/dashboard')
def dashboard():
    if 'user_id' not in session:
        flash('Please log in')
        return redirect('/')

    recipe_for_display = Recipe.get_all_recipes()

    return render_template('dashboard.html',  recipe_for_display=recipe_for_display)


@app.route('/recipes/new')
def new_recipe():
    if 'user_id' not in session:
        flash('Please log in')
        return redirect('/')
    return render_template('/new_recipe.html')


@app.route('/create/recipe', methods=['POST'])
def create_recipe():
    if 'user_id' not in session:
        flash('Please log in')
        return redirect('/')

    if not Recipe.recipe_validator(request.form):
        return redirect('/recipes/new')

    data = {
        'name': request.form['name'],
        'description': request.form['description'],
        'instructions': request.form['instructions'],
        'date': request.form['date'],
        'time': request.form['time'],
        'creator_id': session['user_id']
    }

    recipeId = Recipe.input_recipe(data)

    return redirect('/dashboard')


@app.route('/recipes/<int:recipe_id>')
def view_recipe(recipe_id):
    if 'user_id' not in session:
        flash('Please log in')
        return redirect('/')

    data = {
        'id': recipe_id
    }
    one_recipe = Recipe.get_one_recipe(data)

    return render_template('view_recipe.html', one_recipe=one_recipe)


@app.route('/recipes/edit/<int:recipe_id>')
def update_recipe(recipe_id):
    if 'user_id' not in session:
        flash('Please log in')
        return redirect('/')
    data = {
        'id': recipe_id
    }
    one_recipe = Recipe.get_one_recipe(data)

    return render_template('edit_recipe.html', one_recipe=one_recipe)


@app.route('/recipes/edit/post/<int:recipe_id>', methods=['POST'])
def post_update(recipe_id):
    print(request.form)

    if not Recipe.recipe_validator(request.form):
        return redirect(f'/recipes/edit/{recipe_id}')
        
    data={
        'id': recipe_id,
        'name': request.form['name'],
        'description': request.form['description'],
        'instructions': request.form['instructions'],
        'date': request.form['date'],
        'time': request.form['time'],
        'creator_id': session['user_id']
    }
    print(data)
    
    Recipe.revise_recipe(data)
    
    return redirect('/dashboard')

@ app.route('/recipes/delete/<int:recipe_id>')
def delete_recipe(recipe_id):
    if 'user_id' not in session:
        flash('Please log in')
        return redirect('/')
    data={
        'id': recipe_id
    }
    Recipe.remove_recipe(data)

    return redirect('/dashboard')
