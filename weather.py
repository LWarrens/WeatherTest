import pandas
import weather_util

def get_daylight_temperature(date, dataset):
    '''
    Takes a date and a dataset as its arguments. It returns a data structure
    with the average and standard deviation of the temperature (dry-bulb temperature)
    between the hours of sunrise and sunset
    returns a two element list of doubles in the form [mean, standard deviation]
    Keyword arguments:
    date -- date string the windchill index will be evaluated for
    dataset -- relative filepath of the dataset
    '''
    # the csv is read by the pandas library into a pandas dataframe
    data = pandas.read_csv(dataset).dropna(axis=1, how='all')
    # midday and noon times are constructed for the given date
    day_begin = pandas.Timestamp(date).replace(hour=0, minute=0, second=0, microsecond=0)
    day_end = day_begin + pandas.offsets.Day(1)
    # a mask is created to filter the dataset
    dates = pandas.to_datetime(data["DATE"])
    nullmask = pandas.notnull(data["DATE"]) & pandas.notnull(data["HOURLYDRYBULBTEMPF"])
    mask = (day_begin <= dates) & (dates < day_end) & nullmask
    days_data = data[mask]
    # get sunset and sunrise from the day's data
    if not days_data.empty:
        # extract the daily sunrise and daily sunset from the dataframe.
        # Only the first value will just be repeated for other values in the day
        index_of_first = days_data["DAILYSunrise"].keys()[0]
        sunrise_num = days_data["DAILYSunrise"][index_of_first]
        sunset_num = days_data["DAILYSunset"][index_of_first]
        # create new timestamps for sunrise and sunset
        sunrise = day_begin.replace(hour = sunrise_num / 100, minute = sunrise_num % 100)
        sunset = day_begin.replace(hour = sunset_num / 100, minute = sunset_num % 100)
        # update the filter
        days_data = days_data[(sunrise <= days_data) & (days_data <= sunset)]
        temperatures = pandas.to_numeric(days_data["HOURLYDRYBULBTEMPF"], errors='coerce')
        mean = temperatures.mean(skipna=True)
        std = temperatures.std(skipna=True)
        return [ mean, std ]
    else:
        return None

def get_sub40F_wind_chill(date, dataset):
    '''
    Takes a date and a dataset as its arguments. 
    returns the wind chill in Fahrenheit rounded to the nearest integer
    for the times when the temperature is less than 40 degrees Fahrenheit    
    Keyword arguments:
    date -- date string the windchill index will be evaluated for
    dataset -- relative filepath of the dataset the windchill will be extracted from
    '''
    only_sub40F = (lambda temperature_value: temperature_value < 40)
    return int(round(weather_util.get_wind_chill(only_sub40F, date, dataset)))

def get_most_similar_date(dataset_a, dataset_b):
    '''
    Takes two datasets and returns the day in which the conditions
    were similar between both datasets according to the similarity metric
    returns the date string for the most similar day
    Keyword arguments:
    dataset_a -- relative filepath of the first dataset
    dataset_b -- relative filepath of the second dataset
    '''
    # load both csvs
    data_a = pandas.read_csv(dataset_a).dropna(axis=1, how='all')
    data_b = pandas.read_csv(dataset_b).dropna(axis=1, how='all')
    # convert the datestring to datetime structures
    data_a["DATE"] = pandas.to_datetime(data_a["DATE"])
    data_b["DATE"] = pandas.to_datetime(data_b["DATE"])

    # convert numeric data to numeric types
    cols = ["HOURLYDRYBULBTEMPF", "HOURLYWETBULBTEMPF", "HOURLYDewPointTempF", "HOURLYAltimeterSetting", "HOURLYWindSpeed"]
    data_a[cols] = data_a[cols].apply(pandas.to_numeric, errors='coerce', axis=1)
    data_b[cols] = data_b[cols].apply(pandas.to_numeric, errors='coerce', axis=1)

    # aggregate all hourly values into columns to generate daily values in-place in the new index
    data_a = data_a.resample('d', on='DATE').mean().dropna(how='all')
    data_b = data_b.resample('d', on='DATE').mean().dropna(how='all')
    # filter out unshared days
    mask = data_a.index.intersection(data_b.index)
    data_a = data_a.ix[mask]
    data_b = data_b.ix[mask]

    best_date = None
    best_date_val = None

    for i, row in data_a.iterrows():
        similarity = weather_util.get_similarity_index(
            drybulb_a = row["HOURLYDRYBULBTEMPF"],
            wetbulb_a = row["HOURLYWETBULBTEMPF"],
            dewpoint_a= row["HOURLYDewPointTempF"],
            altimeter_a= row["HOURLYAltimeterSetting"],
            windspeed_a= row["HOURLYWindSpeed"],
            drybulb_b=data_b.loc[i]["HOURLYDRYBULBTEMPF"],
            wetbulb_b=data_b.loc[i]["HOURLYWETBULBTEMPF"],
            dewpoint_b=data_b.loc[i]["HOURLYDewPointTempF"],
            altimeter_b=data_b.loc[i]["HOURLYAltimeterSetting"],
            windspeed_b=data_b.loc[i]["HOURLYWindSpeed"]
        )
        if best_date is None or similarity <= best_date_val:
            best_date = i
            best_date_val = similarity
    if best_date:
        return best_date.strftime("%m/%d/%y")
    return None
