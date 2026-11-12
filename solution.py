"""FIFO request processing and a deque-based palindrome check."""
import argparse
from collections import deque
from dataclasses import dataclass
from itertools import count
from queue import Empty, Queue


@dataclass(frozen=True)
class Request:
    id: int


_request_ids = count(1)


def generate_request(requests: Queue) -> Request:
    request = Request(next(_request_ids))
    requests.put(request)
    return request


def process_request(requests: Queue) -> Request | None:
    try:
        request = requests.get_nowait()
    except Empty:
        return None
    requests.task_done()
    return request


def is_palindrome(text: str) -> bool:
    letters = deque(char for char in text.casefold() if not char.isspace())
    while len(letters) > 1:
        if letters.popleft() != letters.pop():
            return False
    return True


def service(cycles: int | None) -> None:
    requests = Queue()
    cycle = 0
    while cycles is None or cycle < cycles:
        if cycles is None:
            try:
                action = input('Enter to generate/process a request; q to exit: ')
            except EOFError:
                break
            if action.strip().lower() == 'q':
                break
        created = generate_request(requests)
        print(f'Generated request {created.id}')
        processed = process_request(requests)
        print(f'Processed request {processed.id}' if processed else 'Queue is empty.')
        cycle += 1
    if requests.empty():
        print('Queue is empty.')


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    commands = parser.add_subparsers(dest='command', required=True)
    queue_parser = commands.add_parser('service', help='Run the request simulator')
    queue_parser.add_argument('--cycles', type=int, help='Run this many cycles and exit')
    palindrome_parser = commands.add_parser('palindrome', help='Check a string')
    palindrome_parser.add_argument('text')
    args = parser.parse_args()
    if args.command == 'service':
        if args.cycles is not None and args.cycles < 0:
            parser.error('--cycles must be nonnegative')
        service(args.cycles)
    else:
        print('Palindrome' if is_palindrome(args.text) else 'Not a palindrome')


if __name__ == '__main__':
    main()
