import pandas as pd
from pytrends.request import TrendReq
import plotly.graph_objects as go
import pycountry
import numpy as np
import json
import requests
from datetime import datetime
import dateutil.relativedelta
import warnings
warnings.filterwarnings('ignore')

class Graphed_Trend:

    def __init__(self, keyword_list, timeframe, geo_location):
        self.keyword_list = keyword_list
        self.timeframe = timeframe
        self.geo_location = geo_location

    def get_data(self):
        ## Call pytrends
        pytrend = TrendReq(hl = 'en-GB')
        keywords = self.keyword_list
        pytrend.build_payload(
            kw_list = keywords,
            cat = 0,
            timeframe = self.timeframe,
            geo = self.geo_location,
            gprop = '')

        ## DF transformations
        data = pytrend.interest_over_time()
        data.reset_index(inplace = True)
        data.drop('isPartial', axis = 1, inplace = True)

        return data

    def visualise_trends(self, data):
        ## Create traces
        fig = go.Figure()
        try:
            fig.add_trace(go.Scatter(x=data['date'], y=data[data.columns[1]],
                                    mode='lines',
                                    name=data.columns[1]))
        except:
            pass
        try:
            fig.add_trace(go.Scatter(x=data['date'], y=data[data.columns[2]],
                                mode='lines',
                                name=data.columns[2]))
        except:
            pass
        try:
            fig.add_trace(go.Scatter(x=data['date'], y=data[data.columns[3]],
                                mode='lines',
                                name=data.columns[3]))
        except:
            pass
        try:
            fig.add_trace(go.Scatter(x=data['date'], y=data[data.columns[4]],
                                mode='lines',
                                name=data.columns[4]))
        except:
            pass
        try:
            fig.add_trace(go.Scatter(x=data['date'], y=data[data.columns[5]],
                                mode='lines',
                                name=data.columns[5]))
        except:
            pass        

        fig.update_xaxes(
            rangeslider_visible=True,
            range = (data['date'].min(), data['date'].max()),
            rangeselector=dict(
                buttons=list([
                    dict(count=7, label="7d", step="day", stepmode="backward"),
                    dict(count=1, label="1m", step="month", stepmode="backward"),
                    dict(count=3, label="3m", step="month", stepmode="backward"),
                    dict(count=6, label="6m", step="month", stepmode="backward"),
                    dict(count=1, label="YTD", step="year", stepmode="todate"),
                    dict(count=1, label="1y", step="year", stepmode="backward"),
                    dict(step="all")
                ])
            )
        )

        fig.update_layout(
            title = 'Search Interest Aginst Time',
            autosize = False,
            width = 950,
            height = 700,
            margin = dict(
                l = 50,
                r = 50,
                b = 50,
                t = 100,
                pad = 2
            ),
            template = "plotly_white",
            hovermode='x'
        )

        fig.show()

    def trend_average(self, data):
        ## Create dict
        avg = dict()

        for col in data.columns[1:]:
            avg[col] = data[col].mean()

        ## DF transformations
        avg_df = pd.DataFrame.from_dict(avg, orient = 'index')
        avg_df.reset_index(inplace = True)
        avg_df.columns = ['keyword', 'average search interest']

        ## Plotly bar chart
        import plotly.express as px

        fig = px.bar(avg_df, x = 'keyword', y = 'average search interest', color = 'keyword', \
                    color_discrete_sequence = px.colors.qualitative.Plotly)
        fig.update_layout(template = "plotly_white",
        title = "Average Interest Over Time",
            xaxis_title = "Keyword",
            yaxis_title = "Average Search Interest",
            width = 900,
            height = 700,
            showlegend = False)

        fig.show()
        

