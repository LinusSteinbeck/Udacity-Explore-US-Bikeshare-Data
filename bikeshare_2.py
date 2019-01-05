import time
import pandas as pd
import numpy as np
import datetime
import matplotlib.pyplot as plt

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
    unknown = "Unknown input, please do again"


    print('Hello! Let\'s explore some US bikeshare data!')
    # get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs
    while True:
        city = input("\nWould you see data from Chicago, New York City or Washington\n").lower()
        if city in ['chicago', 'new york city', 'washington']:
            break
        else:
            print(unknown)


    # get user input for month (all, january, february, ... , june)
    while True:
        month = input("\nWhich month? January, February, March, April, May, June or do you want see all?\n").lower()
        if month in ["january", "february", "march", "april", "may", "june", "all"]:
            break
        else:
            print(unknown)


    # get user input for day of week (all, monday, tuesday, ... sunday)
    while True:
        day = input("\nWich day you want to see? Monday, Tuesday, Wednesday, Thursday, Friday, Saturday, Sunday or all\n").lower()
        if day in ["monday", "tuesday", "wednesday", "thursday", "friday", "saturday", "sunday", "all"]:
            break
        else:
            print(unknown)



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
    file_name = CITY_DATA[city]
    print("Starts loading data from" + file_name + "...")
    df = pd.read_csv(file_name)

    df["Start Time"] = pd.to_datetime(arg=df["Start Time"], errors="coerce", format='%Y-%m-%d %H:%M:%S')

    if month != "all":
        df["month"] = df["Start Time"].dt.month


        months = ["january", "february", "march", "april", "may", "june"]
        month = months.index(month) + 1

        df = df.loc[df["month"] == month]

    if day != "all":
        df["day_of_week"] = df["Start Time"].dt.weekday_name

        df = df.loc[df["day_of_week"] == day.title()]


    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    df["Start Time"] = pd.to_datetime(arg=df["Start Time"], errors="coerce", format="'%Y-%m-%d %H:%M:%S'")

    month = df["Start Time"].dt.month

    weekday_name = df["Start Time"].dt.weekday_name

    hour = df["Start Time"].dt.hour

    # display the most common month
    most_common_day_of_week = month.mode()[0]
    print("Most common day of week:", most_common_day_of_week)


    # display the most common day of week
    most_common_day_of_week = weekday_name.mode()[0]
    print("Most comon day of the week", most_common_day_of_week)


    # display the most common start hour
    popular_hour = hour.mode()[0]
    print("Most frequent start hour:", popular_hour)


    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station
    print ("The most used start station is:", df["Start Station"].value_counts().idxmax())

    # display most commonly used end station
    print ("The most used end station is:", df["End Station"].value_counts().idxmax())


    # display most frequent combination of start station and end station trip
    combined_stations = df["Start Station"] + "*" + df["End Station"]
    most_used_combination = combined_stations.value_counts().idxmax()
    print ("Most used combinations, start from\n{} \nto\n{}".format(most_used_combination.split("*")[0], most_used_combination.split("*")[1]))



    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

def print_numbers_for_easier_reading(seconds):
    m, s = divmod(seconds, 60)
    h, m = divmod(m, 60)
    d, h = divmod(h, 24)
    y, d = divmod(d, 365)
    print("Years: {}, Days: {}, Hours: {}, Mins: {}, Secs: {}".format(y,d,h,m,s))

    # display total travel time
    total_travel_time = df["Trip Duration"].mean()
    print("Total travel time:\n")
    print_numbers_for_easier_reading(total_travel_time)


    # display mean travel time
    mean_travel_time = df["Trip Duration"].mean()
    print ("\nMean travel time: {} seconds".format(mean_travel_time))


    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    user_types = df["User Type"].value_counts()
    print(user_types)


    # Display counts of gender
    if "Gender" in df.columns:
        gender_counts = df["Gender"].value_counts()
        print(gender_counts)

    # Display earliest, most recent, and most common year of birth
    if 'Birth Year' in df.columns:
        earliest_year = df['Birth Year'].min()
        most_recent_year = df['Birth Year'].max()
        most_common_birth_year = df['Birth Year'].mode()[0]
        print("\nEarliest year of birth: " + str(earliest_year))
        print("\nMost recent year of birth: " + str(most_recent_year))
        print("\nMost common year of birth: " + str(most_common_birth_year))
        df['Birth Year'].hist()
        plt.show()

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def display_data(df, index):
    total_rows = len(df.index)
    if index >= total_rows - 1:
        print("\nNo more raw data in database")
        return
    if index == 0:
        print_raw_data = input("\nDo you want to see raw data? Type yes or no.\n")
    else:
        print_raw_data = input("\nDo you want to see more raw data? Type yes or no.\n")
    if print_raw_data.lower() != 'yes':
        return
    new_index = index + 5
    if new_index >= total_rows:
        new_index = total_rows
    print(df.iloc[index:new_index])
    display_data(df, new_index)



def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)
        display_data(df, 0)

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
	main()
