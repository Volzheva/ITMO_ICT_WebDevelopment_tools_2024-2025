import time
import threading


def calculate_sum(start, end, result):
    result.append(sum(range(start, end)))


def main():
    num_threads = 4
    chunks = 100_000_000 // num_threads
    start_time = time.time()
    threads = []
    result = []
    for i in range(num_threads):
        start = i * chunks + 1
        end = (i+1) * chunks + 1
        t = threading.Thread(target=calculate_sum, args=(start, end, result))
        threads.append(t)
        t.start()
    for t in threads:
        t.join()
    total_sum = sum(result)
    print("Total sum: {}".format(total_sum))
    end_time = time.time()
    print(f"Execution time: {end_time-start_time} seconds")

if __name__ == "__main__":
    main()


#Total sum: 5000000050000000
#Execution time: 0.9064211845397949 seconds