# -*- coding: utf-8 -*-
# Problem Set 5: Experimental Analysis
# Name: 
# Collaborators (discussion):
# Time:

import pylab
import re

#note: from experiment, numpy can replace pylab without any error
import numpy as np

from matplotlib import pyplot as plt

# cities in our weather data
CITIES = [
    'BOSTON',
    'SEATTLE',
    'SAN DIEGO',
    'PHILADELPHIA',
    'PHOENIX',
    'LAS VEGAS',
    'CHARLOTTE',
    'DALLAS',
    'BALTIMORE',
    'SAN JUAN',
    'LOS ANGELES',
    'MIAMI',
    'NEW ORLEANS',
    'ALBUQUERQUE',
    'PORTLAND',
    'SAN FRANCISCO',
    'TAMPA',
    'NEW YORK',
    'DETROIT',
    'ST LOUIS',
    'CHICAGO'
]

TRAINING_INTERVAL = range(1961, 2010)
TESTING_INTERVAL = range(2010, 2016)

"""
Begin helper code
"""
class Climate(object):
    """
    The collection of temperature records loaded from given csv file
    """
    def __init__(self, filename):
        """
        Initialize a Climate instance, which stores the temperature records
        loaded from a given csv file specified by filename.

        Args:
            filename: name of the csv file (str)
        """
        self.rawdata = {}

        f = open(filename, 'r')
        header = f.readline().strip().split(',')
        for line in f:
            items = line.strip().split(',')

            date = re.match('(\d\d\d\d)(\d\d)(\d\d)', items[header.index('DATE')])
            year = int(date.group(1))
            month = int(date.group(2))
            day = int(date.group(3))

            city = items[header.index('CITY')]
            temperature = float(items[header.index('TEMP')])
            if city not in self.rawdata:
                self.rawdata[city] = {}
            if year not in self.rawdata[city]:
                self.rawdata[city][year] = {}
            if month not in self.rawdata[city][year]:
                self.rawdata[city][year][month] = {}
            self.rawdata[city][year][month][day] = temperature
            
        f.close()

    def get_yearly_temp(self, city, year):
        """
        Get the daily temperatures for the given year and city.

        Args:
            city: city name (str)
            year: the year to get the data for (int)

        Returns:
            a 1-d pylab array of daily temperatures for the specified year and
            city
        """
        temperatures = []
        assert city in self.rawdata, "provided city is not available"
        assert year in self.rawdata[city], "provided year is not available"
        for month in range(1, 13):
            for day in range(1, 32):
                if day in self.rawdata[city][year][month]:
                    temperatures.append(self.rawdata[city][year][month][day])
        return pylab.array(temperatures)

    def get_daily_temp(self, city, month, day, year):
        """
        Get the daily temperature for the given city and time (year + date).

        Args:
            city: city name (str)
            month: the month to get the data for (int, where January = 1,
                December = 12)
            day: the day to get the data for (int, where 1st day of month = 1)
            year: the year to get the data for (int)

        Returns:
            a float of the daily temperature for the specified time (year +
            date) and city
        """
        assert city in self.rawdata, "provided city is not available"
        assert year in self.rawdata[city], "provided year is not available"
        assert month in self.rawdata[city][year], "provided month is not available"
        assert day in self.rawdata[city][year][month], "provided day is not available"
        return self.rawdata[city][year][month][day]

def se_over_slope(x, y, estimated, model):
    """
    For a linear regression model, calculate the ratio of the standard error of
    this fitted curve's slope to the slope. The larger the absolute value of
    this ratio is, the more likely we have the upward/downward trend in this
    fitted curve by chance.
    
    Args:
        x: an 1-d pylab array with length N, representing the x-coordinates of
            the N sample points
        y: an 1-d pylab array with length N, representing the y-coordinates of
            the N sample points
        estimated: an 1-d pylab array of values estimated by a linear
            regression model
        model: a pylab array storing the coefficients of a linear regression
            model

    Returns:
        a float for the ratio of standard error of slope to slope
    """
    assert len(y) == len(estimated)
    assert len(x) == len(estimated)
    EE = ((estimated - y)**2).sum()
    var_x = ((x - x.mean())**2).sum()
    SE = pylab.sqrt(EE/(len(x)-2)/var_x)
    return SE/model[0]

