import pandas as pd
import dash
from dash import dcc, html
from dash.dependencies import Input, Output
import plotly.express as px
import dash_bootstrap_components as dbc
import base64

# Load and preprocess data
df1 = pd.read_csv('https://raw.githubusercontent.com/nethajinirmal13/Training-datasets/main/zomato/zomato.csv')
df2 = pd.read_excel('C:\\Users\\krkar\\Downloads\\Country-Code.xlsx', engine='openpyxl')
df = pd.merge(df1, df2, on='Country Code')

df['Average Cost for two'].mean()
a1 = df['Average Cost for two'] / 2
df['Amount'] = a1 * df['Price range']

# Currency conversion
replace_dict = {'Botswana Pula(P)': 'BWP', 'Brazilian Real(R$)': 'BRL', 'Dollar($)': 'USD',
                'Emirati Diram(AED)': 'AED', 'Indian Rupees(Rs.)': 'INR', 'Indonesian Rupiah(IDR)': 'IDR',
                'NewZealand($)': 'NZD', 'Pounds(專)': 'GBP', 'Qatari Rial(QR)': 'QAR', 'Rand(R)': 'ZAR',
                'Sri Lankan Rupee(LKR)': 'LKR', 'Turkish Lira(TL)': 'TRY'}
df = df.replace({'Currency': replace_dict})

df['Rupees'] = 0
df2['Currency'] = ['INR', 'AUD', 'BRL', 'CAD', 'IDR', 'NZD', 'PHP', 'QAR', 'SGD', 'ZAR', 'LKR', 'TRY', 'AED', 'GBP', 'USD']
df2['Currency_rates'] = [1, 56.99, 15.88, 56.97, 0.054, 52.22, 6.47, 22.24, 61.75, 0.21, 0.22, 0.22, 22.25, 100.19, 81.66]
df = pd.merge(df, df2, on='Country Code')
df.drop(df.columns[[11, 21]], axis=1, inplace=True)
df['Rupees'] = df['Amount'] * df['Currency_rates']
df[['Country Code', 'Currency_y', 'Rupees']]
df = df.drop_duplicates()

# Initialize Dash app with suppress_callback_exceptions=True
app = dash.Dash(__name__, suppress_callback_exceptions=True, external_stylesheets=[dbc.themes.BOOTSTRAP])
server = app.server

# Define main content layout with background image
app.layout = html.Div([
    html.Div(style={'display': 'flex'}, children=[
        html.Div(style={'position': 'fixed', 'top': '0', 'left': '0', 'height': '100%', 'width': '250px', 'backgroundColor': '#f0f0f0', 'padding': '20px', 'boxShadow': '0 4px 6px rgba(0, 0, 0, 0.1)', 'zIndex': '1'}, children=[
            html.Div([
                html.H2("Welcome to Zoooomato", style={'color': 'blue','font-size': '25px'}),
                dcc.Tabs(
                    id='sidebar-tabs',
                    value='home',  # Default value
                    vertical=True,  # Display tabs vertically
                    children=[
                        dcc.Tab(label='Home', value='home', className="sidebar-item"),
                        dcc.Tab(label='Charts', value='charts', className="sidebar-item"),
                        dcc.Tab(label='Comparison', value='Comparison', className="sidebar-item"),
                        dcc.Tab(label='About', value='about', className="sidebar-item"),
                    ]
                )
            ])
        ]),
        html.Div(style={'marginLeft': '250px', 'paddingLeft': '50px', 'paddingTop': '20px'}, children=[
            html.Div([
                html.H1("Zomato Data Analysis and Visualization", className="header-title", style={'color': 'blue', 'textAlign': 'center'}),
                html.Div([
                    dcc.Location(id='url', refresh=False),
                    html.Div(id='page-content', className="page-content")
                ]),
            ], className="main-container")
        ])
    ])
])
# Encode images to base64
with open("C:/Users/krkar/Downloads/burger.jpg", "rb") as image_file:
    encoded_home_bg = base64.b64encode(image_file.read()).decode('utf-8')
with open("C:/Users/krkar/Downloads/about food.jpg", "rb") as image_file:
    encoded_about_bg = base64.b64encode(image_file.read()).decode('utf-8')