class Global_Trend:

    def __init__(self, keyword_list, timeframe):
        self.keyword_list = keyword_list
        self.timeframe = timeframe

    def get_data(self):
        
        pytrend = TrendReq()
        keywords = self.keyword_list
        pytrend.build_payload(
            kw_list = keywords,
            cat = 0,
            timeframe = self.timeframe,
            geo = '',
            gprop = '')
        data = pytrend.interest_by_region(resolution = 'COUNTRY', inc_low_vol = True, inc_geo_code = True)
        data.reset_index(inplace = True)
        data = data.replace(0, np.nan)

        return data

    def global_map(self, data):

        ## Dict with name and 3code
        count_d = dict()

        for count in pycountry.countries:
            count_d[count.alpha_2] = count.alpha_3

        ## Map country to 3code
        data['geoCode'] =  data['geoCode'].map(count_d)

        layout = go.Layout(geo=dict(bgcolor= 'rgba(0,0,0,0.8)',
                                                subunitcolor='white',showlakes = False),
                                        font = {"size": 9, "color":"Black"},
                        
                                        titlefont = {"size": 15, "color":"Black"},
                                        margin={"r":0,"t":40,"l":0,"b":0},
                                        paper_bgcolor='white',
                                        plot_bgcolor='white',
                                        )

        fig = go.Figure(data = go.Choropleth(
            locations = data['geoCode'], z = data[data.columns[2]], text = data['geoName'], colorscale = 'Blues',
            autocolorscale = False, reversescale = False, marker_line_color = 'darkgray', marker_line_width = 0.5,
            zmax = 100, zmin = 0), layout = layout)

        try:
            fig2 = go.Figure(data = go.Choropleth(
            locations = data['geoCode'], z = data[data.columns[3]], text = data['geoName'], colorscale = 'Blues',
            autocolorscale = False, reversescale = False, marker_line_color = 'darkgray', marker_line_width = 0.5,
            zmax = 100, zmin = 0), layout = layout)
            fig.add_trace(fig2.data[0])
        except:
            pass
        try:
            fig3 = go.Figure(data = go.Choropleth(
            locations = data['geoCode'], z = data[data.columns[4]], text = data['geoName'], colorscale = 'Blues',
            autocolorscale = False, reversescale = False, marker_line_color = 'darkgray', marker_line_width = 0.5,
            zmax = 100, zmin = 0), layout = layout)
            fig.add_trace(fig3.data[0])
        except:
            pass
        try:
            fig4 = go.Figure(data = go.Choropleth(
            locations = data['geoCode'], z = data[data.columns[5]], text = data['geoName'], colorscale = 'Blues',
            autocolorscale = False, reversescale = False, marker_line_color = 'darkgray', marker_line_width = 0.5,
            zmax = 100, zmin = 0), layout = layout)
            fig.add_trace(fig4.data[0])
        except:
            pass
        try:
            fig5 = go.Figure(data = go.Choropleth(
            locations = data['geoCode'], z = data[data.columns[6]], text = data['geoName'], colorscale = 'Blues',
            autocolorscale = False, reversescale = False, marker_line_color = 'darkgray', marker_line_width = 0.5,
            zmax = 100, zmin = 0), layout = layout)
            fig.add_trace(fig5.data[0])
        except:
            pass

        fig.update_layout(
            title_text = 'Interest by Country',
            width = 950,
            height = 725,
            margin = dict(
                l = 50,
                r = 50,
                b = 50,
                t = 50,
                pad = 1
            ),
            template = "plotly_white",
            geo=dict(
                showframe = False,
                showcoastlines = False,
                projection_type = 'miller'
            )
        )

        if len(data.columns[2:7]) == 1:
            fig.show()
        elif len(data.columns[2:7]) == 2:
            fig.update_layout(
                updatemenus=[
                    dict(
                        type = "buttons",
                        direction = "right",
                        active=0,
                        x=0.60,
                        y=1.05,
                        buttons=list([
                            dict(label = data.columns[2],
                                method = 'update',
                                args = [{'visible': [True, False]}]),
                            dict(label = data.columns[3],
                                method = 'update',
                                args = [{'visible': [False,True]}]),
                    ]),
                # fonts and border
                    bgcolor = 'white', 
                    bordercolor = 'lightgrey',
                    font = dict(size=10))
            ])
            fig.show()
        elif len(data.columns[2:7]) == 3:
            fig.update_layout(
                updatemenus=[
                    dict(
                        type="buttons",
                        direction="right",
                        active=0,
                        x=0.60,
                        y=1.05,
                        buttons=list([
                            dict(label = data.columns[2],
                                method = 'update',
                                args = [{'visible': [True, False, False]}]),
                            dict(label = data.columns[3],
                                method = 'update',
                                args = [{'visible': [False,True,False]}]),
                            dict(label = data.columns[4],
                                method = 'update',
                                args = [{'visible': [False,False,True]}]),
                    ]),
                # fonts and border
                    bgcolor = 'white', 
                    bordercolor = 'lightgrey',
                    font = dict(size=10))
            ])
            fig.show()
        elif len(data.columns[2:7]) == 4:
            fig.update_layout(
                updatemenus=[
                    dict(
                        type="buttons",
                        direction="right",
                        active=0,
                        x=0.60,
                        y=1.05,
                        buttons=list([
                            dict(label = data.columns[2],
                                method = 'restyle',
                                args = [{'visible': [True, False, False, False]}]),
                            dict(label = data.columns[3],
                                method = 'update',
                                args = [{'visible': [False, True, False, False]}]),
                            dict(label = data.columns[4],
                                method = 'update',
                                args = [{'visible': [False, False,True,False]}]),
                            dict(label = data.columns[5],
                                method = 'update',
                                args = [{'visible': [False, False, False, True]}]),
                    ]),
                # fonts and border
                    bgcolor = 'white', 
                    bordercolor = 'lightgrey',
                    font = dict(size=10))
            ])
            fig.show()
        elif len(data.columns[2:7]) == 5:
            fig.update_layout(
                updatemenus=[
                    dict(
                        type="buttons",
                        direction="right",
                        active=0,
                        x=1.00,
                        y=1.05,
                        buttons=list([
                            dict(label = data.columns[2],
                                method = 'update',
                                args = [{'visible': [True, False, False, False, False]}]),
                            dict(label = data.columns[3],
                                method = 'update',
                                args = [{'visible': [False,True, False, False, False]}]),
                            dict(label = data.columns[4],
                                method = 'update',
                                args = [{'visible': [False, False, True, False, False]}]),
                            dict(label = data.columns[5],
                                method = 'update',
                                args = [{'visible': [False, False, False, True, False]}]),
                            dict(label = data.columns[6],
                                method = 'update',
                                args = [{'visible': [False, False, False, False, True]}]),
                            # fonts and border
                    ]),
                # fonts and border
                    bgcolor = 'white', 
                    bordercolor = 'lightgrey',
                    font = dict(size=10))
            ])
            fig.show()
            

