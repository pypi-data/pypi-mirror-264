from time import perf_counter
from os import get_terminal_size, system, name

def ft_tqdm(lst: range):
    width = get_terminal_size().columns
    coeff = (width - 46)/width
    range_end = lst[-1] + 1
    start_time = perf_counter() * 10**6 
    yield
    for n in lst:
        elapsed_time = start_time - perf_counter()
        frequency = (n / elapsed_time) * 10**6
        eta = (range_end - n - 1) / frequency if frequency else 0
        completion_proportion = ((n+1)*100) // range_end
        completion_length = int(width * coeff * completion_proportion / 100)
        progress_bar = f"{str(completion_proportion)}%|{'█' * (completion_length)}{' ' * (int(width*coeff) - completion_length)}| {str(n+1)} / {str(range_end)} [eta: {eta:.1f}s, {frequency:.2f}it/s]"
        if n>1:
            system('cls' if name == 'nt' else 'clear')
            print(progress_bar, end="\r")
        start_time = perf_counter() * 10**6 
        yield
