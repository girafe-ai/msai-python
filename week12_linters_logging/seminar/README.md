# Tagging System Scheme

```
                       Tagger server 1
                     /
Clients -> API Gate -> Tagger server 2
                     \
                       Tagger server 3
```

Clients send queries, they come to API Gate. API Gate route them to real executors, which are scalable.


## API Gate

Receives external queries, authorize them and route them to executors. In future, it can also save them into database.

API Gate execute mainly IO bound tasks (read request, proxy it to real executors, wait answer, return it to the client),
so we will use aiohttp framework to implement it using asyncio.

We should validate http request, send it to executors (if executor fails, we should repeat attempt several times),
then return response to client.


## Tagger servers

Executors that do tagging.

We'll use taggers.py from week04 as the base. They implement CPU-bound tasks.
Then we will use web framework to receive HTTP requests and handle them with Python code.
We also use threading and multiprocessing to increase throughput of single server.

### Tagger server using flask

The simplest way to create server that will serve our NLU algorithms - use Flask.
It has built-it instrument to turn on threading or multiprocessing.

### Tagger server using aiohttp

Another way is to separate requests handling which is IO-bound task from tagging which is CPU-bound tasks.
We can create asynchronous aiohttp view to receive tagging requests and run tagging in executor -
ThreadPoolExecutor or ProcessPoolExecutor. Waiting result from executor may be considered as IO-bound task,
because we wait result from other thread / process.


## Why aiohttp seems to work slower?

During seminar we did multiple calls to gate, gate distributed them to flask and aiohttp server randomly,
but in logs we saw, that flask server finishes its requests handling waay faster - responses from flask
come almost immediately, responses from our aiohttp servers come in several seconds.

I did some experiments after seminar, to check why its happening.

To understand that, firstly lets find out what our servers do to handle requests:

#### Flask server

Flask uses multiprocessing through Python's built-in socketserver library.
When new request come, flask run with `processes=4` param uses ForkingMixIn:
- parent process creates new child process via fork and leaves request handling
- child process handles request (call 3 taggers and collect results)
- child process sends response to client's connection and dies.

So flask creates new process for every connection but no more that 4 at the same time.

#### Aiohttp server

Aiohttp doesn't create processes by default. We did it by ourselves using ProcessPoolExecutor.

Important moment, that we decided to run every tagger separately in different workers.

When new request come:
- aiohttp creates new coroutine (our view)
- loop runs our view
- our view sends 3 tasks to ProcessPoolExecutor via `loop.run_in_executor` and receives 3 awaitable futures
- (now loop has several tasks to handle other requests and task to run executor's code - it doesn't happen in background, loop has to run executor's functions between other coroutines)
- our view uses `gather` to create new coroutine to wait while executor handles taggers and await it
- loop receives execution control and runs next task - requests comes very fast, so next task would probably be our view for next request
- ... etc
- at some point in time loop receives execution control and runs executor's function to run first task in worker
- workers aren't create so executor creates new process and send task to that process
- loop receives execution control and can continue views if futures are computed or continue to run executor's calls
- executor will run new tasks, creates new worker processes, sets results of completed futures
- ...
- at some point in time 3 futures of 1 view became completed, loop continues our view
- our view glue results from different taggers and send it to client's connection
- loop receives execution control and continue run tasks.

ProcessPoolExecutor creates only 4 processes and reuse them for new tasks.
It uses shared memory to send the task to separate process and receive result from separate process.

----

So, to understand where is the problem, let's do 2 experiments:

#### Experiment 1 - make really long CPU-bound tasks

Our CPU-bound tasks actually work very fast.
Transferring data between processes can take more time than single tagger execution.
Let's add `sleep(1)` to every `tagger.get_tags()` function.

That experiment shows that with long-term tasks there are no difference between our servers.

If loop has enough time until futures became computed, it manages to execute all tasks in time - finish views and run executor's functions.


#### Experiment 2 - make single process for all tagger in aiohttp

As we understood, we have 3 quite fast tasks that we run in 3 different processes with only 4 workers.

If tasks would be really slow, than yes - we can handle single process faster.
But with the same number of workers it doesn't affect throughput - time of N requests computation will be the same.

Let's create tagging job that run our taggers one by one in single process (check tagger_aiohttp_2.py).

Now, even without `sleep(1)` in taggers, aiohttp server works as fast as flask server.

That experiment again shows that the problem is connected with tasks launch in executor.


### Conclusion

We created the situation, where tasks in executor finish so fast,
that loop in main process has to return to view coroutines before it handles to run new tasks in executor.

Because of that workers idle some amount of time. And total execution time of N requests in aiohttp increases.

In real world we probably won't find same behaviour - client's requests are distributed in time, but we sent them simultaneously.
That wasn't proper load testing. But that was kind of stress testing that help us to find a problem.

Now we have 6 versions of tagger server:
- threaded and processed flask
- threaded and processed aiohttp with 3 workers for request
- threaded and processed aiohttp with 1 worker for request.