#from request import TrendReq

class City_Trend(TrendReq):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        

    def interest_by_region(self, resolution='CITY', inc_low_vol=True,
                           inc_geo_code=True):
        """Request data from Google's Interest by Region section and return a dataframe"""

        # make the request
        region_payload = dict()

        if self.geo == '': 
            self.interest_by_region_widget['request']['resolution'] = resolution 
        elif self.geo == 'US' and resolution in ['DMA', 'CITY', 'REGION']: 
            self.interest_by_region_widget['request']['resolution'] = resolution 
        elif len(self.geo) == 2 and resolution in ['CITY', 'REGION']:
            self.interest_by_region_widget['request']['resolution'] = resolution        

        self.interest_by_region_widget['request'][
            'includeLowSearchVolumeGeos'] = inc_low_vol

        # convert to string as requests will mangle
        region_payload['req'] = json.dumps(
            self.interest_by_region_widget['request'])
        region_payload['token'] = self.interest_by_region_widget['token']
        region_payload['tz'] = self.tz

        # parse returned json
        req_json = self._get_data(
            url=TrendReq.INTEREST_BY_REGION_URL,
            method=TrendReq.GET_METHOD,
            trim_chars=5,
            params=region_payload,
        )
        df = pd.DataFrame(req_json['default']['geoMapData'])
        df['country'] = self.geo
        #print(df)
        if (df.empty):
            return df

        # rename the column with the search keyword
        df = df[['geoName', 'coordinates', 'value', 'country']].set_index(['geoName']).sort_index()
        
        # split list columns into seperate ones, remove brackets and split on comma
        result_df = df['value'].apply(lambda x: pd.Series(
            str(x).replace('[', '').replace(']', '').split(',')))
        if inc_geo_code:
            result_df['coordinates'] = df['coordinates']

        result_df['country'] = df['country']

        # rename each column with its search term
        for idx, kw in enumerate(self.kw_list):
            result_df[kw] = result_df[idx].astype('int')
            del result_df[idx]

        return result_df

    def interest_by_city(self, data, geo_location):
        temp_df = data.copy()

        ## Append lat & lng to lists
        lat = list()
        lng = list()

        for row in range(len(temp_df['coordinates'])):
            lat.append(temp_df['coordinates'].iloc[row]['lat'])
            lng.append(temp_df['coordinates'].iloc[row]['lng'])

        ## Create region df from lists
        city_df = pd.DataFrame([lat, lng]).T
        city_df.columns = ['lat', 'long']

        ## Transform original DF
        temp_df.reset_index(inplace = True)
        city_df['name'] = temp_df['geoName']
        city_df[temp_df.columns[2]] = temp_df[temp_df.columns[2]]
        try:
            city_df[temp_df.columns[3]] = temp_df[temp_df.columns[3]]
        except: 
            pass
        try:
            city_df[temp_df.columns[4]] = temp_df[temp_df.columns[4]]
        except: 
            pass
        try:
            city_df[temp_df.columns[5]] = temp_df[temp_df.columns[5]]
        except: 
            pass
        try:
            city_df[temp_df.columns[6]] = temp_df[temp_df.columns[6]]
        except: 
            pass
        try:
            city_df[temp_df.columns[7]] = temp_df[temp_df.columns[7]]
        except: 
            pass

        ## Fetch OpenDataSoft API
        import requests
        import json
        
        def get_city_opendata(city, country):
            tmp = 'https://public.opendatasoft.com/api/records/1.0/search/?' \
            'dataset=worldcitiespop&q=%s&sort=population&facet=country&refine.country=%s'
            cmd = tmp % (city, country)
            res = requests.get(cmd)
            dct = json.loads(res.content)
            out = dct['records'][0]['fields']
            return out

        ## Calculate city pop
        if temp_df['country'].iloc[0] == 'US':
            country_opendata = 'us'
        elif temp_df['country'].iloc[0] == 'GB-ENG':
            country_opendata = 'gb'
        else:
            country_opendata = temp_df['country'].iloc[0].lower()

        city_dict = dict()
        for city in set(city_df['name']):
            try:
                city_dict[city] = get_city_opendata(city, country_opendata)['population']    
            except:
                city_dict[city] = 5000
        
        ## Map to city_df
        city_df['pop.'] = city_df['name'].map(city_dict)    

        ## Preview DF
        city_df.replace(0, np.nan, inplace = True)
        pop_col = city_df.pop('pop.')
        city_df.insert(3, 'pop.', pop_col)

        ## Center of Map based on country
        if temp_df['country'].iloc[0] == 'US':
            map_center = {'lat' : 39.00, 'lon' : -98.00}
            zoom = 3
        elif temp_df['country'].iloc[0] == 'GB-ENG':
            map_center = {'lat' : 53.0, 'lon' : -1.1743}
            zoom = 5.6
        
        ## Plot average interest
        import plotly.express as px
        px.set_mapbox_access_token('pk.eyJ1IjoiY2hlZXNldWdseSIsImEiOiJja2JqZmR5YXIwb2hoMzBycDBiNHN1MWZrIn0.RNzuuAyOAtuPcwYIZRskEQ')

        fig = px.scatter_mapbox(city_df, lat = "lat", lon = "long", color = city_df.columns[5], size = 'pop.',
                        color_continuous_scale = px.colors.sequential.Reds, size_max = 40, zoom = zoom, \
                                hover_name = city_df['name'], range_color=(0,100), \
                                center = map_center)
        try:
            fig2 = px.scatter_mapbox(city_df, lat = "lat", lon = "long", color = city_df.columns[6], size = 'pop.',
                            color_continuous_scale = px.colors.sequential.Greens, size_max = 40, zoom = 3, \
                                    hover_name = city_df['name'], range_color=(0, 100))
            fig.add_trace(fig2.data[0])
        except:
            pass
        try:
            fig3 = px.scatter_mapbox(city_df, lat = "lat", lon = "long", color = city_df.columns[7], size = 'pop.',
                            color_continuous_scale = px.colors.sequential.Greens, size_max = 40, zoom = 3, \
                                    hover_name = city_df['name'], range_color=(0,100))
            fig.add_trace(fig3.data[0])
        except:
            pass
        try:
            fig4 = px.scatter_mapbox(city_df, lat = "lat", lon = "long", color = city_df.columns[8], size = 'pop.',
                            color_continuous_scale = px.colors.sequential.Greens, size_max = 40, zoom = 3, \
                                    hover_name = city_df['name'], range_color=(0,100))
            fig.add_trace(fig4.data[0])
        except:
            pass
        try:
            fig5 = px.scatter_mapbox(city_df, lat = "lat", lon = "long", color = city_df.columns[9], size = 'pop.',
                            color_continuous_scale = px.colors.sequential.Greens, size_max = 40, zoom = 3, \
                                    hover_name = city_df['name'], range_color=(0,100))
            fig.add_trace(fig5.data[0])
        except:
            pass

        ## Got it but wrong color
        fig.update_layout(template = "plotly_white", mapbox_style = "dark", hovermode = 'closest',
        title = f"Average Interest per {geo_location} City",
            width = 950,
            height = 900,
            showlegend = False,
                        coloraxis_colorbar=dict(
            title=""))

        if len(city_df.columns[4:-1]) == 1:
            fig.show()
        elif len(city_df.columns[4:-1]) == 2:
            fig.update_layout(
                updatemenus=[
                    dict(
                        type = "buttons",
                        direction = "right",
                        active=0,
                        x=0.60,
                        y=1.05,
                        buttons=list([
                            dict(label = city_df.columns[5],
                                method = 'update',
                                args = [{'visible': [True, False]}]),
                            dict(label = city_df.columns[6],
                                method = 'update',
                                args = [{'visible': [False,True]}]),
                    ]),
                # fonts and border
                    bgcolor = 'white', 
                    bordercolor = 'lightgrey',
                    font = dict(size=10))
            ])
            fig.show()
        elif len(city_df.columns[4:-1]) == 3:
            fig.update_layout(
                updatemenus=[
                    dict(
                        type="buttons",
                        direction="right",
                        active=0,
                        x=0.60,
                        y=1.05,
                        buttons=list([
                            dict(label = city_df.columns[5],
                                method = 'update',
                                args = [{'visible': [True, False, False]}]),
                            dict(label = city_df.columns[6],
                                method = 'update',
                                args = [{'visible': [False,True,False]}]),
                            dict(label = city_df.columns[7],
                                method = 'update',
                                args = [{'visible': [False,False,True]}]),
                    ]),
                # fonts and border
                    bgcolor = 'white', 
                    bordercolor = 'lightgrey',
                    font = dict(size=10))
            ])
            fig.show()
        elif len(city_df.columns[4:-1]) == 4:
            fig.update_layout(
                updatemenus=[
                    dict(
                        type="buttons",
                        direction="right",
                        active=0,
                        x=0.60,
                        y=1.05,
                        buttons=list([
                            dict(label = city_df.columns[5],
                                method = 'restyle',
                                args = [{'visible': [True, False, False, False]}]),
                            dict(label = city_df.columns[6],
                                method = 'update',
                                args = [{'visible': [False, True, False, False]}]),
                            dict(label = city_df.columns[7],
                                method = 'update',
                                args = [{'visible': [False, False,True,False]}]),
                            dict(label = city_df.columns[8],
                                method = 'update',
                                args = [{'visible': [False, False, False, True]}]),
                    ]),
                # fonts and border
                    bgcolor = 'white', 
                    bordercolor = 'lightgrey',
                    font = dict(size=10))
            ])
            fig.show()
        elif len(city_df.columns[4:-1]) == 5:
            fig.update_layout(
                updatemenus=[
                    dict(
                        type="buttons",
                        direction="right",
                        active=0,
                        x=1.00,
                        y=1.05,
                        buttons=list([
                            dict(label = city_df.columns[5],
                                method = 'update',
                                args = [{'visible': [True, False, False, False, False]}]),
                            dict(label = city_df.columns[6],
                                method = 'update',
                                args = [{'visible': [False,True, False, False, False]}]),
                            dict(label = city_df.columns[7],
                                method = 'update',
                                args = [{'visible': [False, False, True, False, False]}]),
                            dict(label = city_df.columns[8],
                                method = 'update',
                                args = [{'visible': [False, False, False, True, False]}]),
                            dict(label = city_df.columns[9],
                                method = 'update',
                                args = [{'visible': [False, False, False, False, True]}]),
                            # fonts and border
                    ]),
                # fonts and border
                    bgcolor = 'white', 
                    bordercolor = 'lightgrey',
                    font = dict(size=10))
            ])
            fig.show()


