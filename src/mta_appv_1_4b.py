"""Just importing"""
from dash import Dash, dcc, html, Input, Output
import dash_bootstrap_components as dbc
import plotly.express as px
import plotly.io as pio
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import pandas as pd

import warnings
warnings.filterwarnings("ignore")

pio.templates.default = "simple_white"

# Importing and preparing the data for general visualizations
df = pd.read_csv(
    "https://raw.githubusercontent.com/plotly/datasets/refs/heads/master/MTA_Ridership_by_DATA_NY_GOV.csv")
# df = pd.read_csv(r'../data/MTA_NYC/MTA_Daily_Ridership.csv') ## Local Working Directory
# working dir Pythonanywhere
# df = pd.read_csv(r'/home/juangerman2024/mysite/MTA_Daily_Ridership.csv')


column_mapper = {
    'Subways: Total Estimated Ridership': 'subway',
    'Subways: % of Comparable Pre-Pandemic Day': 'subway_perc',
    'Buses: Total Estimated Ridership': 'buses',
    'Buses: % of Comparable Pre-Pandemic Day': 'buses_perc',
    'LIRR: Total Estimated Ridership': 'lirr',
    'LIRR: % of Comparable Pre-Pandemic Day': 'lirr_perc',
    'Metro-North: Total Estimated Ridership': 'mn',
    'Metro-North: % of Comparable Pre-Pandemic Day': 'mn_perc',
    'Access-A-Ride: Total Scheduled Trips': 'aar',
    'Access-A-Ride: % of Comparable Pre-Pandemic Day': 'aar_perc',
    'Bridges and Tunnels: Total Traffic': 'br_tun',
    'Bridges and Tunnels: % of Comparable Pre-Pandemic Day': 'br_tun_perc',
    'Staten Island Railway: Total Estimated Ridership': 'sti_rw',
    'Staten Island Railway: % of Comparable Pre-Pandemic Day': 'sti_rw_perc',
}
radio_mapper = [
    {'label': 'Subway', 'value': 'subway'},
    {'label': 'Buses', 'value': 'buses'},
    {'label': 'Bridge & Tunnels', 'value': 'br_tun'}
]  # {'label': 'LIRR, MN, AAR, STIRW', 'value': 'others'}
# df columns renamed according to mapper
dfr = df.rename(columns=column_mapper).copy()

dt_parsed = pd.to_datetime(dfr['Date'])
dfr['dt_parsed'] = dt_parsed

dfr['tot_ridership'] = (dfr['subway']
                        .add(dfr['buses'])
                        .add(dfr['lirr'])
                        .add(dfr['mn'])
                        .add(dfr['aar'])
                        .add(dfr['br_tun'])
                        .add(dfr['sti_rw']))

# The percentage that represent is more representative if we've gathered them.
others_perc = ['lirr_perc', 'mn_perc', 'aar_perc', 'sti_rw_perc']
others = ['lirr', 'mn', 'aar', 'sti_rw']
dfr['others'] = (dfr['lirr']
                 .add(dfr['mn'])
                 .add(dfr['aar'])
                 .add(dfr['sti_rw']))

# just to manage less columns
transp = ['subway', 'buses', 'br_tun', 'others']


dfr_date_idxd = dfr.set_index(dfr['dt_parsed'])
# Subway is more representative in total riderships
dfr_sub = dfr_date_idxd.iloc[:, :3].copy()
dfr_sub_2020 = dfr_sub.loc['2020'].copy()  # Y2020


# # Fig1 Main chart to introduce the story
fig1 = px.line(dfr_sub_2020, x=dfr_sub_2020.index, y='subway_perc',
               labels={'Date': 'Year 2020',
                       'subway_perc': 'Subway percent of riderships',
                       'dt_parsed': ''},
               title='Subways: % of Comparable Pre-Pandemic Day')
fig1.add_vline(x="2020-05-06", line_width=2,
               line_dash="dot", line_color="green")
fig1.add_annotation(x="2020-05-06", y=97,
                    text="Subway system was closed overnight for<br> the first time in the agency’s 116 years on May 06. "
                    "<a href='https://new.mta.info/press-release/mta-restore-24-hour-subway-service-monday-may-17'>[Ref].</a>",
                    xshift=150,
                    showarrow=False,
                    )
