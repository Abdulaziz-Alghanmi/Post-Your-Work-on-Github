import time
import pandas as pd
import numpy as np

# Dictionary to map city names to their respective data files
CITY_DATA = {
    'Chicago': 'chicago.csv',
    'New York City': 'new_york_city.csv',
    'Washington': 'washington.csv'
}


def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('\nHello! Let\'s explore some US bikeshare data!')

    # Get user input for city (case-insensitive)
    city = get_user_input("\nWhich city would you like to filter by? New York City, Chicago or Washington?\n",
                          ['new york city', 'chicago', 'washington'])

    # Get user input for month (case-insensitive)
    month = get_user_input(
        "\nWhich month would you like to filter by? January, February, March, April, May, June or type 'all' if you do not have any preference?\n",
        ['january', 'february', 'march', 'april', 'may', 'june', 'all'])

    # Get user input for day of the week (case-insensitive)
    day = get_user_input(
        "\nAre you looking for a particular day? If so, kindly enter the day as follows: Sunday, Monday, Tuesday, Wednesday, Thursday, Friday, Saturday or type 'all' if you do not have any preference.\n",
        ['sunday', 'monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'all'])

    print('-' * 40)
    # Return user inputs, converting them to title case
    return city.title(), month.title(), day.title()


def get_user_input(prompt, valid_inputs):
    """
    Gets user input and validates it against a list of valid inputs.

    Args:
        prompt (str): The prompt to display to the user.
        valid_inputs (list): A list of valid inputs.

    Returns:
        (str): The user's input if it is valid.
    """
    while True:
        # Convert user input to lowercase for case-insensitive comparison
        user_input = input(prompt).strip().lower()
        if user_input in valid_inputs:
            return user_input
        print("Sorry, I didn't catch that. Try again.")


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
    # function implementation
    # Load data file into a dataframe
    df = pd.read_csv(CITY_DATA[city])

    # Convert the Start Time column to datetime
    df['Start Time'] = pd.to_datetime(df['Start Time'])

    # Extract month and day of week from Start Time to create new columns
    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.day_name()

    # Filter by month if applicable
    if month != 'All':
        months = ['January', 'February', 'March', 'April', 'May', 'June']
        month = months.index(month.title()) + 1
        df = df[df['month'] == month]

    # Filter by day of week if applicable
    if day != 'All':
        df = df[df['day_of_week'] == day.title()]

    return df


def display_data(df):
    """Displays rows of data on user request."""
    start_loc = 0
    while True:
        view_data = input('Do you want to see 5 rows of data? Enter yes or no.\n').lower()
        if view_data == 'yes':
            print(df.iloc[start_loc:start_loc + 5])
            start_loc += 5
        else:
            break


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""
    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # Display the most common month
    popular_month = df['month'].mode()[0]
    print(f'Most Common Month: {popular_month}')

    # Display the most common day of week
    popular_day = df['day_of_week'].mode()[0]
    print(f'Most Common Day: {popular_day}')

    # Display the most common start hour
    df['hour'] = df['Start Time'].dt.hour
    popular_hour = df['hour'].mode()[0]
    print(f'Most Common Hour: {popular_hour}')

    print(f"\nThis took {time.time() - start_time} seconds.")
    print('-' * 40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""
    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # Display most commonly used start station
    start_station = df['Start Station'].mode()[0]
    print(f'Most Commonly Used Start Station: {start_station}')

    # Display most commonly used end station
    end_station = df['End Station'].mode()[0]
    print(f'Most Commonly Used End Station: {end_station}')

    # Display most frequent combination of start station and end station trip
    combination_station = df.groupby(['Start Station', 'End Station']).size().idxmax()
    print(f'Most Common Trip: {combination_station[0]} to {combination_station[1]}')

    print(f"\nThis took {time.time() - start_time} seconds.")
    print('-' * 40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""
    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # Display total travel time in days
    total_travel_time = df['Trip Duration'].sum()
    print(f'Total Travel Time: {total_travel_time / 86400:.2f} Days')

    # Display mean travel time in minutes
    mean_travel_time = df['Trip Duration'].mean()
    print(f'Mean Travel Time: {mean_travel_time / 60:.2f} Minutes')

    print(f"\nThis took {time.time() - start_time} seconds.")
    print('-' * 40)


def user_stats(df):
    """Displays statistics on bikeshare users."""
    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    user_types = df['User Type'].value_counts()
    print('User Types:\n', user_types)

    # Display counts of gender, if available
    try:
        gender_types = df['Gender'].value_counts()
        print('\nGender Types:\n', gender_types)
    except KeyError:
        print("\nGender Types:\nNo data available.")

    # Display earliest, most recent, and most common year of birth, if available
    try:
        earliest_year = int(df['Birth Year'].min())
        print('\nEarliest Year:', earliest_year)
    except KeyError:
        print("\nEarliest Year:\nNo data available.")

    try:
        most_recent_year = int(df['Birth Year'].max())
        print('\nMost Recent Year:', most_recent_year)
    except KeyError:
        print("\nMost Recent Year:\nNo data available.")

    try:
        most_common_year = int(df['Birth Year'].mode()[0])
        print('\nMost Common Year:', most_common_year)
    except KeyError:
        print("\nMost Common Year:\nNo data available.")

    print(f"\nThis took {time.time() - start_time} seconds.")
    print('-' * 40)


def main():
    while True:
        # Get user inputs for city, month, and day
        city, month, day = get_filters()

        # Load data based on user inputs
        df = load_data(city, month, day)

        # Display statistics
        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)

        # Ask user if they want to see raw data
        display_data(df)

        # Ask user if they want to restart the analysis
        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
    main()