#from request import TrendReq

class Time_Series(TrendReq):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def interest_by_region(self, resolution='COUNTRY', inc_low_vol=True,
                           inc_geo_code=False):
        """Request data from Google's Interest by Region section and return a dataframe"""

        # make the request
        region_payload = dict()

        if self.geo == '': 
            self.interest_by_region_widget['request']['resolution'] = resolution 
        elif self.geo == 'US' and resolution in ['DMA', 'CITY', 'REGION']: 
            self.interest_by_region_widget['request']['resolution'] = resolution 
        elif len(self.geo) == 2 and resolution in ['CITY', 'REGION']:
            self.interest_by_region_widget['request']['resolution'] = resolution        

        self.interest_by_region_widget['request'][
            'includeLowSearchVolumeGeos'] = inc_low_vol

        # convert to string as requests will mangle
        region_payload['req'] = json.dumps(
            self.interest_by_region_widget['request'])
        region_payload['token'] = self.interest_by_region_widget['token']
        region_payload['tz'] = self.tz

        # parse returned json
        req_json = self._get_data(
            url=TrendReq.INTEREST_BY_REGION_URL,
            method=TrendReq.GET_METHOD,
            trim_chars=5,
            params=region_payload,
        )
        df = pd.DataFrame(req_json['default']['geoMapData'])
        df['country'] = self.geo
        #print(df)
        if (df.empty):
            return df

        # rename the column with the search keyword
        df = df[['geoName', 'coordinates', 'value', 'country']].set_index(['geoName']).sort_index()
        
        # split list columns into seperate ones, remove brackets and split on comma
        result_df = df['value'].apply(lambda x: pd.Series(
            str(x).replace('[', '').replace(']', '').split(',')))
        if inc_geo_code:
            result_df['coordinates'] = df['coordinates']

        result_df['country'] = df['country']

        # rename each column with its search term
        for idx, kw in enumerate(self.kw_list):
            result_df[kw] = result_df[idx].astype('int')
            del result_df[idx]

        return result_df

    def time_series_map(self, start_date, end_date, kw_list, geo):

        if __name__=="__main__":
            pytrend = Time_Series()

        ## Initial dates
        date1 = start_date  # input start date
        date2 = end_date  # input end date

        month_list = [i.strftime("%Y-%m-%d") for i in pd.date_range(start = date1, end = date2, freq = 'MS')]

        ## Pair months
        month_pair = list()
        for i, j in zip(month_list, month_list[1:]):
            month_pair.append(i + ' ' + j)

        ## Create and populate df
        in_df = pd.DataFrame(columns = ['geoName']).set_index('geoName')

        for i in month_pair:
            self.build_payload(kw_list = kw_list, geo = geo, timeframe = i)
            df = self.interest_by_region(resolution = 'CITY', inc_low_vol = True, inc_geo_code = True)
            df['time'] = i
            in_df = in_df.append(df)

        if len(in_df) == 0:
            raise ValueError(f'not enough searches for keyword "{kw_list[0]}" in the {geo} market')

        ## Append lat & lng to lists
        lat = list()
        lng = list()

        for row in range(len(in_df['coordinates'])):
            lat.append(in_df['coordinates'].iloc[row]['lat'])
            lng.append(in_df['coordinates'].iloc[row]['lng'])

        ## Create region df from lists
        city_df = pd.DataFrame([lat, lng]).T
        city_df.columns = ['lat', 'long']

        ## DF transformations
        in_df.reset_index(inplace = True)
        try: 
            city_df['name'] = in_df['geoName']
        except:
            in_df['geoName'] = in_df['index']
            city_df['name'] = in_df['geoName']

        city_df[in_df.columns[2]] = in_df[in_df.columns[2]]
        city_df[in_df.columns[3]] = in_df[in_df.columns[3]]

        city_df['time'] = in_df['time']
        city_df[['start','finish']] = city_df['time'].str.split(' ',expand=True)

        ## Fetch OpenDataSoft API
        def get_city_opendata(city, country):
            tmp = 'https://public.opendatasoft.com/api/records/1.0/search/?' \
            'dataset=worldcitiespop&q=%s&sort=population&facet=country&refine.country=%s'
            cmd = tmp % (city, country)
            res = requests.get(cmd)
            dct = json.loads(res.content)
            out = dct['records'][0]['fields']
            return out
        
        ## Calculate city pop
        if in_df['country'].iloc[0] == 'US':
            country_opendata = 'us'
        elif in_df['country'].iloc[0] == 'GB-ENG':
            country_opendata = 'gb'
        else:
            country_opendata = in_df['country'].iloc[0].lower()

        city_dict = dict()
        for city in set(city_df['name']):
            try:
                city_dict[city] = get_city_opendata(city, country_opendata)['population']    
            except:
                city_dict[city] = 5000
        
        ## Map to city_df
        city_df['pop.'] = city_df['name'].map(city_dict)    

        ## Preview DF
        city_df.replace(0, np.nan, inplace = True)
        pop_col = city_df.pop('pop.')
        city_df.insert(3, 'pop.', pop_col)

        ## Center of Map based on country
        if in_df['country'].iloc[0] == 'US':
            map_center = {'lat' : 39.00, 'lon' : -98.00}
            zoom = 3
        elif in_df['country'].iloc[0] == 'GB-ENG':
            map_center = {'lat' : 53.0, 'lon' : -1.1743}
            zoom = 5.6

        ## Plot average interest
        import plotly.express as px
        px.set_mapbox_access_token('pk.eyJ1IjoiY2hlZXNldWdseSIsImEiOiJja2JqZmR5YXIwb2hoMzBycDBiNHN1MWZrIn0.RNzuuAyOAtuPcwYIZRskEQ')

        fig = px.scatter_mapbox(city_df, lat = "lat", lon = "long", color = city_df[city_df.columns[5]], size = city_df['pop.'],
                        color_continuous_scale = px.colors.sequential.Blues, size_max = 40, zoom = zoom, \
                                hover_name = city_df['name'], animation_frame="start", animation_group='name' , range_color=(0,100), \
                            center = map_center)

        fig.layout.updatemenus[0].buttons[0].args[1]["frame"]["duration"] = 700
        fig.layout.updatemenus[0].buttons[0].args[1]["transition"]["duration"] = 700
        fig.layout.sliders[0].pad.t = 10
        fig.layout.updatemenus[0].pad.t= 10

        fig.update_layout(template = "plotly_white", mapbox_style = "dark", hovermode = 'closest',
        title = f"Average Interest per {geo} City",
            width = 950,
            height = 900,
            showlegend = False)

        fig.show()