# Home page layout
home_layout = html.Div(style={'backgroundImage': f'url("data:image/jpeg;base64,{encoded_home_bg}")', 'backgroundSize': 'cover', 'height': '100vh', 'padding': '20px'}, children=[
    html.P(" "),
    html.P("Zomato is a popular restaurant discovery and food delivery platform.", className="section-content", style={'font-size': '25px', 'color': 'black', 'textAlign': 'justify','fontWeight': 'bold'}),  
    html.P("This project aims to analyze Zomato restaurant data to provide insights and trends.", className="section-content", style={'font-size': '25px', 'color': 'black', 'textAlign': 'justify','fontWeight': 'bold'}), 
    html.P("It covers areas such as restaurant ratings, cuisines, locations, and more.", className="section-content", style={'font-size': '25px', 'color': 'black', 'textAlign': 'justify','fontWeight': 'bold'}), 
    html.P("Food sector is one of the major growing business and essential industries and zomato application is most widely used.", className="section-content", style={'font-size': '25px', 'color': 'black', 'textAlign': 'justify','fontWeight': 'bold'}),  
    html.H3("Skills Take Away : Python Scripting, Pandas and Plotly", className="highlighted-text", style={'color': 'white', 'textAlign': 'justify'}),
    html.H3("Domain : Data analysis and visualization", className="highlighted-text", style={'color': 'white', 'textAlign': 'justify'})
], className="home-content")


# About page layout
about_layout = html.Div(style={'backgroundImage': f'url("data:image/jpeg;base64,{encoded_about_bg}")', 'backgroundSize': 'cover', 'height': '100vh', 'padding': '20px'}, children=[
    html.H2(" "),
    html.H2("About Zomato", className="section-title", style={'color': 'blue'}),
    html.H2(" "),
    html.P("Zomato is an Indian multinational restaurant aggregator and food delivery company.", className="section-content", style={'font-size': '25px', 'color': 'red','fontWeight': 'bold'}), 
    html.H2(" "),
    html.P("Founded in 2008 by Deepinder Goyal and Pankaj Chaddah, Zomato provides information, menus, and user reviews of restaurants, and also offers food delivery from partner restaurants in select cities.", className="section-content", style={'font-size': '25px', 'color': 'red','fontWeight': 'bold'}),  
    html.P("As of 2022, Zomato operates in over 10,000 cities across 24 countries.", className="section-content", style={'font-size': '25px', 'color': 'red','fontWeight': 'bold'}),  
    html.P("The company's mission is to ensure that nobody has a bad meal.", className="section-content", style={'font-size': '25px', 'color': 'red','fontWeight': 'bold'}), 
    html.P("The major reason for selecting this particular data collection is to analyze and create visual representation of the best restaurants in prominent places throughtout the world based on many criteria, including customer reviews, food quality,hospitality and more.", className="section-content", style={'font-size': '25px', 'color': 'red','fontWeight': 'bold'}), 
    html.P("We can also visualize the most affordable and priciest restaurants in around the world using this dataset.", className="section-content", style={'font-size': '25px', 'color': 'red','fontWeight': 'bold'}) 
], className="about-content")

# Charts page layout
charts_layout = dbc.Container([
    html.H2("Charts Page"),
    dcc.Dropdown(
        id="dropdown-country",
        options=[{"label": country, "value": country} for country in df['Country_y'].unique()],
        value=df['Country_y'].unique()[0],
        clearable=False,
    ),
    html.Div(id='output-container-country'),
    dbc.Row([
        dbc.Col(dcc.Graph(id='chart1'), width=12),  
        dbc.Col(dcc.Graph(id='chart2'), width=12),  
    ]),  
    dbc.Row([
        dbc.Col(dcc.Graph(id='chart3'), width=12),  
    ]),  
    dbc.Row([
        dbc.Col(dcc.Graph(id='chart4'), width=12),  
    ]),
], fluid=True)

# Chart 8: Living Cost Comparison Across Cities in India
all_cities_restaurant_counts = df[df['Country_y'] == 'India'].groupby('City')['Restaurant Name'].nunique().reset_index()
fig_chart8 = px.bar(all_cities_restaurant_counts, x='City', y='Restaurant Name', title='Restaurant Count Comparison Across Cities in India')
fig_chart8.update_layout(xaxis_title="City", yaxis_title="Number of Restaurants")

