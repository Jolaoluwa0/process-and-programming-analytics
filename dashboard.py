# install requirements
from dash import Dash, html, dcc, Input, Output
import pandas as pd
import plotly.express as px
import plotly.figure_factory as ff
import seaborn as sns
import numpy as np

# Load the dataset
df = pd.read_csv('telco-customer-churn/WA_Fn-UseC_-Telco-Customer-Churn.csv')

# preprocessing
df.replace(' ', np.nan, inplace = True)
df.drop('customerID', axis=1, inplace=True)
df.dropna(axis=0, inplace = True)

# extracting continuous variable
continuous_variables = []
categorical_variables = []
for x in df.columns:
    if df[x].nunique()>50:
        continuous_variables.append(x)
    else:
        categorical_variables.append(x)
        
# converting continuous variable to caregorical variable
# for variable in continuous_variables:
#     df[variable]=df[variable].astype('float')
#     df[variable]=np.where(df[variable]>df[variable].median(),f'High {variable}',f'Low {variable}')
        
# Create the Dash app
app = Dash()

# Set up the app layout
column_dropdown = dcc.Dropdown(options=list(df.columns),
                            value='Churn')
graph_type_dropdown = dcc.Dropdown(options=['histogram','box plots', 'scatter plots','group bar'],
                            value='histogram')

app.layout = html.Div(children=[
    html.H1(children='Customer Churn Dashboard'),
    graph_type_dropdown,
    column_dropdown,
    dcc.Graph(id='churn-graph')
])


# Set up the callback function
@app.callback(
    Output(component_id='churn-graph', component_property='figure'),
    Output(component_id=column_dropdown, component_property='options'),
    Input(component_id=column_dropdown, component_property='value'),
    Input(component_id=graph_type_dropdown, component_property='value')
)
def update_graph(selected_column,selected_graph):
    if selected_graph == 'histogram':
        line_fig = px.histogram(df, x=selected_column, color='Churn')
        return line_fig,categorical_variables
    elif selected_graph == 'box plots':
        line_fig = px.box(df, x=selected_column, color='Churn')
        return line_fig,continuous_variables
    elif selected_graph == 'scatter plots':
        line_fig = px.scatter(df, x=selected_column, color='Churn')
        return line_fig,continuous_variables
    elif selected_graph == 'group bar':
        line_fig = px.histogram(df, x=selected_column, color='Churn', barmode='group')
        return line_fig,categorical_variables


# Run local server
if __name__ == '__main__':
    app.run_server(debug=True)