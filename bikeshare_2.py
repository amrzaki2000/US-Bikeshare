import time
import pandas as pd
import numpy as np

CITY_DATA = {'chicago': 'chicago.csv',
             'new york city': 'new_york_city.csv',
             'washington': 'washington.csv'}

filter_ = 'none'
valid_cities = ['chicago', 'new york city', 'washington']
valid_months = ['all', 'january', 'february', 'march', 'april', 'may', 'june']
valid_days = ['all', 'saturday', 'sunday', 'monday', 'tuesday', 'wednesday', 'thursday', 'friday']


def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    global filter_, valid_days, valid_months, valid_cities
    month = 'all'
    day = 'all'
    print('Hello! Let\'s explore some US bike-share data!')

    # get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs

    city = input('Enter the city name to be analyzed (chicago, new york city, washington): ').lower().strip()
    while city not in valid_cities:
        city = input('Please enter only one of the mentioned three cities (chicago, new york city, washington):').lower().strip()

    # get user input for month (all, january, february, ... , june)
    
    filter_ = input('How do you want to filter data (month or day or both or none for no filters) : ')
    while filter_ not in ['day', 'month', 'both', 'none']:
        filter_ = input('Please follow input instructions (month or day or both or none for no filters): ')

    if filter_ == 'month' or filter_ == 'both':
        month = input('Enter the month name to filter by (from january to june or \'all\' to skip filter):').lower().strip()
        while month not in valid_months:
            month = input('Please enter a valid month (from january to june or all to skip filter):').lower().strip()

    # get user input for day of week (all, monday, tuesday, ... sunday)
    if filter_ == 'day' or filter_ == 'both':
        day = input('Please enter the day name to filter by (\'all\' to skip filter) :').lower().strip()
        while day not in valid_days:
            day = input('Please enter a valid day:').lower().strip()

    print('-' * 40)

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

    global valid_months
    df = pd.read_csv(CITY_DATA[city])
    df['Start Time'] = pd.to_datetime(df['Start Time'])
    df['month'] = df['Start Time'].dt.month
    df['day'] = df['Start Time'].dt.day_name()
    df['start_hour'] = df['Start Time'].dt.hour

    if month != 'all':
        month = valid_months.index(month)
        df = df[df['month'] == month]
    if day != 'all':
        df = df[df['day'] == day.title()]

    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    global filter_
    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    if filter_ != 'month' and filter_ != 'both':
        # display the most common month
        common_month = df['month'].mode()[0]
        month_name = valid_months[common_month].title()
        count_month = df[df['month'] == common_month].count()[0]

        print(f'Most common month is: {month_name},Count of common month: {count_month},Filter:{filter_}')

    if filter_ != 'day' and filter_ != 'both':
        # display the most common day of week
        common_day = df['day'].mode()[0]
        count_day = df[df['day'] == common_day].count()[0]

        print(f'Most common day is: {common_day}, Count of common month: {count_day}, Filter:{filter_}')

    # display the most common start hour
    common_hour = df['start_hour'].mode()[0]

    count_hour = df[df['start_hour'] == common_hour].count()[0]

    print(f'Most common start hour is: {common_hour}, Count of common month: {count_hour}, Filter:{filter_}')

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-' * 40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""
    global filter_
    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station
    common_start_station = df['Start Station'].mode()[0]
    count_start_station = df[df['Start Station'] == common_start_station].count()[0]

    print(f'Most common start station is: {common_start_station}, '
          f'Count:{count_start_station}, Filter:{filter_}')

    # display most commonly used end station
    common_end_station = df['End Station'].mode()[0]
    count_end_station = df[df['End Station'] == common_end_station].count()[0]

    print(f'Most common end station is: {common_end_station}, '
          f'Count:{count_end_station}, Filter:{filter_}')

    # display most frequent combination of start station and end station trip
    df['Start & End'] = 'From ' + df['Start Station'] + ' To ' + df['End Station']
    common_combination = df['Start & End'].mode()[0]
    count_combination = df[df['Start & End'] == common_combination].count()[0]
    print(f'Most common combination of start & end stations is: {common_combination}\n, '
          f'Count:{count_combination}, Filter:{filter_}')

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-' * 40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # display total travel time
    total_trip_duration = df['Trip Duration'].sum()
    print(f'Total travel time of all trips: {total_trip_duration} seconds, approx. {total_trip_duration//60} minutes, '
          f'approx {(total_trip_duration//60)//60} hours')

    # display mean travel time
    avg_trip_duration = df['Trip Duration'].mean()
    print(f'Average travel time of all trips: {avg_trip_duration} seconds, approx {avg_trip_duration/60} minutes')

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-' * 40)


def user_stats(df, city):
    """Displays statistics on bike-share users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    print('Counts of User types are == >')
    types = df['User Type'].value_counts()
    for user, count in types.items():
        print(user, ":", count)

    if city != 'washington':
        # Display counts of gender
        print('Counts of Gender are ==> ')
        genders = df['Gender'].value_counts()
        for gender, count in genders.items():
            print(gender, ":", count)

        # Display earliest, most recent, and most common year of birth
        print('\nEarliest year of birth is:', df[pd.notnull(df['Birth Year'])]['Birth Year'].min())
        print('Most recent year of birth is:', df[pd.notnull(df['Birth Year'])]['Birth Year'].max())
        print('Most common year of birth is:', df[pd.notnull(df['Birth Year'])]['Birth Year'].mode()[0])

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-' * 40)


def show_raw_data(city):
    display_data = pd.read_csv(CITY_DATA[city])
    display_data.fillna('Information Not available', inplace=True)
    i = 0
    ans = 'yes'
    while ans == 'yes' and i +5 < len(display_data.index):
        print(display_data[i:i+5])
        i += 5
        ans = input('Do you want to show more data ? ( yes or no )').lower().strip()
        while ans not in ['yes', 'no']:
            ans = input('Please enter yes or no only: ').lower().strip()

        if ans == 'no':
            return


def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df, city)
        show_raw_data(city)
        restart = input('\nWould you like to restart? Enter yes or no.\n')

        if restart.lower().strip() != 'yes':
            print('Thank you for using our services !')
            break


if __name__ == "__main__":
    main()