chart8_layout = dcc.Graph(id='chart8', figure=fig_chart8)
# Add a new layout for city comparison
city_comparison_layout = html.Div([
    html.H2("City Comparison"),
    dcc.Dropdown(
        id="dropdown-city",
        options=[{"label": city, "value": city} for city in df[df['Country_y'] == 'India']['City'].unique()],
        value=df[df['Country_y'] == 'India']['City'].unique()[0],
        clearable=False,
    ),
    html.Div(id='output-container-city'),
    dbc.Row([
        dbc.Col(dcc.Graph(id='chart7'), width=12),  # Chart 7: Online Delivery vs Dine-in
        dbc.Col(chart8_layout, width=12),  # Chart 8: Living Cost Comparison
    ]),
])

# Callback to render content based on selected sidebar option
@app.callback(
    Output('page-content', 'children'),
    [Input('sidebar-tabs', 'value')]
)
def render_content(selected_tab):
    if selected_tab == 'home':
        return home_layout
    elif selected_tab == 'about':
        return about_layout
    elif selected_tab == 'charts':
        return charts_layout
    elif selected_tab == 'Comparison':  # Add city comparison layout
        return city_comparison_layout
    else:
        # Default to home layout if an unknown tab is selected
        return home_layout

# Callback to update country-specific data
@app.callback(
    Output('output-container-country', 'children'),
    [Input('dropdown-country', 'value')]
)
def update_country_data(country):
    return f"You have selected {country}"

@app.callback(
    Output('chart1', 'figure'),
    [Input('dropdown-country', 'value')]
)
def update_chart1(country):
    mask = (df['Country_y'] == country)  # Filter by country only
    top_expensive_cuisines = df[mask].nlargest(10, 'Rupees')
    # Get currency and currency rate for the selected country
    currency = df[df['Country_y'] == country]['Currency_y'].iloc[0]
    currency_rate = df[df['Country_y'] == country]['Currency_rates'].iloc[0]
    # Apply currency conversion if the currency is not INR
    if currency != 'INR':
        top_expensive_cuisines['Rupees'] = top_expensive_cuisines['Rupees'] * currency_rate
    fig = px.bar(top_expensive_cuisines, x='Cuisines', y='Rupees', title=f'Top 10 Expensive Cuisines in {country}')
    fig.update_layout(xaxis_title="Cuisine", yaxis_title=f"Average Cost ({currency})")
    return fig


@app.callback(
    Output('chart2', 'figure'),
    [Input('dropdown-country', 'value')]
)
def update_chart2(country):
    mask = (df['Country_y'] == country)  # Filter by country only
    delivery_modes = df[mask]['Has Online delivery'].value_counts().reset_index()
    delivery_modes.columns = ['Delivery Mode', 'Count']
    fig = px.pie(delivery_modes, values='Count', names='Delivery Mode', title=f'Online Delivery vs Dine-in in {country}')
    return fig


@app.callback(
    Output('chart3', 'figure'),
    [Input('dropdown-country', 'value')]
)
def update_chart3(country):
    mask = (df['Country_y'] == country)
    city_famous_cuisine = df[mask]['Cuisines'].value_counts().nlargest(10)
    fig = px.bar(x=city_famous_cuisine.index, y=city_famous_cuisine.values, title=f'Famous Cuisines in {country}')
    fig.update_layout(xaxis_title="Cuisine", yaxis_title="Number of Restaurants")
    return fig

@app.callback(
    Output('chart4', 'figure'),
    [Input('dropdown-country', 'value')]
)
def update_chart4(country):
    mask = (df['Country_y'] == country)
    city_rating_count = df[mask]['Aggregate rating'].value_counts().reset_index()
    fig = px.bar(city_rating_count, x=city_rating_count.index, y='Aggregate rating', title=f'Rating Count in {country}')
    fig.update_layout(xaxis_title="Rating", yaxis_title="Number of Restaurants")
    return fig

# Callback to update city-specific data
@app.callback(
    Output('output-container-city', 'children'),
    [Input('dropdown-city', 'value')]
)
def update_city_data(city):
    return f"You have selected {city}"
# Chart 7: Online Delivery vs Dine-in Spending Comparison
@app.callback(
    Output('chart7', 'figure'),
    [Input('dropdown-city', 'value')]
)
def update_chart7(city):
    mask = (df['City'] == city) & (df['Country_y'] == 'India')  # Filter by city and country
    delivery_modes = df[mask]['Has Online delivery'].value_counts().reset_index()
    delivery_modes.columns = ['Delivery Mode', 'Count']
    fig = px.pie(delivery_modes, values='Count', names='Delivery Mode', title=f'Online Delivery vs Dine-in in {city}')
    return fig


if __name__ == '__main__':
    app.run_server(debug=True)
