import time
import numpy as np
import pandas as pd


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

    # get user input for city (cities from CITY_DATA). Return it in lowercase and without spaces.
    possible_cities = []
    for city in CITY_DATA:
        possible_cities.append(city.lower())
    possible_cities_str = ", ".join(possible_cities)
    wrong_input = True
    city = ''
    while wrong_input:
        try:
            city = str(input("\nPlease select a city or 'all'. Possible cities are: "+possible_cities_str.title()+"\n"))
            possible_cities.append('all')
            wrong_input = city.lower().rstrip() not in possible_cities
        except Exception as e:
            print("Exception occurred: {}".format(e))
    city = city.lower().rstrip().replace(' ','_')
    wrong_input = True

    # get user input for month (all, january, february, ... , december). Return it in lowercase.
    possible_months = ['all','january','february','march','april','mai','june','july','august','september','october','november','december']
    month = ''
    while wrong_input:
        try:
            month = str(input("\nPlease select a month or enter 'all' to not filter by month.\n"))
            wrong_input = month.lower().rstrip() not in possible_months
        except Exception as e:
            print("Exception occurred: {}".format(e))
    month = month.lower().rstrip()
    wrong_input = True

    # get user input for day of week (all, monday, tuesday, ... sunday). Return it in lowercase.
    possible_days = ['all','monday','tuesday','wednesday','thursday','friday','saturday','sunday']
    day = ''
    while wrong_input:
        try:
            day = str(input("\nPlease select a weekday or enter 'all' to not filter by weekdays.\n"))
            wrong_input = day.lower().rstrip() not in possible_days
        except Exception as e:
            print("Exception occurred: {}".format(e))
    day = day.lower().rstrip()

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
    # Get data from necessary files. Distinguish between all files or a single file.
    df = pd.DataFrame()
    if(city=='all'):
        for place in CITY_DATA:
            place = place.replace(" ","_")
            f = open(place+'.csv')
            df_single = pd.read_csv(f)
            df = pd.concat([df,df_single],sort=False)
            f.close()
    else:
        f = open(city+'.csv')
        df = pd.read_csv(f)
        f.close()

    df['Start Time'] = pd.to_datetime(df['Start Time'])

    #Filter by month if necessary.
    if month!='all':
        months = ['january','february','march','april','mai','june','july','august','september','october','november','december']
        df = df[df['Start Time'].dt.month==months.index(month)+1]

    #Filter by weekday if necessary.
    if day!='all':
        days = ['monday','tuesday','wednesday','thursday','friday','saturday','sunday']
        df = df[df['Start Time'].dt.day==days.index(day)+1]

    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    try:
        # Display the most common month and it amount.
        most_common_month_name = df['Start Time'].dt.month.mode()[0]
        months = ['january','february','march','april','mai','june','july','august','september','october','november','december']
        most_common_month_name = months[most_common_month_name-1].title()
        most_common_month_count = str(df['Start Time'].dt.month.value_counts().max())
        print("The most frequent month of the trips is "+most_common_month_name+" with "+most_common_month_count+" performed trips.")

        # Display the most common day of week and it amount.
        most_common_day_name = df['Start Time'].dt.day.mode()[0]%7
        days = ['sunday','monday','tuesday','wednesday','thursday','friday','saturday']
        most_common_day_name = days[most_common_day_name].title()
        most_common_day_count = str(df['Start Time'].dt.day.value_counts().max())
        print("The most common day of the week for trips is "+most_common_day_name+" with "+most_common_day_count+" trips made.")

        # Display the most common start hour and it amount.
        most_common_hour_name = str(df['Start Time'].dt.hour.mode()[0])
        most_common_hour_count = str(df['Start Time'].dt.hour.value_counts().max())
        print("The most common starting hour of the trips is "+most_common_hour_name+" with "+most_common_hour_count+" trips performed.")
    # If there is not enough data to determine the statistics.
    except KeyError:
        print("For the specified filter there is not enough data available to evaluate the time data")

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    try:
        # Display most commonly used start station and it amount.
        most_common_start_station_name = df['Start Station'].mode()[0]
        most_common_start_station_count = str(df['Start Station'].value_counts().max())
        print("The most frequent station to start is '"+most_common_start_station_name+"' with "+most_common_start_station_count+" started trips.")

        # Display most commonly used end station and it amount.
        most_common_end_station_name = df['End Station'].mode()[0]
        most_common_end_station_count = str(df['End Station'].value_counts().max())
        print("The most frequent station to the end is '"+most_common_end_station_name+"' with "+most_common_end_station_count+" trips completed.")

        # Display most frequent combination of start station and end station trip and it amount.
        df['Start To End Station'] = df['Start Station']+" to "+df['End Station']
        most_common_combination_name = df['Start To End Station'].mode()[0]
        most_common_combination_count = str(df['Start To End Station'].value_counts().max())
        print("The most frequent combination of start and end station is "+most_common_combination_name+" with "+most_common_combination_count+" cases.")
    # If there is not enough data to determine the statistics.
    except KeyError:
        print("There is not enough data available for the specified filter to evaluate the station data.")

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    try:
        # Display total travel time.
        total_travel_time = str(df['Trip Duration'].sum())
        print("The total trip duration is "+total_travel_time+".")

        # Display mean travel time.
        mean_travel_time = str(df['Trip Duration'].mean())
        if mean_travel_time == 'nan':
            mean_travel_time = "0"
        print("The average trip duration is "+mean_travel_time+".")
    # If there is not enough data to determine the statistics.
    except KeyError:
        print("There is not enough data available for the specified filter to evaluate the trip data.")

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    try:
        # Display counts of user types.
        print(df.groupby(['User Type'])['User Type'].count())
        print("\n")

        # Display counts of gender.
        print(df.groupby(['Gender'])['Gender'].count())
        print("\n")

        # Display earliest, most recent, and most common year of birth and it amount.
        earliest_birth_year = str(df['Birth Year'].min())
        latest_birth_year = str(df['Birth Year'].max())
        most_comman_birth_year_name = str(df['Birth Year'].mode()[0])
        most_comman_birth_year_count = str(df['Birth Year'].value_counts().max())
        print("The earliest year of birth is "+earliest_birth_year+" and the latest is "+latest_birth_year+".")
        print("The most frequent birth year is "+most_comman_birth_year_name+"with "+most_comman_birth_year_count+" cases.")
    # If there is not enough data to determine the statistics.
    except KeyError:
        print("For the specified filter there is not enough data available to evaluate the user data.")

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def main():
    while True:
        # Load data.
        city, month, day = get_filters()
        df = load_data(city, month, day)

        # Print statistics if possible.
        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)

        # Show raw data if possible.
        new_data = True
        row = 0
        while new_data:
            if df[row:row+6].empty:
                new_data = False
                print("\nNo Data can be shown.")
            else:
                try:
                    see_data = str(input("\nWould you like to view individual trip data? Type 'yes' or 'no'.\n"))
                    if see_data.lower().rstrip() == "no":
                        new_data = False
                    elif see_data.lower().rstrip() == "yes":
                        print(df.iloc[row:row+6,:])
                        row = row+5
                except Exception as e:
                    print("Exception occurred: {}".format(e))
        print('-'*40)
        new_data = True

        # Ssk for restart.
        print("\nThe last filter was city: {}, month:{}, weekday:{}.".format(city,month,day))
        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower().rstrip() != 'yes':
            break

if __name__ == "__main__":
	main()