"""
End helper code
"""

def generate_models(x, y, degs=[1]):
    """
    Generate regression models by fitting a polynomial for each degree in degs
    to points (x, y).

    Args:
        x: an 1-d pylab array with length N, representing the x-coordinates of
            the N sample points
        y: an 1-d pylab array with length N, representing the y-coordinates of
            the N sample points
        degs: a list of degrees of the fitting polynomial

    Returns:
        a list of pylab arrays, where each array is a 1-d array of coefficients
        that minimizes the squared error of the fitting polynomial
    """
    ls_coeffs = [pylab.polyfit(x,y,deg) for deg in degs]
    return ls_coeffs


def r_squared(y, estimated):
    """
    Calculate the R-squared error term.
    
    Args:
        y: 1-d pylab array with length N, representing the y-coordinates of the
            N sample points
        estimated: an 1-d pylab array of values estimated by the regression
            model

    Returns:
        a float for the R-squared error term
    """
    sum_square_residual = pylab.sum((y -estimated)**2)
    sum_square_total = pylab.sum((y - pylab.mean(y))**2)
    r_squared = 1 - sum_square_residual/sum_square_total

    return r_squared


def evaluate_models_on_training(x, y, models):
    """
    For each regression model, compute the R-squared value for this model with the
    standard error over slope of a linear regression line (only if the model is
    linear), and plot the data along with the best fit curve.

    For the plots, you should plot data points (x,y) as blue dots and your best
    fit curve (aka model) as a red solid line. You should also label the axes
    of this figure appropriately and have a title reporting the following
    information:
        degree of your regression model,
        R-square of your model evaluated on the given data points,
        and SE/slope (if degree of this model is 1 -- see se_over_slope). 

    Args:
        x: an 1-d pylab array with length N, representing the x-coordinates of
            the N sample points
        y: an 1-d pylab array with length N, representing the y-coordinates of
            the N sample points
        models: a list containing the regression models you want to apply to
            your data. Each model is a pylab array storing the coefficients of
            a polynomial.

    Returns:
        None
    """
    for model in models:
        model_function = pylab.poly1d(model)
        r_2 = r_squared(y, model_function(x))

        plt.figure()
        plt.plot(x, y, 'bo', label='data points')
        plt.plot(x, model_function(x), 'r-', label='model line')
        plt.legend(loc='best')
        if len(model) > 1:
            plt.title(f'Degree of fit: {len(model) - 1} \n R2: {r_2} \n Ratio of SE: {se_over_slope(x, y, model_function(x), model)}.')
        else:
            plt.title(f'Degree of fit: {len(model) - 1} \n R2: {r_2}')
        plt.xlabel('Year')
        plt.ylabel('Temperature in Celsius')
        plt.show()

def get_temperature_multi_cities_specific_year(climate, multi_cities, year):
    temperature_all = np.empty(0)

    for city in multi_cities:
        temperature = climate.get_yearly_temp(city, year)
        temperature_all = np.append(temperature_all, temperature)
    
    return temperature_all

def gen_cities_avg(climate:object, multi_cities:list, years:list):
    """
    Compute the average annual temperature over multiple cities.

    Args:
        climate: instance of Climate
        multi_cities: the names of cities we want to average over (list of str)
        years: the range of years of the yearly averaged temperature (list of
            int)

    Returns:
        a pylab 1-d array of floats with length = len(years). Each element in
        this array corresponds to the average annual temperature over the given
        cities for a given year.
    """
    avg_temperature_years = np.empty(0)

    for year in years:
        temperature_all = get_temperature_multi_cities_specific_year(climate, multi_cities, year)
        avg_temperature_years = np.append(avg_temperature_years, temperature_all.mean())
    
    return avg_temperature_years


def moving_average(y, window_length):
    """
    Compute the moving average of y with specified window length.

    Args:
        y: an 1-d pylab array with length N, representing the y-coordinates of
            the N sample points
        window_length: an integer indicating the window length for computing
            moving average

    Returns:
        an 1-d pylab array with the same length as y storing moving average of
        y-coordinates of the N sample points
    """
    moving_average = np.empty(0)

    for index in range(len(y)):
        lower_index = max(0, index - window_length + 1)
        sliced_y = np.array(y[lower_index:(index + 1)])
        moving_average = np.append(moving_average, sliced_y.mean())
    
    return moving_average


