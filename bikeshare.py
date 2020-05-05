import time
import pandas as pd
import numpy as np

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }

def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('Hello! Let\'s explore some US bikeshare data!')
    #  get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs
    x = 0
    while x == 0:
        city = input('Which city are you interested in (Chicago, New York City, Washington)?\n').title()
        if city == 'Chicago' or city == 'New York City' or city == 'Washington':
            x = 1
        else:
            print('Sorry! I don\'t regognize that city\n')
    print('You\'ve selected',city,'!')
    #  get user input for month (all, january, february, ... , june)
    x = 0
    while x == 0:
        month = input('What month are you interested in looking at? (January, February, March, April, May, June, All)\n').title()
        if month == 'All' or month == 'January' or month == 'February' or month == 'March' or month == 'April' or month == 'May' or month == 'June':
            x = 1
            print('You\'ve selected',month,'!')
        else:
            print('I\'m sorry, I don\'t recognize that month.')


    #  get user input for day of week (all, monday, tuesday, ... sunday)
    x = 0
    while x == 0:
        day = input('What day of the week are you interested in looking at? (Monday, Tuesday, Wednesday, Thursday, Friday, Saturday, Sunday, All)\n').title()
        if day == 'All' or day == 'Monday' or day == 'Tuesday' or day == 'Wednesday' or day == 'Thursday' or day == 'Friday' or day == 'Saturday' or day == 'Sunday':
            x = 1
            print('You\'ve selected',day,'!')
        else:
            print('I\'m sorry, I don\'t recognize that day.')

    print('-'*40)
    return city, month, day


def load_data(city, month, day):
    """
    Loads data for the specified city and filters by month and day if applicable.

    Args:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    Returns:
        df - Pandas DataFrame containing city data filtered by month and day
    """
    #Load data file into dataframe
    df = pd.read_csv(CITY_DATA[city.lower()])
    #Convert Start Time column to datetime
    df['Start Time'] = pd.to_datetime(df['Start Time'])
    #Extract month and day of week from start time
    df['Month'] = df['Start Time'].dt.month
    df['Weekday'] = df['Start Time'].dt.weekday_name
    if month != 'All':
        months = ['January','February','March','April','May','June','July']
        month_number = months.index(month) + 1
        df = df[df['Month'] == month_number]

    if day != 'All':
       df = df[df['Weekday'] == day.title()]

    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    #  display the most common month\
    months = ['January','February','March','April','May','June','July']
    most_common_month = df['Month'].mode()[0]
    print('The most popular month for bike rentals is',months[most_common_month-1],'.')

    #  display the most common day of week
    most_common_day = df['Weekday'].mode()[0]
    print('The most popular day of the week for bike rentals is',most_common_day,'.')

    #  display the most common start hour

    # convert the Start Time column to datetime
    df['Start Time'] = pd.to_datetime(df['Start Time'])
    #Extract Hour from the Start Time and create a column
    df['Hour'] = df['Start Time'].dt.hour
    #Find the most common hour of starting usage
    popular_hour = df['Hour'].mode()[0]
    print('The most common start time for usage in this data set is:',popular_hour,': 00.')

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    #  display most commonly used start station
    most_common_start_station = df['Start Station'].mode()[0]
    print('The most common starting station is',most_common_start_station)

    #  display most commonly used end station
    most_common_end_station = df['End Station'].mode()[0]
    print('The most common ending station is',most_common_end_station)

    #  display most frequent combination of start station and end station trip
    trip_start_stop_counts = df.groupby(['Start Station','End Station'])['Start Station'].size().sort_values().index[-1]
    start_trip = trip_start_stop_counts[0]
    stop_trip = trip_start_stop_counts[1]
    print('The most common tip taken is',start_trip,'to',stop_trip)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    #  display total travel time
    total_travel_time = df['Trip Duration'].sum()
    print('The total travel time on these bicycles is',total_travel_time,'seconds.')

    #  display mean travel time
    mean_travel_time = df['Trip Duration'].mean()
    print('The average travel time for each trip is',mean_travel_time,'seconds.')

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    #  Display counts of user types
    user_type_counts = df['User Type'].value_counts()
    print('Here are the counts of each user type:')

    for i in range(user_type_counts.index.size):
        print(user_type_counts.index[i],' \t:\t',user_type_counts[i])

    #  Display counts of gender
    if 'Gender'in df.columns:
        gender_counts = df['Gender'].value_counts()
        print('\nHere are the number of rides broken down by gender:')
        for i in range(gender_counts.index.size):
            print(gender_counts.index[i],'\t:\t',gender_counts[i])
    else:
        print('\nThere is no gender data for this city!')

    #  Display earliest, most recent, and most common year of birth
    if 'Birth Year' in df.columns:
        min_birth_year = df['Birth Year'].min()
        max_birth_year = df['Birth Year'].max()
        most_common_birth_year = df['Birth Year'].mode()
        print('\nThe earliest birth year is',int(min_birth_year))
        print('The most recent birth year is',int(max_birth_year))
        print('The most common birth year is',int(most_common_birth_year))
    else:
        print('There is no birth year data for this city!')

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def raw_data_disp(df):
    x = 1
    row_count = 0
    df = df.reset_index()
    while x == 1:
        show_raw_data = input('Would you like to see 5 lines of raw data? (Yes/No)').title()
        if show_raw_data != 'Yes' and show_raw_data != 'No':
            print('I don\'t recognize that answer, please try again (Yes/No)')
        elif show_raw_data == 'Yes':
            row_count_end = row_count + 4
            print(df.loc[row_count : row_count_end,:])
            row_count = row_count_end + 1
        else:
            x = 0

def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)
        raw_data_disp(df)

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
	main()
