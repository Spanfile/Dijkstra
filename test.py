from random import randint
from time import perf_counter
from multiprocessing import Process, JoinableQueue, current_process
from progressbar import ProgressBar
from dijkstra import Graph, dijkstra


def generate_random_graph(nodes, edges_per_node, max_weight):
    graph = Graph()

    for node_index in range(1, nodes + 1):
        for edge_index in range(edges_per_node):
            weight = randint(1, max_weight)
            neighbour = node_index
            while neighbour == node_index:
                neighbour = randint(0, nodes)
            graph.add_edge_with_cost(node_index, neighbour, weight)

    return graph


def test(queue, output):
    start = 1
    edges_per_node = 6
    max_weight = 100
    pid = current_process().pid

    while True:
        graph_size, graph_index = queue.get()
        if not graph_size:
            break
        end = graph_size

        #print("PID {}: Starting graph_size={}, graph_index={}".format(pid, graph_size, graph_index))
        #csv.write("Time,Steps,Length,Nodes\n")
        while True:
            graph = generate_random_graph(graph_size, edges_per_node, max_weight)
            try:
                start_time = perf_counter()
                moves, weights, steps = dijkstra(graph, start)
                end_time = perf_counter()
            except:
                continue

            elapsed = end_time - start_time

            path = []
            length = weights[end]
            current = end
            complete = False

            while current:
                path.append(current)
                if current == start:
                    complete = True
                    break
                current = moves[current]

            if not complete:
                continue

            row = "{},{},{},{},{},{}".format(graph_size, graph_index, elapsed, steps, length, len(path))
            #print("PID {}: {}".format(pid, row))
            output.put(row)
            #csv.write(row + "\n")
            break
        queue.task_done()

    print("PID {}: done".format(pid))


def writer(output):
    with open("results.csv", "w") as f, ProgressBar(max_value=5000) as bar:
        f.write("Graph size,Test index,Elapsed time,Steps,Path length,Path nodes\n")
        i = 0
        while True:
            row = output.get()
            if not row:
                break
            f.write(row + "\n")
            i += 1
            bar.update(i)
            output.task_done()


def main():
    queue = JoinableQueue()
    output = JoinableQueue()
    processes = [Process(target=test, args=(queue, output)) for index in range(8)]
    write_proc = Process(target=writer, args=(output,))

    for p in processes:
        p.start()
    write_proc.start()

    for size in range(100, 5100, 100):
        for index in range(0, 100):
            queue.put((size, index))

    queue.join()
    output.join()

    for i in range(100, 5000, 100):
        queue.put((None, None))
    output.put(None)

    for p in processes:
        p.join()

if __name__ == "__main__":
    main()