def rmse(y, estimated):
    """
    Calculate the root mean square error term.

    Args:
        y: an 1-d pylab array with length N, representing the y-coordinates of
            the N sample points
        estimated: an 1-d pylab array of values estimated by the regression
            model

    Returns:
        a float for the root mean square error term
    """
    mse = pylab.sum((y - estimated)**2)/len(y)
    rmse = mse**(1/2)
    return rmse

def gen_std_devs(climate, multi_cities, years):
    """
    For each year in years, compute the standard deviation over the averaged yearly
    temperatures for each city in multi_cities. 

    Args:
        climate: instance of Climate
        multi_cities: the names of cities we want to use in our std dev calculation (list of str)
        years: the range of years to calculate standard deviation for (list of int)

    Returns:
        a pylab 1-d array of floats with length = len(years). Each element in
        this array corresponds to the standard deviation of the average annual 
        city temperatures for the given cities in a given year.
    """
    std_avg_temperature_years = np.empty(0)

    for year in years:

        temperature_cities  = np.array([climate.get_yearly_temp(city, year) for city in multi_cities])
        temperature_cities_daily_mean = np.mean(temperature_cities, axis=0)
        temperature_cities_daily_std = temperature_cities_daily_mean.std()
        std_avg_temperature_years = np.append(std_avg_temperature_years, temperature_cities_daily_std)

    return std_avg_temperature_years

def evaluate_models_on_testing(x, y, models):
    """
    For each regression model, compute the RMSE for this model and plot the
    test data along with the model???s estimation.

    For the plots, you should plot data points (x,y) as blue dots and your best
    fit curve (aka model) as a red solid line. You should also label the axes
    of this figure appropriately and have a title reporting the following
    information:
        degree of your regression model,
        RMSE of your model evaluated on the given data points. 

    Args:
        x: an 1-d pylab array with length N, representing the x-coordinates of
            the N sample points
        y: an 1-d pylab array with length N, representing the y-coordinates of
            the N sample points
        models: a list containing the regression models you want to apply to
            your data. Each model is a pylab array storing the coefficients of
            a polynomial.

    Returns:
        None
    """
    for model in models:
        model_function = pylab.poly1d(model)
        rmse_result = rmse(y, model_function(x))

        plt.figure()
        plt.plot(x, y, 'bo', label='data points')
        plt.plot(x, model_function(x), 'r-', label='model line')
        plt.legend(loc='best')
        if len(model) > 1:
            plt.title(f'Degree of fit: {len(model) - 1} \n RMSE: {rmse_result}')
        else:
            plt.title(f'Degree of fit: {len(model) - 1} \n RMSE: {rmse_result}')
        plt.xlabel('Year')
        plt.ylabel('Temperature in Celsius')
        plt.show()

def answering_part_a4_part1():
    climate = Climate('data.csv')
    temperature_data = [climate.get_daily_temp("NEW YORK", 1, 10, year) for year in range(1961, 2010)]

    x_axis_array = np.array(range(1961, 2010))
    y_axis_array = np.array(temperature_data)

    models = generate_models(x_axis_array, y_axis_array)
    evaluate_models_on_training(x_axis_array, y_axis_array, models)


def answering_part_a4_part2():
    climate = Climate('data.csv')
    avg_temperature_data = gen_cities_avg(climate, ["NEW YORK"], range(1961, 2010))

    x_axis_array = np.array(range(1961, 2010))
    y_axis_array = np.array(avg_temperature_data)

    models = generate_models(x_axis_array, y_axis_array)
    evaluate_models_on_training(x_axis_array, y_axis_array, models)

def answering_part_b():
    climate = Climate('data.csv')
    ls_cities = list(climate.rawdata.keys())
    avg_temperature_data_cities = gen_cities_avg(climate, ls_cities, range(1961, 2010))

    x_axis_array = np.array(range(1961, 2010))
    y_axis_array = np.array(avg_temperature_data_cities)

    models = generate_models(x_axis_array, y_axis_array)
    evaluate_models_on_training(x_axis_array, y_axis_array, models)

