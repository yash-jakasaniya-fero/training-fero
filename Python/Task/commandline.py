import argparse
import re
from collections import defaultdict

parser = argparse.ArgumentParser()
parser.add_argument('-c', type=int, help='Top "n" users who had made the highest requests.')
parser.add_argument('-user', help='User "x" how many requests they sent.', nargs='?')
# parser.add.argument('Help')
args = parser.parse_args()

def read_file():
    with open('tracking_log.txt', 'r') as file:
        return file.read()

def find_matches(content, pattern):
    return re.findall(pattern, content)

def count_matches(matches):
    match_counts = defaultdict(int)
    for match in matches:
        match_counts[match] += 1
    return match_counts

def get_top_matches(match_counts, top_n):
    sorted_client = sorted(match_counts.items(), key=lambda item: item[1], reverse=True)
    top_matches = defaultdict(int)
    for counter in range(min(top_n, len(sorted_client))):
        client, count = sorted_client[counter]
        top_matches[client] = count
    return top_matches

def get_client_name(match_count, client_name):
    return match_count.get(client_name, 0)

def main():
    content = read_file()
    pattern = r'from (.*) with'
    matches = find_matches(content, pattern)
    match_counts = count_matches(matches)


    try:
        if args.user is not None:
            if not args.user.strip():
                raise ValueError("You need to enter a user name after '-user'.")
            client_name = get_client_name(match_counts, args.user)
            print(f'{args.user} sent {client_name} request.')
        elif args.c is not None:
            if args.c <= 0:
                raise ValueError("You need to enter a positive integer after '-c'.")
            top_n = get_top_matches(match_counts, args.c)
            print(dict(top_n))
        else:
            raise ValueError("You need to provide either '-user' or '-c' with appropriate values.")
    except ValueError as e:
        print(f"Error: {e}")


if __name__ == '__main__':
    main()
