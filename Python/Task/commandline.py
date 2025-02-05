from collections import defaultdict
from datetime import timedelta, timedelta
from collections import Counter
import re
import argparse
import datetime
import numpy as np
import matplotlib.pyplot as plt

parser = argparse.ArgumentParser()
parser.add_argument('-c', type=int, help='Top "n" users who had made the highest requests.')
parser.add_argument('-user', help='User "x" how many requests they sent.')
# parser.add_argument('-h', type=int, help='Enter Hour value for time_block')
# parser.add.argument('Help')
args = parser.parse_args()

def read_file():
    with open('tracking_log.txt', 'r') as file:
        return file.read()


def count_matches(matches):
    match_counts = defaultdict(int)
    for match in matches:
        match_counts[match] += 1
    return match_counts

def get_top_n_users(match_counts, top_n):
    sorted_client = sorted(match_counts.items(), key=lambda item: item[1], reverse=True)
    top_matches = defaultdict(int)
    for counter in range(min(top_n, len(sorted_client))):
        client, count = sorted_client[counter]
        top_matches[client] = count
    return top_matches

def find_user(content, pattern):
    return re.findall(pattern, content)

def get_client_name(match_count, client_name):
    return match_count.get(client_name, 0)


def datetimearg():
    t1_s = read_file.split("\n")[0].split(",")[0].strip('[')
    t2_e = read_file.split("\n")[-2].split(",")[0].strip('[')

    t1 = datetime.datetime.strptime(t1_s, "%Y-%m-%d %H:%M:%S")
    t2 = datetime.datetime.strptime(t2_e, "%Y-%m-%d %H:%M:%S")

    print("Start time:", t1)
    print("end time:", t2)

    time_block = timedelta(hours=int(input("Enter the time block in hours: ")))

    while t1<t2:
        window_end=min(t1+time_block, t2)
        print(t1, " to ", window_end)
        t1 += time_block

############################################################
# def read_file():
#     with open('tracking_log.txt', 'r') as file:
#         return file.readlines()
 
# user = input("Enter the user name:")
# gap=timedelta(hours= int(input("Enter the hours")))
# data = []
# content = read_file()

# for entry in content:
#     parts = entry.split('] INFO Tracking Request from ')
#     if len(parts) == 2:
#         timestamp_str = parts[0][1:]
#         timestamp_obj = datetime.strptime(timestamp_str, "%Y-%m-%d %H:%M:%S,%f")
#         name = parts[1].split(' ')[0]
#         data.append({"timestamp": timestamp_obj, "name": name})
#         intervals = {}
        
# first_time_stamp = data[0]["timestamp"]
# last_time_stamp = data[-1]["timestamp"]
 
# while first_time_stamp<last_time_stamp:
#     window_end = min(first_time_stamp+gap, last_time_stamp)
#     first_time_stamp += gap
#     intervals[f"{first_time_stamp} to {window_end}"] = 0
 
# for object in data:
#     for key in intervals.keys():
#         end_stamp = key.split(" to ")[1]
#         end_datetime_object = datetime.strptime(end_stamp, "%Y-%m-%d %H:%M:%S.%f")
#         if object["name"] == user and object["timestamp"]<end_datetime_object:
#             intervals[key] = intervals[key] + 1
#             break
 
# x_axis_data = []
# y_axis_data = []


# for i in intervals.keys():
#     x_axis_data.append(i)
#     y_axis_data.append(intervals[i])
 
# print("x values", x_axis_data)
# print("y values", y_axis_data)

# import matplotlib.pyplot as plt
 
# fig, ax = plt.subplots()
 
# intervals = x_axis_data
# values = y_axis_data
 
# ax.bar(intervals, values, label=x_axis_data)
 
# ax.set_ylabel('Requests')
# ax.set_title('Time windows')

#############################################################

def main():
    file = read_file()
    pattern = r'from (.*) with'
    matches = find_user(file, pattern)
    match_counts = count_matches(matches)


    try:
        if args.user is not None:
            if not args.user.strip():
                raise ValueError("You need to enter a user name after '-user'.")
            client_name = get_client_name(match_counts, args.user)
            print(f'{args.user} sent {client_name} request.')

        elif args.c is not None:
            if args.c <= 0:
                raise ValueError("You need to enter a positive int value after '-c'.")
            top_n = get_top_n_users(match_counts, args.c)
            print(dict(top_n))

        
        else:
            raise ValueError("You need to provide either '-user' or '-c' with appropriate values.")
    except ValueError as e:
        print(f"Error: {e}")


 
    # plt.bar(time_periods, request_counts)
    # plt.xlabel("Time Block")
    # plt.ylabel("Request Count")
    # plt.title(f"Tracking Requests for User {-args.user} by Time Block")
    # plt.show()


    # user = list(client_name.key())
    # request = list(client_name.values())
    # plt.bar( request, color='red')
    # plt.xlabel('user')
    # plt.ylabel('request')
    # plt.show()

 
    user = list(top_n.keys())
    request = list(top_n.values())
    plt.bar(user, request, color='grey')
    plt.xlabel('user name')
    plt.ylabel('no of request')
    plt.title('Top Most Request user')
    plt.show()


if __name__ == '__main__':
    main()