import pandas as pd
from datetime import datetime

class NutritionCounter:
    """The class has methods to calculate different nutrition values of a given list of food"""
    nutritionsDF = pd.read_csv("database_food_converted.csv", index_col = 0) # the database of nutrition values
    
    def __init__(self, list_of_foods):
        self.list_of_foods = list_of_foods
    
    def get_total_nutritions(self):
        """
        The main output function of this class. 
        Returns the dictionary containing values for each of respective nutritions
        """
        
        return {"Calories / kJ": self.get_calories(total = True),
                "Protein / g": self.get_protein(total = True),
                "Carbohydrate / g": self.get_carbon(total = True),
                "Fat / g": self.get_fat(total = True)}

    def get_parameter_META(self, parameter, quantity, is_total = False):
    
        """ Returns either dictionary with nutrition data about each ingredient or a total number of it
        parameter and quantity: String -- are the nutrition name and quantity,
        is_total: Bool -- specifies the output type
        The function gets the values from the database
        """

        dict_param={}
        params = []
        params_nested = []

        for foodtype in self.list_of_foods:
            params = [NutritionCounter.nutritionsDF[parameter][i] for i in range(len(NutritionCounter.nutritionsDF)) if foodtype in NutritionCounter.nutritionsDF.index[i]]
            params_nested.append(params)
        
        for ind, foodtype in enumerate(self.list_of_foods):
            if len(params_nested[ind]) != 0:
                dict_param[foodtype] = round((sum(params_nested[ind])/len(params_nested[ind])) / (len(self.list_of_foods) * 0.5), ndigits = 3)
            
        if is_total == False: # returns dictionary with food type as keys and nutrition values as values
            return dict_param
        else: # returns dictionary with nutrition name as key and the total nutrition values of all the food as dictionary value
            return sum([v for k,v in dict_param.items()]) 

    
    def get_calories(self, total = False): # returns calory values of given instance of a class
        return self.get_parameter_META(parameter = "calories", quantity = "kJ", is_total = total)
    
    def get_fat(self, total = False): # returns fat values of given instance of a class
        return self.get_parameter_META(parameter = "total_fat", quantity = "g", is_total = total)
        
    def get_protein(self, total = False): # returns protein values of given instance of a class
        return self.get_parameter_META(parameter = "protein", quantity = "g", is_total = total)
        
    def get_water(self, total = False): # returns calory water of given instance of a class
        return self.get_parameter_META(parameter = "Moisture (water)", quantity = "g", is_total = total)
        
    def get_cholesterol(self, total = False): # returns calory cholesterol of given instance of a class
        return self.get_parameter_META(parameter = "Cholesterol", quantity = "mg", is_total = total)
    
    def get_carbon(self, total = False): # returns carbon values of given instance of a class
        return self.get_parameter_META(parameter = "carbohydrate", quantity = "g", is_total = total)
    
    def get_fiber(self, total = False): # returns fiber values of given instance of a class
        return self.get_parameter_META(parameter = "Total dietary fibre", quantity = "g", is_total = total)

    def get_sodium(self, total = False): # returns sodium values of given instance of a class
        return self.get_parameter_META(parameter = "Sodium (Na)", quantity = "mg", is_total = total)



class DFmanager:

    """The class has methods to create, populate, modify and resample a time series data frame, containing user's nutreition data."""

    
    @staticmethod
    def createDataFrame():
        """Creates an empty data frame that later will be populated."""

        df = pd.DataFrame(data = {"Calories": None, "Water / g":None, "Fat / g": None, "Protein / g": None, "Cholesterol / mg":None}, index = DFmanager.getTimeIndex(), dtype = "float64")
        df.dropna(inplace = True)
        return df


    @staticmethod
    def getTimeIndex():
        """Using time series, gets the current date and populates the dataframe with those dates as rows."""

        currentTime = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        dateTime = pd.to_datetime([currentTime])
        return dateTime


    @staticmethod
    def addNewEntry(df, nutritions):
        """Appends the dictionary containing the ingredients of the meal with respect to their neutritions' amount.

        Keyword arguments:
        df -- the dataframe created by the first method of the class
        neutritions -- the dictionary containing the ingredients of the meal with respect to their neutritions' amount
        """

        outputDF = df
        outputDF = outputDF.append(pd.DataFrame(nutritions, index = DFmanager.getTimeIndex()))
        return outputDF


    @staticmethod
    def resampleTotalNutrition(df, how = "D"):
        """Resamples the dataframe on a daily basis and computes the sum of the neutritions.

        Keyword arguments:
        df -- the dataframe
        how -- the type of resampling ("D", "W", "M", "Y") (default "D")
        """

        outputDF = df.resample(how).sum()
        return outputDF


    @staticmethod
    def resampleMeanNutrition(df, how = "D"):
        """Resamples the dataframe on a daily basis and computes the mean of the neutritions.

        Keyword arguments:
        df -- the dataframe
        how -- the type of resampling ("D", "W", "M", "Y") (default "D")
        """

        outputDF = df.resample(how).mean()
        return outputDF