fig1.add_trace(go.Scatter(
    x=['2020-06-19'],
    y=[38],
    mode='markers+text',
    marker_color='blue',
    marker_symbol='diamond',
    text='June 19, Phase 2 reopening',
    textposition='top center')
)
fig1.add_trace(go.Scatter(
    x=['2020-11-11'],
    y=[64],
    mode='markers+text',
    marker_color='blue',
    marker_symbol='diamond',
    text="Veterans Day",
    textposition='top center')
)
fig1.update_layout(showlegend=False)


# # Fig2a - Y2020 - Bridge and tunnels +++++++++++++++++++++++++++++
dfr_2020 = dfr_date_idxd.loc['2020'].copy()
fig2a = px.line(dfr_2020, x='dt_parsed', y=['subway_perc', 'buses_perc', 'br_tun_perc'],
                labels={
                    'variable': 'Types of transport',
                    'value': 'Percent of riderships',
                    'dt_parsed': 'Year 2020',
})
fig2a.update_layout(title='Different types of transportation - Year 2020',
                    title_font_size=14, title_y=0.97,
                    legend=dict(
                        orientation="h",
                        yanchor="bottom",
                        y=1.02,
                        xanchor="right",
                        x=1,
                        font_size=10,
                    ))

# Add range slider Fig2.b ++++++++++++++++++++++++++++++++++++++++++++++
fig2b = px.line(dfr_date_idxd, x='dt_parsed', y=['subway_perc', 'buses_perc', 'br_tun_perc'],
                labels={
                    'variable': 'Types of transport',
                    'value': 'Percent of riderships',
                    'dt_parsed': '',
})
fig2b.update_layout(title='Different types of transportation',
                    title_font_size=14,  # title_y=0.97,
                    legend=dict(
                        orientation="v",
                        yanchor="bottom",
                        y=0.95,
                        xanchor="right",
                        x=1,
                        font_size=10,)
                    )
fig2b.update_layout(
    xaxis=dict(
        rangeselector=dict(
            buttons=list([
                dict(count=1,
                     label="1m",
                     step="month",
                     stepmode="backward"),
                dict(count=6,
                     label="6m",
                     step="month",
                     stepmode="backward"),
                dict(count=1,
                     label="YTD",
                     step="year",
                     stepmode="todate"),
                dict(count=1,
                     label="1y",
                     step="year",
                     stepmode="backward"),
                dict(step="all")
            ])
        ),
        rangeslider=dict(
            visible=True,
            bordercolor='#404040',
            borderwidth=1,
        ),
        type="date"
    )
)

# Bar_animated_chart Figure #3 +++++++++++++++++++++++++++++++++++++++++++++++++++++++++
# to slice by dates
dfr_march_april_2020 = dfr_date_idxd.loc['2020-03':'2020-04'].copy()
df_bar_long = (dfr_march_april_2020[['dt_parsed']+transp]
               .reset_index(drop=True)
               # 'Date
               .melt(id_vars='dt_parsed', var_name='Transport', value_name='Riderships')
               )
# modified to proper render in Pythonanywhere
df_bar_long['Date'] = df_bar_long['dt_parsed'].dt.date
fig3 = px.bar(df_bar_long, x='Transport', y='Riderships', color='Transport',
              animation_frame='Date', template='simple_white',
              title='Riderships behavior March to April 2020')
fig3.update_traces(marker=dict(line=dict(color='#000000', width=1)))


# Novel Coronavirus (COVID-19) Cases, provided by JHU CSSE
# This exploratoy data analysis contains info from the data repository by JHU. Novel Coronavirus COVID-19 (2019-nCoV) \
# Data Repository by Johns Hopkins CSSE - (CSSE = Computer Science and Software Engineering)
world_confirmed_url = 'https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_confirmed_global.csv'
world_deaths_url = 'https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_deaths_global.csv'

world_confirmed = pd.read_csv(world_confirmed_url)
world_deaths = pd.read_csv(world_deaths_url)

df_us_conf = world_confirmed[world_confirmed['Country/Region'].str.contains(
    'US')].copy()
df_us_death = world_deaths[world_deaths['Country/Region']
                           .str.contains('US')].copy()


exclude_columns = ['Province/State', 'Country/Region', 'Lat', 'Long']
value_vars = [
    element for element in df_us_conf.columns if element not in exclude_columns]
