## Commandline Task

**1. read_file()**

- Reads the log file (tracking_log.txt).
- Returns a list of log entries, each containing a timestamp and a username.


**2. get_top_n_users(n, total)**
- Extracts and counts the number of requests per user.
- Identifies the top n most active users.
- Returns a list of request data and a set of top users.


**3. group_by_time_block(data, top_users, gap)**
- Divides log entries into time blocks based on the given duration (gap).
- Counts requests for top users within each time block.
- Returns a dictionary of grouped request counts.


**4. plot_data(intervals)**
- Takes grouped request data (intervals) and prepares a bar chart.
- Displays the number of requests per user across time blocks.


**5. track_user_requests(user, gap, total)**
- Filters request data for a specific user.
- Groups the user’s requests into time blocks.
- Displays the data and generates a bar chart if needed.


**6. total_requests_for_user(user, total)**
- Counts the total number of requests made by a specific user.
- Returns the total request count.


**7. main()**
- Parses command-line arguments (-c, -u, -t, -g).
- Calls appropriate functions based on user input.
- Displays results and generates charts when required.