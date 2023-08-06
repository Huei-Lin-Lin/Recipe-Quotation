from flask import Blueprint, render_template, request, jsonify
from .crawler.crawler import crawler


views = Blueprint('views', __name__)


@views.route('/')
def home():
    return render_template('home.html')


@views.route('/message', methods=['POST', 'GET'])
async def getInfo():
    if request.method == 'POST':
        cuisine = request.form['cuisine']
        headcount = request.form['headcount']
        quotation_data, update_recipe_data = await crawler(cuisine, headcount)

        result_data = dict()
        result_data.update({"估價": quotation_data})

        result_data.update({"料理食材": update_recipe_data['ingred_dict']})
        return jsonify(result_data)
    else:
        print(request.method)
        return jsonify({})
