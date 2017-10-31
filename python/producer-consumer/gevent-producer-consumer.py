# External Requirement: gevent
# Use-case: Multiple producer-consumers distributed over a grid of processes to
# perform a task on a large data-set in a non I/O blocking manner.
# NUM_CORES could be seen as horizontal scaling while within each core,
# greenlets(gevent) producer-consumers operate in non-I/O blocking manner
# eg: The following code downloads the page content of HackerNews(https://news.ycombinator.com/item?id=XXX)
# where item-ids are between 0-10000
import requests
import traceback

import gevent
import multiprocessing

from gevent import monkey
from gevent.queue import JoinableQueue


def spawn_processes(num_items=100, batch_size=10):
    """
    Distribute the sample num_items IDs into 4 processes, processing a batch of batch_size in a single process (fairly large)
    """
    NUM_CORES = 4
    pool = multiprocessing.Pool(NUM_CORES)

    map_data = []
    for i in range(num_items/batch_size):
        map_data.append({"start_id": i * batch_size, "batch_size": batch_size})

    pool.imap(processor, map_data) # imap for random execution i.e. pick any batch first
    pool.close()
    pool.join()
    pool.terminate()


def processor(data):
    """
    Each launched process(=NUM_CORES) executes 1 item in the list map_data as data.
    For given start_id and batch_size, launches gevent consumers to scrape data for the given ID
    Also, the main thread acts as a producer to produce the data for the workers to use 
    """
    try:
        NUM_GREENLETS = 8 # Depending on how much I/O block is expected. Varies for each problem.
        process_id = multiprocessing.current_process()
        monkey.patch_all() # Patch all the libraries to support non-IO blocking

        start_id = data["start_id"]
        batch_size = data["batch_size"]

        joinable_queue = JoinableQueue()

        # Launch NUM_GREENLETS workers
        for i in range(NUM_GREENLETS):
            gevent.spawn(worker, joinable_queue=joinable_queue, greenlet_id=i, process_id=process_id)

        # Producer
        for id in range(start_id, start_id + batch_size):
            joinable_queue.put(id)

        joinable_queue.join()

    except:
        # If the processes have any uncaptured error, it'd not redirect to stderr,
        # as it's a different Pipe for each process fork spawned
        print(traceback.format_exc())



def worker(joinable_queue, greenlet_id, process_id):
    """
    Consumer instance which is nonIO blocking
    Gets each individual ID at a time and processes it till the queue is either empty or the wait times out
    """
    while True:
        try:
            id_to_process = joinable_queue.get(timeout=2) # Wait 2 seconds to see if an item comes in a queue, else raise Queue.Empty
            print("Process %s,'s Greenlet %d, processing Id=%d" %(process_id, greenlet_id, id_to_process))
            response = requests.get("https://hacker-news.firebaseio.com/v0/item/" + str(id_to_process) + ".json?print=pretty")
            joinable_queue.task_done()
        except gevent.queue.Empty:
            break
        except:
            print(traceback.format_exc())

spawn_processes()