def time_conversion(timeframe):
    timeframe = timeframe

    if timeframe == 'today 1-m':
        today = datetime.today().strftime('%Y-%m-%d')
        date2 = datetime.strptime(today, "%Y-%m-%d")
        date1 = date2 - dateutil.relativedelta.relativedelta(months = 1)
        return date2, date1

    elif timeframe == 'today 3-m':
        today = datetime.today().strftime('%Y-%m-%d')
        date2 = datetime.strptime(today, "%Y-%m-%d")
        date1 = date2 - dateutil.relativedelta.relativedelta(months = 3)
        return date2, date1

    elif timeframe == 'today 12-m':
        today = datetime.today().strftime('%Y-%m-%d')
        date2 = datetime.strptime(today, "%Y-%m-%d")
        date1 = date2 - dateutil.relativedelta.relativedelta(months = 12)
        return date2, date1

    elif timeframe == 'today 5-y':
        today = datetime.today().strftime('%Y-%m-%d')
        date2 = datetime.strptime(today, "%Y-%m-%d")
        date1 = date2 - dateutil.relativedelta.relativedelta(years = 5)
        return date2, date1   

def run_pytrends(keyword_list, timeframe, geo_location):
    
    graphed_trend = Graphed_Trend(keyword_list, timeframe, geo_location)
    graphed_trend_data = graphed_trend.get_data()
    return1 = graphed_trend.visualise_trends(graphed_trend_data)
    return2 = graphed_trend.trend_average(graphed_trend_data)
    
    global_trend = Global_Trend(keyword_list, timeframe)
    global_trend_data = global_trend.get_data()
    return3 = global_trend.global_map(global_trend_data)
    
    city_trend = City_Trend()
    city_trend.build_payload(kw_list = keyword_list, geo = geo_location, timeframe = timeframe)
    city_trend_data = city_trend.interest_by_region()
    return4 = city_trend.interest_by_city(city_trend_data, geo_location)
    
    time_series = Time_Series()
    date1, date2 = time_conversion(timeframe)[1], time_conversion(timeframe)[0]
    return5 = time_series.time_series_map(date1, date2, [keyword_list[0]], geo_location) 

    return return1, return2, return3, return4, return5