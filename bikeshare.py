# Importing various packages and functions needed
import time
import pandas as pd
import numpy as np

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }
cities = {'chicago', 'new york city', 'washington'}
months = {'january', 'february', 'march', 'april', 'may', 'june', 'all'}
days = {'monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday', 'all'}

def get_cmd(): #Asks user to choose a city, month, and day to analyze. I called it cmd.
    """

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('Hello! Let\'s explore some US bikeshare data!')

    # TO DO: get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs
    while True:
        city = input('What city do you want to explore: Chicago, New York City, or Washington?')
        city = city.strip().lower() #This removes any extra spaces and makes all the letters lowercase
        if city not in cities:
            print('Please select a valid city and try again.')
            continue
        else:
            break

    # TO DO: get user input for month (all, january, february, ... , june)
    while True:
        month = input('What month are you interested in? January, February, March, April, May, June, or all to see all months.')
        month = month.strip().lower()
        if month not in months:
            print('Sorry. We do not have data for that month. Please try again.')
            continue
        else:
            break
    # TO DO: get user input for day of week (all, monday, tuesday, ... sunday)
    while True:
        day = input('What day of the week would you like to see? Choose: Monday, Tuesday, Wednesday, Thursday, Friday, Saturday, Sunday, or all.')
        day = day.strip().lower()
        if day not in days:
            print('Sorry. That is not a valid day. Please try again.')
            continue
        else:
            break

    print('-'*40)
    return city, month, day

def load_cmd_data(city, month, day):
    """
    Loads data for the specified city and filters by month and day if applicable.

    Args:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    Returns:
        df - Pandas DataFrame containing city data filtered by month and day
    """
    # load data file into a dataframe
    df = pd.read_csv(CITY_DATA[city], index_col = 0)

    # convert the Start Time column to datetime
    df['Start Time'] = pd.to_datetime(df['Start Time'])

    # extract month and day of week from Start Time to create new columns
    df['month'] = df['Start Time'].dt.month
    df['day'] = df['Start Time'].dt.day_name()


    # filter by month if applicable
    if month != 'all':
        # use the index of the months list to get the corresponding int
        months = ['january', 'february', 'march', 'april', 'may', 'june']
        month = months.index(month) + 1

        # filter by month to create the new dataframe
        df = df[df['month'] == month]

    # filter by day of week if applicable
    if day != 'all':
        # filter by day of week to create the new dataframe
        df = df[df['day'] == day.title()]

    return df

def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # TO DO: display the most common month
    popular_month = df['month'].mode()[0]
    print('The most common month for bike rentals is: ', popular_month)

    # TO DO: display the most common day of week
    popular_day = df['day'].mode()[0]
    print('The most common day for bike rentals is: ', popular_day)

    # TO DO: display the most common start hour
    # extract hour from the Start Time column to create an hour column
    df['hour'] = df['Start Time'].dt.hour

    # find the most popular hour
    popular_hour = df['hour'].mode()[0]
    print('The most common hour for bike rentals is: ', popular_hour)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # TO DO: display most commonly used start station
    popular_start_station = df['Start Station'].mode()[0]
    print('The most common start station for bike rentals is: ', popular_start_station)

    # TO DO: display most commonly used end station
    popular_end_station = df['End Station'].mode()[0]
    print('The most common end station for bike rentals is: ', popular_end_station)

    # TO DO: display most frequent combination of start station and end station trip
    popular_start_end_station = df.groupby(['Start Station','End Station']).size().nlargest(1)
    print('The most common combination of start station and end station for bike rentals is:\n', popular_start_end_station)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # TO DO: display total travel time
    total_time = df['Trip Duration'].sum()
    print('The total trip time for bike rentals is: ', total_time, 'seconds')

    # TO DO: display mean travel time
    mean_time = df['Trip Duration'].mean()
    print('The mean trip time for bike rentals is: ', mean_time, 'seconds')

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # TO DO: Display counts of user types
    user_count = df['User Type'].value_counts()
    print('Break down of users by user type:\n', user_count)

    # TO DO: Display counts of gender
    #washington.csv doesn't have gender column
    if 'Gender' in df.columns:
        gender_count = df['Gender'].value_counts()
        print('Break down of users by gender:\n', gender_count)
    else:
        print('Washington does not have gender data.')

    # TO DO: Display earliest, most recent, and most common year of birth
    if 'Birth Year' in df.columns:
        #earliest birth year
        earliest_year = df['Birth Year'].min()
        print('Birth year of the oldest user: ', earliest_year)

        #most recent birth year
        recent_year = df['Birth Year'].max()
        print('Birth year of the youngest user: ', recent_year)

        #most common birth year
        popular_year = df['Birth Year'].value_counts().idxmax()
        print('Most common birth year for users: ', popular_year)
    else:
        print('Washington does not have birth year data.')

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def show_raw_data(df):
    """Displays 5 rows of raw data upon user request.

    Args:
        (DataFrame) df - Contains city data that is filtered by month and day
    """
    print(df.head())
    start_loc = 0
    while True:
        show_raw_data = input('Would you like to see the next 5 rows of individual trip data? Enter yes or no.')
        show_raw_data = show_raw_data.strip().lower()
        if show_raw_data != 'yes':
            return
        start_loc +=5
        print(df.iloc[start_loc:start_loc + 5])



def main():
    while True:
        city, month, day = get_cmd()
        df = load_cmd_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)
        show_raw_data(df)

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
	main()

"""

Helpful References
While loops: https://www.w3schools.com/python/python_while_loops.asp
Functions: https://www.programiz.com/python-programming/function

"""
