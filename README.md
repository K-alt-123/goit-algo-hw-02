# Queues and deques

Requires Python 3.12 or newer; no third-party dependencies.

```powershell
python solution.py --help
python solution.py service --cycles 5
python solution.py service
python solution.py palindrome "Race car"
python -m unittest discover -s tests -v
```

The service uses `queue.Queue`: new requests join the back and processing removes the oldest request. IDs are unique within one process. Interactive mode generates and processes one request per Enter; `q` or end-of-input exits. The finite mode is useful for demonstrations. An empty queue returns `None` from `process_request()` and is reported by the interface.

The palindrome function case-folds the text, removes whitespace, and puts its characters in a `deque`. It compares and removes the two ends until they meet. Punctuation remains significant: `aba!` is not a palindrome. Empty and single-character strings are palindromes.

Queue insertion/removal and deque end operations take O(1) time. Checking a palindrome takes O(n) time and O(n) additional memory for the normalized characters.
