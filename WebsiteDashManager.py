#!/usr/bin/env python
# coding: utf-8

# In[ ]:


from FoodDetector import FoodDetector
from Nutritions import NutritionCounter
from Nutritions import DFmanager as mngr
import dash
import dash_table as dt
from dash.dependencies import Input, Output, State
import dash_core_components as dcc
import dash_html_components as html
import os
from PIL import Image
import pandas as pd
import base64
from datetime import datetime

path=os.getcwd()
external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

# uncomment the next line if you want a real-life Yummy Detector (not to showcase)
# create df
# resampledTotal = mngr.resampleTotalNutrition(df, how = "W")
# dates = [str(i).split(sep = " ")[0] for i in resampledTotal.index]

df = pd.read_csv("TestDataFrame.csv", parse_dates = True, index_col=0) # A sample dataframe

colors = { # Dictionary of constant colors
    'background': '#111111',
    'text': '#7FDBFF'
}

def reloadPlotlyGraph(resampleType = "W", dataF = df):
    
    '''
    Returns a plotly multihistogram with the specified dataframe and resample type for the dataframe
    
    Keyword arguments:
    resampleType -- Determines the resample type. May be "D", "W", "M", "Y" (default: "W")
    dataF -- Input dataframe (default: df)
    
    '''
    
    resampleTypeNew = resampleType
    xaxis = []
    
    if resampleType == "Today":
        resampleTypeNew = "D"
        
        
    resampledTotal = mngr.resampleTotalNutrition(dataF, how = resampleTypeNew)
    
    currentTime = datetime.now().strftime('%Y-%m-%d')
    
    if resampleType == "Today":
        resampledTotal = resampledTotal[currentTime:currentTime]
        
    xaxis = resampledTotal.index
    figure={
            'data': [
                {'x': xaxis, 'y': resampledTotal["Protein / g"], 'type': 'bar', 'name': 'Protein / g'},
                {'x': xaxis, 'y': resampledTotal["Carbohydrate / g"], 'type': 'bar', 'name': 'Carbohydtrate / g'},
                {'x': xaxis, 'y': resampledTotal["Fat / g"], 'type': 'bar', 'name': 'Fat / g'}

            ],
            'layout': {
                'plot_bgcolor': colors['background'],
                'paper_bgcolor': colors['background'],
                'font': {
                    'color': colors['text']
                }
            }
        }
    
    return figure

logoImage = 'logo.png' # replace with your own image
encoded_image = base64.b64encode(open(logoImage, 'rb').read())

