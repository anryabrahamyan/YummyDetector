# Uncomment next line if you are executing the framework for the first time
# !pip install clarifai

from clarifai.rest import ClarifaiApp
from functools import reduce

class FoodDetector:  

    def __init__(self, filename):
        self.app = ClarifaiApp(api_key='4c7517bd377b4a418fffb9704d042e69')
        self.filename = filename
        self.model = self.app.models.get('food-items-v1.0')  # loads the clarifai's food-items prediction model
        self.response = self.model.predict_by_filename(
            filename)  # uses the food-items model to predict ingredient from the picture and outputs a json file.

    def get_components_with_prob(self):
        dc = {}
        exclude_words = ['dinner',
                         'meal',
                         'vegetable',
                         'food',
                         'lunch',
                         'no person',
                         'delicious',
                         'plate',
                         'dish',
                         'nutrition',
                         'bowl',
                         'appetizer',
                         'healthy',
                         'diet',
                         'epicure',
                         'health']  # excludes the outputs that are not ingredients

        for i in self.response["outputs"][0]["data"]["concepts"]:  # gets the ingredients dictionary from the json file 
            name = i["name"]
            prob = i['value']
            if name not in exclude_words:
                dc[name] = prob

        return dc  # returns a dictionary that contains the ingredients and their probabilities

    def ingredients(self):
        comp_dict = self.get_components_with_prob()
        return [k for k, v in comp_dict.items()]  # returns a list with only the ingredients

    def probability_correct_guess(self):  # returns the probability of each ingredient rounded to 2 digits

        components_dict = self.get_components_with_prob()
        probs = [val for key, val in components_dict.items()]

        return f"{round(reduce(lambda x, y: x * y, probs), ndigits=2) * 100}%"  
       