def answering_part_c():
    climate = Climate('data.csv')
    ls_cities = list(climate.rawdata.keys())
    
    avg_temperature_data_cities = gen_cities_avg(climate, ls_cities, range(1961, 2010))
    ma_avg_temperature_cities = moving_average(avg_temperature_data_cities, 5)

    x_axis_array = np.array(range(1961, 2010))
    y_axis_array = np.array(ma_avg_temperature_cities)

    models = generate_models(x_axis_array, y_axis_array)
    evaluate_models_on_training(x_axis_array, y_axis_array, models)


def answering_part_d_pb1():
    climate = Climate('data.csv')
    ls_cities = list(climate.rawdata.keys())
    
    avg_temperature_data_cities = gen_cities_avg(climate, ls_cities, range(1961, 2010))
    ma_avg_temperature_cities = moving_average(avg_temperature_data_cities, 5)

    x_axis_array = np.array(range(1961, 2010))
    y_axis_array = np.array(ma_avg_temperature_cities)

    models = generate_models(x_axis_array, y_axis_array, [1, 2, 20])
    evaluate_models_on_training(x_axis_array, y_axis_array, models)


def answering_part_d_pb2():
    climate = Climate('data.csv')
    ls_cities = list(climate.rawdata.keys())
    
    """
    training dataset
    """
    avg_train_temperature_data_cities = gen_cities_avg(climate, ls_cities, range(1961, 2010))
    ma_train_avg_temperature_cities = moving_average(avg_train_temperature_data_cities, 5)

    x_train_array = np.array(range(1961, 2010))
    y_train_array = np.array(ma_train_avg_temperature_cities)

    models = generate_models(x_train_array, y_train_array, [1, 2, 20])

    """
    Test dataset
    """
    avg_test_temperature_data_cities = gen_cities_avg(climate, ls_cities, range(2010, 2016))
    ma_test_avg_temperature_cities = moving_average(avg_test_temperature_data_cities, 5)

    x_test_array = np.array(range(2010, 2016))
    y_test_array = np.array(ma_test_avg_temperature_cities)

    evaluate_models_on_testing(x_test_array, y_test_array, models)


def answering_part_e():
    climate = Climate('data.csv')
    ls_cities = list(climate.rawdata.keys())
    
    std_temperature_data_cities = gen_std_devs(climate, ls_cities, range(1961, 2010))
    ma_std_temperature_data_cities = moving_average(std_temperature_data_cities, 5)

    x_axis_array = np.array(range(1961, 2010))
    y_axis_array = np.array(ma_std_temperature_data_cities)

    models = generate_models(x_axis_array, y_axis_array)
    evaluate_models_on_training(x_axis_array, y_axis_array, models)


if __name__ == '__main__':

    # pass 

    # Part A.4
    """
    The model with degree of one tell us that there is an incremental trend of temperature on annually basis
    The trend of the avg temperature of New York also confirm the incremetal trend of temperature

    The average data tend to be less noisy than the only data point of the year
    The average data also prone to confirm that temperature has trend more than the data point model judeged from SE OVER SLOPE
    """
    # answering_part_a4_part1()
    # answering_part_a4_part2()

    # Part B
    """
    Considering all city in USA confirm an incrementatl trend of temperature with hige value of R^2 and low value for SE OVER SLOPE
    
    Using 3 cities may get different resulr from 100 cities depending on used cities which may get different effect from global warming

    Using cities in the same region may lead to bias in conclusion as the same region may get the result represents for that only region
    
    """
    # answering_part_b()

    # Part C
    """
    As moving average help to reduce noise.

    The model from miving average is also confirm trend in incremental tempreature with higher r square and se over slope
    """
    # answering_part_c()

    # Part D.2
    """
    The higher polynomial degree give higher r-squre.
    However, the higher polynomial degree lead to higher rmse from high variance of model
    """
    # answering_part_d_pb1()
    # answering_part_d_pb2()

    # Part E
    """
    Trend of standard deviation is deremental across period of time which confirm that in the later years, 
    the result of the linear regression model can be conclusive and confirm the existance of "Glogal Warming"
    """
    answering_part_e()