df_us_conf_melted = pd.melt(
    df_us_conf, var_name='Date', value_vars=value_vars, value_name='conf')
df_us_death_melted = pd.melt(
    df_us_death, var_name='Date', value_vars=value_vars, value_name='deaths')


df_us_conf_melted_date_idxd = df_us_conf_melted.set_index(
    pd.to_datetime(df_us_conf_melted['Date']))
df_us_death_melted_date_idxd = df_us_death_melted.set_index(
    pd.to_datetime(df_us_death_melted['Date']))
diff_deaths = (df_us_death_melted['deaths']
               .diff()
               .fillna(0)
               )
df_us_death_melted['diff_deaths'] = diff_deaths


# Preparing data for charts
df_us_conf_death_merged = (df_us_conf_melted.merge(
    df_us_death_melted, how='left', on='Date')).copy()

date1_parsed = pd.to_datetime(df_us_conf_death_merged['Date'])
df_us_conf_death_merged['Date'] = date1_parsed

dfr2 = (dfr
        .merge(df_us_conf_death_merged, how='left', left_on='dt_parsed', right_on='Date')
        )
mask_conf_nan = dfr2['conf'].isnull()

# Dropping NaT cells above max_date reported by JHU
dfr2.drop(dfr2[mask_conf_nan].index.values, inplace=True)
dfr2_date_idxd = dfr2.set_index(
    pd.to_datetime(dfr2['Date_x']))  # , drop=False)

dfr_fig2 = (dfr2_date_idxd.loc['2020-03':'2020-04'])  # March to April 2020


# Drawing
fig5a = make_subplots(rows=2, cols=1,
                      subplot_titles=(
                          "Subway & Buses Riderships % trend", "Confirmed vs Death cases USA"),
                      shared_xaxes=True,
                      vertical_spacing=0.15)
fig5a.add_trace(go.Scatter(x=dfr_fig2['dt_parsed'], y=dfr_fig2['subway_perc'],
                           mode='lines',
                           name='Subway riderships (%)'),
                row=1, col=1)
fig5a.add_trace(go.Scatter(x=dfr_fig2['dt_parsed'], y=dfr_fig2['buses_perc'],
                           mode='lines',
                           name='Buses riderships (%)'),
                row=1, col=1)
fig5a.add_trace(go.Scatter(x=dfr_fig2['dt_parsed'], y=dfr_fig2['conf'],
                           mode='lines',
                           name='Confirmed cases'),
                row=2, col=1)
fig5a.add_trace(go.Scatter(x=dfr_fig2['dt_parsed'], y=dfr_fig2['deaths'],
                           mode='lines',
                           name='Deaths cases'),
                row=2, col=1)
# type='log', title_text="conf & death cases",
fig5a.update_yaxes(range=[0, 2000], row=2, col=1)
fig5a.update_layout(height=600, width=800, title_text="Correlation with confirmed and death cases of CoVid and"
                    " the utilization of<br>public transportation",
                    title_subtitle_text='Data sampled from March and April 2020',
                    title_font_size=14,
                    legend=dict(yanchor="top", y=0.99, xanchor="left", x=0.79)
                    )
fig5a.update_annotations(
    y=0.97, selector={'text': 'Subway & Buses Riderships % trend'})
fig5a.update_layout(hovermode='x')
# Death diffences respect the previous day
fig5b = px.scatter(df_us_death_melted, x='Date', y='diff_deaths', opacity=0.5,
                   title='Deaths diff to previous day')
fig5b.update_traces(name='Deaths diff',
                    marker_color='#FF7F0E')
fig5b.update_layout(title_subtitle_text='Deaths difference cases respect the previous day,<br>reported by JHU CSSE',
                    yaxis_title_text='Deaths diff')


INTRO = "The COVID-19 pandemic dramatically altered daily life in **New York City**, \
     with one of the most visible impacts being the steep decline in public transportation usage. \
     This dashboard captures the multifaceted story of how the **MTA (Metropolitan Transportation Authority)** endures\
     the crisis and continues to recover in the face of changing public behavior and pandemic realities.\
     The graph below it is just a photo for the **Y2020** and showing only the subway ridership\
     showcasing for the dropping of public transport usage."

