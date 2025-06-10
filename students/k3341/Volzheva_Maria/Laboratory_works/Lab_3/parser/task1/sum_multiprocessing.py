import time
import multiprocessing


def calculate_sum(start, end, result):
    result.append(sum(range(start, end)))


def main():
    num_processes = 4
    chunks = 100_000_000 // num_processes
    start_time = time.time()
    process = []
    manager = multiprocessing.Manager()
    result = manager.list()
    for i in range(num_processes):
        start = i * chunks + 1
        end = (i+1) * chunks + 1
        p = multiprocessing.Process(target=calculate_sum, args=(start, end, result))
        process.append(p)
        p.start()
    for p in process:
        p.join()
    total_sum = sum(result)
    print("Total sum: {}".format(total_sum))
    end_time = time.time()
    print(f"Execution time: {end_time - start_time} seconds")


if __name__ == "__main__":
    main()

#Total sum: 5000000050000000
#Execution time: 0.42986202239990234 seconds