app.layout = html.Div([
    
    html.Div([
        
    
    
    html.Img(
        src= 'data:image/png;base64,{}'.format(encoded_image.decode()),
            width="10%",
            style = {
                'display': 'inline-block'
            }),
    
    html.H1( # Title 
        id="The name",
        children="Yummy Detector",
        style={
            'text-align': 'center'
        }),
    
    dcc.Upload( # Upload button
        id='upload-image',
        children=html.Div(
            ['Drag and Drop / Click'],
            style = {
                "margin-left": "auto",
                "margin-right": "auto",
                'text-align': 'center',
                'display': 'inline-block'
            }
        ),
        style={
            'width': '20%',
            'height': '40px',
            'lineHeight': '60p',
            'borderStyle': 'hidden',
            'borderRadius': '15px',
            'text-align': 'center',
            "boxShadow": "0px 15px 30px -10px grey",
            "margin-left": "auto",
            "margin-right": "auto",
            "transform": "scale(1.5)",

            "background": "rgb(70,252,177)",
            "background": "-moz-radial-gradient(circle, rgba(70,252,177,1) 4%, rgba(63,251,110,1) 95%)",
            "background": "-webkit-radial-gradient(circle, rgba(70,252,177,1) 4%, rgba(63,251,110,1) 95%)",
            "background": "radial-gradient(circle, rgba(70,252,177,1) 4%, rgba(63,251,110,1) 95%)",
            "filter": "progid:DXImageTransform.Microsoft.gradient(startColorstr='#46fcb1',endColorstr='#3ffb6e',GradientType=1)"
        },
        multiple=False
    )
    ]),
    
    html.Div( # Displayed image and the ingredients in it
            id='output-image-upload',
            style = {"padding":"30px",
                     "width":"49%",
                     "textAlign":"center",
                     'borderRadius': '10px',
                     "margin-left": "auto",
                     "margin-right": "auto"}),
    
    html.H1( # CHANGE TO H1
            id="result", 
            children="",
            style = {"padding":"20px",
                     'display': 'inline-block',
                     "height":"auto",
                     "vertical-align": "top",
                     "word-wrap": "break-word",
                     "fontSize":"40px"}),
    
    html.Div(
        dt.DataTable(id='data-table',
            style_as_list_view=True,
            style_cell = {'padding': '5px',
                          'backgroundColor': 'rgb(50, 50, 50)',
                          'color': 'white'
                },
            style_header = {
                'backgroundColor': 'rgb(30, 30, 30)',
                'fontWeight': 'bold'
                }
            ), # One-line dataframe outputting the nutritions from the uploaded image
        style = {
            "padding":"20px",
            "fontSize":"25px"
        }
    ),
    
    dcc.Dropdown( # Dropdown to choose resampling type
        id='resample_dropdown',
        options = [
            {'label': 'Today', 'value': 'Today'},
            {'label': 'Dalily', 'value': 'D'},
            {'label': 'Weekly', 'value': 'W'},
            {'label': 'Monthly', 'value': 'M'},
            {'label': 'Annually', 'value': 'Y'}
            ],
        value = "W",
        
        style = {"textAlign":"center",
                 "width":"45%",
                 "height":"45%",
                 "margin-left": "auto",
                 "margin-right": "auto",
                 'borderRadius': '10px'}
        
        
        ), 
        
    
    dcc.Graph( # Multihistogram
        id='dataframe', 
        style={
            "padding": "10px"
        }
    ),

])
    


def parse_contents(contents):
    """Returns an html div to output uploaded image."""
    
    return html.Div([

        # HTML images accept base64 encoded strings in the same format
        # that is supplied by the upload
        html.Img(src=contents,width="60%",height="60%")
    ])

def save_file(content):
    """Decode and store a file uploaded with Plotly Dash."""
    
    data = content.encode("utf8").split(b";base64,")[1]
    with open('some_image.png', "wb") as fp:
        fp.write(base64.decodebytes(data))


@app.callback(Output('output-image-upload', 'children'),[Input('upload-image', 'contents')])
def update_output(content): # Displayes the image
    """Displays an inputted image on the page."""
    
    if content is not None:
        children = parse_contents(content)
        return children
    

@app.callback([Output("result", 'children'), # Executed when image is uploaded or resample method is changed
               Output('data-table', 'columns'),
               Output('data-table', 'data'),
               Output("dataframe", 'figure')],
              
              [Input("upload-image","contents"),
               Input("resample_dropdown","value")])

def info(images, resampleType):
    """Updates the following data on the page: 
        * Outputs the list of ingredients
        * Populates and displays the dataframe containing nutritions from uploaded image
        * Changes the dropdown value to 'Today'
        * Updates the plotly multihistagram
    """
    # No need to look at this chunk
    total_nutr = {}
    ings = []
    columns = []
    data = []
    resultString = ""
    
    if images is not None:
        save_file(images)
        filename=path+"/some_image.png"
        food = FoodDetector(filename)
        ings = food.ingredients()
        nut  = NutritionCounter(ings)
        total_nutr = nut.get_total_nutritions()
        total_nutr = {v:round(k, ndigits=2) for v,k in total_nutr.items() }
        columns = [{"name": i, "id": i} for i in df.columns]
        data = [total_nutr]
        resultString = "Found ingredients: " + ", ".join(ings[0:6])

    # The problems must be here below
    df_ = df.append(pd.DataFrame(total_nutr, index = mngr.getTimeIndex())) # Adds new netry to the timeseries dataframe
    figureToOut = reloadPlotlyGraph(resampleType, dataF = df_) # Creates figure with the above created df_ to be further returned in the line below

    return resultString, columns, data, figureToOut


if __name__ == '__main__':
    app.run_server(debug=False)