paragraph2 = """Data reveals a historic low in subway ridership on **April 12, 2020**;\
     when usage was at its lowest point. Subway and bus ridership dropped to just a fraction of pre-pandemic levels,\
     leading to significant financial losses for the MTA.\
     On this single day, income losses reached a staggering **$8.19 million**, \
     highlighting the agency's reliance on fare revenue and the profound economic shock caused by the pandemic.\
     Move the analysis to compare the Maximum and Minimun number of ridership\
     by type of services provided by MTA.
"""
paragraph3 = """Something noticeable happened with Bridges and Tunnels and it is related to\
        the fact that never went down the traffic-flow. This could be visible in the line graph below the bar chart, \
            where the upper line corresponds to Bridges and Tunnels traffic-percentage during Y2020.
"""
INTRO2nd = """In this second part of the analysis, it is introduced information provided by[Johns Hopkins Coronavirus Resource Center](https://coronavirus.jhu.edu/).\
      This information will lead us toward the relationship between the informed cases of CoVid and the downtrend in the public-transportation utilization.\
      Integrating data from **JHU CSSE**, we observe a strong correlation between rising confirmed COVID-19 cases and the decline in public transport usage.  \
      As cases surged in the spring of 2020, fear of infection and mandated restrictions kept riders off the subways and buses.  
      The recovery trend in ridership, though gradual, mirrors the periods of reduced case numbers and vaccine rollouts.
      This alignment underscores how public health trends directly influence urban mobility patterns, a dynamic likely to persist in future crises.
"""

# Initialize the Dash app with a Bootstrap theme
app = Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

# Card Main with some info +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
card_main = dbc.Card(
    [
        dbc.CardImg(src="/assets/mta_lirr.avif", top=True,
                    title="Image by MTA", alt='MTA NYC Dashboard'),
        dbc.CardBody(
            [
                html.H4("123.5M less riderships\n\
                        equiv. to $339.8M in losses", className="card border-light mb-3"),
                html.P(
                    "This amount is until April 12, global minimun\
                        of riderships in subway observations.",
                    className="card-text",
                ),
            ]
        ),
    ],
    color="light",   # https://bootswatch.com/default/ for more card colors
    inverse=False,   # change color of text (black or white)
    outline=True,  # True = remove the block colors from the background and header
)

# Card Pie with some info +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
card_pie = dbc.Card(
    [
        # dbc.CardHeader("Bridges and Tunnels")
        dbc.CardImg(src="/assets/bridges-and-tunnels_.png", top=True,
                    title='MTA_Bus', alt='MTA NYC Dashboard'),
        dbc.CardBody(
            [
                html.H4("Bridges and Tunnels", className="card-title"),
                dcc.Markdown(paragraph3,
                             id='card_content',  # Place holder for dynamic content
                             className="card-text",
                             ),
                # dbc.Button("Go somewhere", color="primary"),
            ]
        ),
    ],
    className="h-100",  # Full-height card
    color="light",   # https://bootswatch.com/default/ for more card colors
    inverse=False,   # change color of text (black or white)
    outline=True,  # True = remove the block colors from the background and header,
)

