import argparse
from datetime import datetime, timedelta
from collections import Counter
import matplotlib.pyplot as plt
import numpy as np


def read_file():
    with open('tracking_log.txt', 'r') as file:
        return file.readlines()


def get_top_n_users(n, total):
    user_request_total = Counter()
    data = []

    for requests in total:
        client = requests.split('] INFO Tracking Request from ')
        if len(client) == 2:
            timestamp_str = client[0][1:]
            timestamp_obj = datetime.strptime(timestamp_str, "%Y-%m-%d %H:%M:%S,%f")
            name = client[1].split(' ')[0]
            user_request_total[name] += 1
            data.append({"timestamp": timestamp_obj, "name": name})

    top_n_users = user_request_total.most_common(n)
    top_users = set(user for user, _ in top_n_users)
    return data, top_users


def group_by_time_block(data, top_users, gap):
    intervals = {}
    first_time_stamp = data[0]["timestamp"]
    last_time_stamp = data[-1]["timestamp"]

    while first_time_stamp < last_time_stamp:
        window_end = min(first_time_stamp + gap, last_time_stamp)
        intervals[f"{first_time_stamp} to {window_end}"] = {user: 0 for user in top_users}
        first_time_stamp += gap

    for entry in data:
        if entry["name"] in top_users:
            for key in intervals.keys():
                end_stamp = key.split(" to ")[1]
                end_datetime_object = datetime.strptime(end_stamp, "%Y-%m-%d %H:%M:%S.%f")
                if entry["timestamp"] < end_datetime_object:
                    intervals[key][entry["name"]] += 1
                    break

    return intervals


def plot_data(intervals):
    x_axis_data = [f"{start.split(' to ')[0]}" for start in intervals.keys()]
    y_axis_data = {user: [] for user in next(iter(intervals.values())).keys()}

    for window, user_counts in intervals.items():
        for user, count in user_counts.items():
            y_axis_data[user].append(count)

    x_indices = np.arange(len(x_axis_data))
    bar_width = 0.15

    fig, ax = plt.subplots()

    for i, (user, counts) in enumerate(y_axis_data.items()):
        ax.bar(x_indices + (i * bar_width), counts, bar_width, label=user)

    ax.set_xticklabels(x_axis_data)
    ax.set_xlabel('Time block')
    ax.set_ylabel('Requests')
    ax.set_title('Requests for Top Users')
    ax.legend()
    plt.tight_layout()
    plt.show()


def track_user_requests(user, gap, total):
    data = []
    intervals = {}
    for requests in total:
        users = requests.split('] INFO Tracking Request from ')
        if len(users) == 2:
            timestamp_str = users[0][1:]
            timestamp_obj = datetime.strptime(timestamp_str, "%Y-%m-%d %H:%M:%S,%f")
            name = users[1].split(' ')[0]
            data.append({"timestamp": timestamp_obj, "name": name})

    first_time_stamp = data[0]["timestamp"]
    last_time_stamp = data[-1]["timestamp"]

    while first_time_stamp < last_time_stamp:
        window_end = min(first_time_stamp + gap, last_time_stamp)
        first_time_stamp += gap
        intervals[f"{first_time_stamp} to {window_end}"] = 0

    for object in data:
        for key in intervals.keys():
            end_stamp = key.split(" to ")[1]
            end_datetime_object = datetime.strptime(end_stamp, "%Y-%m-%d %H:%M:%S.%f")
            if object["name"] == user and object["timestamp"] < end_datetime_object:
                intervals[key] += 1
                break

    x_axis_data = []
    y_axis_data = []

    for i in intervals.keys():
        x_axis_data.append(i)
        y_axis_data.append(intervals[i])

    print(f"\nRequests by {user}:")

    print("x values", x_axis_data)
    print("y values", y_axis_data)

    fig, ax = plt.subplots()

    ax.bar(x_axis_data, y_axis_data, label=user)

    ax.set_ylabel('Requests')
    ax.set_title(f'Requests for {user} in Time Windows')
    plt.tight_layout()
    plt.show()


def total_requests_for_user(user, total):
    request_count = 0
    for requests in total:
        client = requests.split('] INFO Tracking Request from ')
        if len(client) == 2:
            name = client[1].split(' ')[0]
            if name == user:
                request_count += 1
    return request_count


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-user', help='Specify a user to track')
    parser.add_argument('-u', help='Total request of a particular user')
    parser.add_argument('-c', type=int, help='Number of top users to find')
    parser.add_argument('-t', type=int, help='Time block duration in hours')
    parser.add_argument('-g', action='store_true', help='Generate group chart for time blocks')
    args = parser.parse_args()

    try:
        if args.c:
            if not isinstance(args.c, int) or args.c <= 0:
                raise ValueError("The number of top users (-c) must be a positive integer.")
            content = read_file()
            data, top_users = get_top_n_users(args.c, content)

            if args.t:
                if not isinstance(args.t, int) or args.t <= 0:
                    raise ValueError("Time block duration (-t) must be a positive integer.")
                gap = timedelta(hours=args.t)
                intervals = group_by_time_block(data, top_users, gap)
                print(f"Top {args.c} users with time block duration of {args.t} hours:")
                for window, user_counts in intervals.items():
                    print(f"\n{window}:")
                    for user, count in user_counts.items():
                        print(f"{user}: {count} requests")

                if args.g:
                    plot_data(intervals)

            else:
                print(f"Top {args.c} users by request count:")
                for user, count in data:
                    print(f"{user}: {count} requests")

        elif args.user:
            if not args.user.strip():
                raise ValueError("You need to enter a user name after '-user'.")
            user = args.user
            content = read_file()
            gap = timedelta(hours=args.t) if args.t else timedelta(hours=1)
            track_user_requests(user, gap, content)

        elif args.u:
            if not args.u.strip():
                raise ValueError("You need to specify a valid user for '-u'.")
            user = args.u
            content = read_file()
            total_requests = total_requests_for_user(user, content)
            if total_requests == 0:
                print(f"{user} has no requests in the log.")
            else:
                print(f"{user} has made {total_requests} requests in total.")

        else:
            raise ValueError("Please specify the number of top users with '-c <n>'")

    except ValueError as ve:
        print(f"Error: {ve}")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")


if __name__ == "__main__":
    main()