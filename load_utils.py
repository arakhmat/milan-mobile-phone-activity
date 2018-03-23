import pandas as pd
import geojson
import progressbar

def load_geojsons():
    
    # countries.geojson is from https://github.com/johan/world.geo.json/blob/master/countries.geo.json
    
    geojsons = {
            'grid':      'data/milano-grid.geojson',
            'provinces': 'data/Italian_provinces.geojson',
            'countries': 'data/countries.geojson',
    }
    
    for key, file_name in geojsons.items():
        with open(file_name) as json_file:
            geojsons[key] = geojson.load(json_file)
    
    return geojsons

def load_csv(file_name):
    return pd.read_csv(file_name, engine ='python', index_col=0)

def load_csvs(prefix, start_date='2013-11-01', n_days=7):
    print('Loading {} CSV file(s) with prefix "{}"'.format(n_days, prefix))
    start_date = pd.Timestamp(start_date)
    
    csvs = []
    bar = progressbar.ProgressBar(max_value=n_days)
    for i, day in enumerate(pd.date_range(start_date, periods=n_days, freq='1d')):
        csv = load_csv("data/{}-{}.csv".format(prefix, day.strftime('%Y-%m-%d')))
        csvs.append(csv)
        bar.update(i)
    return csvs
    
def load_provinces(start_date='2013-11-01', n_days=7):
    csvs = load_csvs('mi-to-provinces', start_date, n_days)
    return pd.concat(csvs)

def load_countries(start_date='2013-11-01', n_days=7):
    csvs = load_csvs('sms-call-internet-mi', start_date, n_days)
    return pd.concat(csvs)

def load_provinces_and_countries(start_date='2013-11-01', n_days=7):
    provinces_df = load_provinces(start_date, n_days)
    countries_df = load_countries(start_date, n_days)
    return provinces_df, countries_df