# ++++++++++++++++++++++++++++++++++++++++++++++++++
# App layout using Dash Bootstrap Components
app.layout = dbc.Container(
    fluid=True,
    children=[
        # Header with explanation
        dbc.Row(
            [
                dbc.Col(
                    html.H1("MTA NYC Challenge",
                            className="text-start text-primary mb-2"),
                    width=12
                ),
                dbc.Col(
                    dcc.Markdown(INTRO,
                                 className="text-start text-muted"
                                 ),
                    width=12
                )
            ]
        ),

        # Graph and card
        dbc.Row(
            [
                dbc.Col(
                    dcc.Graph(id='subway-line-chart', figure=fig1),
                    width=9  # Main content width
                ),
                dbc.Col(card_main, width=3)
            ]
        ),

        # 2nd layout
        # Pie Charts with interaction
        # Main Row
        dbc.Row(
            [
                # Left Column (Width = 8)
                dbc.Col(
                    [
                        # Title Row
                        dbc.Row(
                            [
                                dbc.Col(
                                    html.H4("MTA, different types of services.",
                                            className="text-start text-primary mb-2"),
                                    width=12
                                ),
                                dbc.Col(
                                    dcc.Markdown(
                                        paragraph2, className="text-start text-muted"),
                                    width=12
                                )
                            ]
                        ),
                        # Graph Row - RadioItems plus Pie_chart
                        dbc.Row(
                            [
                                dbc.Col(dcc.RadioItems(
                                    id='service_type',
                                    options=radio_mapper,
                                    value='subway',
                                    inline=True,
                                ), width=12
                                ),
                                dbc.Col(
                                    dcc.Graph(id='pie_chart', figure={}),
                                    width=12  # Main content width
                                )
                            ]
                        ),
                        # Graph Row - Animated Bar_chart
                        dbc.Row(
                            [
                                dbc.Col(
                                    html.H5("Bar Chart to check the behavior in "\
                                            "riderships from March to April 2020", className="text-start text-primary mb-2"),
                                    width=12
                                ),
                                dbc.Col(
                                    dcc.Graph(
                                        id='bar_animated_chart', figure=fig3),
                                    width=12  # Main content width
                                )
                            ]
                        )
                    ], width=8
                ),
                # Right Column (Width = 4)
                dbc.Col(
                    dbc.Card(card_pie), width=4
                )
            ]
        ),
        # Main Title for tabs
        dbc.Row(
            dbc.Col(
                html.H5("Line chart for Bridges and tunnels.",
                        className="text-start text-primary mb-4"),
                width=12
            )
        ),
        # 2nd row with line chart for bridge and tunnels
        dbc.Row(
            dbc.Col(
                dcc.Tabs(
                    id='tabs',  # Unique ID for the tabs
                    value='tab1',  # Default tab
                    className='custom-tabs',
                    children=[
                        dcc.Tab(label='Y2020 - Bridge & Tunnels', value='tab1',
                                className='custom-tab', selected_className='custom-tab--selected'),
                        dcc.Tab(label='Date Slider - Bridge and Tunnels', value='tab2',
                                className='custom-tab', selected_className='custom-tab--selected')
                    ]
                ), width=10
            )
        ),
        # Tab Content
        dbc.Row(
            dbc.Col(
                # Placeholder for tab-specific content
                html.Div(id='tab_content'),
                width=10
            )
        ),
        # 2nd section with Covid Data ++++++++++++++++++++++++++++++++++++++++++++++++
        dbc.Row(
            [
                dbc.Col(
                    html.H2("CoVid Information added to Dataset",
                            className="text-start text-primary mb-2"),
                    width=12
                ),
                dbc.Col(
                    html.H4("Novel Coronavirus (COVID-19) Cases, provided by JHU CSSE",
                            className="text-start text-primary mb-2"),
                    width=12
                ),
                dbc.Col(
                    dcc.Markdown(INTRO2nd,
                                 className="text-start text-muted"
                                 ),
                    width=12
                )
            ]
        ),
        # Graph and card
        dbc.Row(
            [
                dbc.Col(
                    dcc.Graph(id='subway_vs_covid', figure=fig5a),
                    width=8  # Subplots
                ),
                dbc.Col(
                    dcc.Graph(id='deaths_diff', figure=fig5b),
                    width=4  # Death differences
                )
            ]
        ),
        # Summary card below with final insigths +++++++++++++++++++++++++++++++++++++++++++++++++
        dbc.Row(
            dbc.Col(
                dbc.Card(
                    [
                        dbc.CardHeader([
                            html.H4("Future Considerations and Recommendations",
                                    className="text-start text-primary mb-2"),
                            html.P('The insights from this analysis provide a roadmap for building a resilient and adaptive\
                                    public transportation system. Taking into account data trends and strategies employed\
                                    by the MTA during the pandemic, the following refined recommendations are proposed:',
                                   className="text-start text-muted"
                                   )]
                        ),
                        dbc.CardBody(
                            [
                                html.H6('1. Strengthen Public Health Integration',
                                        className="text-start text-primary mb-2"),
                                dcc.Markdown("- **Health Protocols**: Build on the MTA's success with enhanced cleaning,\
                                              mask mandates, and air filtration improvements. These measures should become\
                                              part of a permanent contingency plan.",
                                             className="text-start text-muted"),
                                dcc.Markdown("- **Real-Time Health Monitoring**: Collaborate with public health agencies to\
                                              monitor case surges and adjust operations as needed.",
                                             className="text-start text-muted"),
                                html.H6('2. Innovate for Financial Resilience',
                                        className="text-start text-primary mb-2"),
                                html.P("The MTA's heavy reliance on fare revenue exposed vulnerabilities during the pandemic.\
                                        Future strategies should diversify income streams:",
                                       className="text-start text-muted"),
                                dcc.Markdown("- **Federal and State Support**: Advocate for sustainable government funding models\
                                              to stabilize finances during crises.",
                                             className="text-start text-muted"),
                                dcc.Markdown("- **Congestion Pricing**: Implement and expand congestion pricing to generate revenue\
                                              and manage demand for transit alternatives.",
                                             className="text-start text-muted"),
                                dcc.Markdown("- **Technology Integration**: Explore dynamic fare pricing based on demand patterns,\
                                              incentivizing off-peak travel and reducing crowding.",
                                             className="text-start text-muted"),
                                html.H6('3. Enhance Rider Confidence and Communication',
                                        className="text-start text-primary mb-2"),
                                html.P("The slow recovery in ridership reflects lingering hesitance among riders.\
                                        Steps to rebuild trust include:",
                                       className="text-start text-muted"),
                                dcc.Markdown("- **Transparency**: Provide regular updates on safety measures,\
                                              ridership data, and system performance.",
                                             className="text-start text-muted"),
                                dcc.Markdown("- **Flexible Pass Options**: Offer new fare products tailored to hybrid work patterns,\
                                              such as part-time commuter passes.",
                                             className="text-start text-muted"),
                                dcc.Markdown("- **Community Engagement**: Use surveys and outreach programs to better understand rider concerns and needs.",
                                             className="text-start text-muted"),
                                html.H6('4. Plan for Long-Term Ridership Shifts',
                                        className="text-start text-primary mb-2"),
                                html.P("The pandemic accelerated changes in work and travel habits,\
                                        which are unlikely to fully reverse. The MTA should:",
                                       className="text-start text-muted"),
                                dcc.Markdown("- **Data-Driven Decisions**: Leverage ridership data to adapt service levels and routes to evolving demand.",
                                             className="text-start text-muted"),
                                dcc.Markdown("- **Last-Mile Solutions**: Partner with micromobility providers (e.g., bike and scooter sharing)\
                                              to improve last-mile connectivity.",
                                             className="text-start text-muted"),
                                dcc.Markdown("- **Sustainability Goals**: Prioritize investments in green technologies, such as electrified buses,\
                                              to attract environmentally conscious riders.",
                                             className="text-start text-muted"),
                                html.H6('5. Build Crisis-Resilient Infrastructure',
                                        className="text-start text-primary mb-2"),
                                html.P("To prepare for future crises, the MTA must focus on:",
                                       className="text-start text-muted"),
                                dcc.Markdown("- **Emergency Preparedness**: Develop detailed scenarios and action plans for various crisis types,\
                                              including pandemics and climate events.",
                                             className="text-start text-muted"),
                                dcc.Markdown("- **Digital Transformation**: Enhance remote work and learning resources for staff to ensure uninterrupted\
                                              operations during disruptions.",
                                             className="text-start text-muted"),
                                dcc.Markdown("- **Redundancy**: Invest in system redundancies to minimize disruptions, including backup power systems\
                                              and alternative communication networks.",
                                             className="text-start text-muted"),
                                html.H6('6. Collaborate Across Agencies',
                                        className="text-start text-primary mb-2"),
                                html.P("COVID-19 underscored the importance of collaboration between transit agencies,\
                                        public health authorities, and governments. The MTA should:",
                                       className="text-start text-muted"),
                                dcc.Markdown("- **Coordinate Regionally**: Share resources and information with neighboring\
                                              transit systems to create a unified response.",
                                             className="text-start text-muted"),
                                dcc.Markdown("- **National Advocacy**: Collaborate with other agencies to advocate for federal\
                                              support programs addressing transit funding gaps during crises.",
                                             className="text-start text-muted"),
                                html.P("These refined recommendations align with the MTA's existing priorities while addressing\
                                        critical lessons from the pandemic. By implementing these strategies, the MTA can transform\
                                        challenges into opportunities, ensuring a safer, more resilient, and rider-focused public transit system.",
                                       className="text-start text-muted"),
                                html.H6('References',
                                        className="text-start text-primary mb-2"),
                                html.P("For deeper insights, you can explore:",
                                       className="text-start text-muted"),
                                dcc.Markdown("- [MTA Inspector General Reports](https://mtaig.ny.gov/)\
                                              detailing operational adjustments and challenges during the pandemic.",
                                             className="text-start text-muted"),
                                dcc.Markdown("- [Office of the State Comptroller's Subway Recovery Analysis](https://www.osc.ny.gov/)\
                                              for data-driven perspectives on ridership trends and recovery patterns.",
                                             className="text-start text-muted"),
                                dcc.Markdown("- Financial Impacts and Ridership Trends. [Archived Subway Tracker | Office of the NY State Comptroller_Archived]\
                                             (https://www.osc.ny.gov/reports/osdc/subway-recovery-tracker-archived).",
                                             className="text-start text-muted"),
                                dcc.Markdown("- [Impact of the COVID-19 Pandemic on Subway Ridership in New York City]\
                                             (https://www.osc.ny.gov/osdc/subway-recovery-tracker)",
                                             className="text-start text-muted"),
                            ]
                        )
                    ], outline=True
                ),
                width=12  # Full width
            )
        )
    ]
)


