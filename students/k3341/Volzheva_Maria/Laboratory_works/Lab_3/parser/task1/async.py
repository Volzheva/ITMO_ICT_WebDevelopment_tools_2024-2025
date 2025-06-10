import time
import asyncio

async def calculate_sum(start, end):
    return sum(range(start, end))


async def main():
    num_tasks = 4
    chunks = 100_000_000 // num_tasks
    start_time = time.time()
    tasks = []
    for i in range(num_tasks):
        start = i * chunks + 1
        end = (i+1) * chunks + 1
        tasks.append(asyncio.create_task(calculate_sum(start, end)))
    results = await asyncio.gather(*tasks)
    total_sum = sum(results)
    print("Async sum:", total_sum)
    end_time = time.time()
    print(f"Execution time: {end_time - start_time} seconds")

if __name__ == "__main__":
    asyncio.run(main())



#Async sum: 5000000050000000
#Execution time: 0.7945249080657959 seconds