# Callback for interactivity for Pie Charts
@app.callback(
    Output('pie_chart', 'figure'),
    Input('service_type', 'value')
)
def update_chart(service_type):
    # print(service_type)
    dff_max_idx = dfr[service_type].idxmax()
    dff_min_idx = dfr[service_type].idxmin()
    pie_min = (dfr
               .loc[dff_min_idx, transp]
               .reset_index()
               .rename(columns={'index': 'Type', dff_min_idx: 'Riderships'}))
    pie_max = (dfr
               .loc[dff_max_idx, transp]
               .reset_index()
               .rename(columns={'index': 'Type', dff_max_idx: 'Riderships'}))

    # Create subplots: use 'domain' type for Pie subplot
    name_max = dfr.loc[dff_max_idx, 'dt_parsed'].strftime('%b %d, %Y')
    name_min = dfr.loc[dff_min_idx, 'dt_parsed'].strftime('%b %d, %Y')
    name_max_ = dfr.loc[dff_max_idx, 'dt_parsed'].strftime('%b %d')
    name_min_ = dfr.loc[dff_min_idx, 'dt_parsed'].strftime('%b %d')

    perc_max = dfr.loc[dff_max_idx, service_type+'_perc']
    perc_min = dfr.loc[dff_min_idx, service_type+'_perc']

    fig20 = make_subplots(rows=1, cols=2, specs=[
                          [{'type': 'domain'}, {'type': 'domain'}]])
    fig20.add_trace(go.Pie(labels=pie_max['Type'], values=pie_max['Riderships'], name=name_max),
                    1, 1)
    fig20.add_trace(go.Pie(labels=pie_min['Type'], values=pie_min['Riderships'], name=name_min),
                    1, 2)

    # # Use `hole` to create a donut-like pie chart
    fig20.update_traces(hole=.4, hoverinfo="label+percent+name")
    fig20.update_traces(textinfo='value', textfont_size=12, insidetextorientation='horizontal',
                        marker=dict(line=dict(color='#000000', width=1)))
    fig20.update_layout(
        title_text=f"{name_max} vs. {name_min}",
        title_subtitle_text=f"Daily Riderships. {name_max}({
            perc_max} % of total pre-pandemic subway riderships) vs. < br > {name_min} ({perc_min} %, global minimum)",
        title_subtitle_font_size=12,
        title_font_size=20,
        template='simple_white',
        # Add annotations in the center of the donut pies.
        annotations=[dict(text=name_max_, x=sum(fig20.get_subplot(1, 1).x) / 2, y=0.5,
                          font_size=14, showarrow=False, xanchor="center"),
                     dict(text=name_min_, x=sum(fig20.get_subplot(1, 2).x) / 2, y=0.5,
                          font_size=14, showarrow=False, xanchor="center")])
    return fig20

# Callback for interactivity for Tabs


@app.callback(
    Output('tab_content', 'children'),
    Input('tabs', 'value')
)
def render_tab_content(tab):
    if tab == 'tab1':  # 'Y2020 - Bridge & Tunnels', value='tab1'
        return dcc.Graph(
            id='graph-a',
            figure=fig2a
        )
    elif tab == 'tab2':  # 'Date Slider - Bridge and Tunnels'
        return dcc.Graph(
            id='graph-b',
            figure=fig2b
        )


# Run the app
if __name__ == '__main__':
    app.run(debug=False)
