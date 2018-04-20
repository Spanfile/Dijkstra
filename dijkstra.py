#!/usr/bin/env python3

from heapq import *
from collections import defaultdict
from typing import Dict, Tuple, Any


class Graph():
    def __init__(self):
        self.vertices = set()
        self.edges = defaultdict(list)
        self.weights = {}


    def add_edge_with_cost(self, src, dest, weight) -> None:
        if src not in self.vertices:
            self.vertices.add(src)

        if dest not in self.vertices:
            self.vertices.add(dest)

        self.edges[src].append(dest)
        self.edges[dest].append(src)
        self.weights[(src, dest)] = weight
        self.weights[(dest, src)] = weight


class MinPriorityQueue():
    def __init__(self):
        self._queue = []
        self._queue_entry_dict = {}
        self._removed = -1

    
    def add_with_priority(self, item, priority):
        if item in self._queue_entry_dict:
            self._remove(item)
        queue_entry = [priority, item]
        self._queue_entry_dict[item] = queue_entry
        heappush(self._queue, queue_entry)


    def pop(self):
        while self._queue:
            priority, item = heappop(self._queue)
            if item is not self._removed:
                del self._queue_entry_dict[item]
                return item
        raise Exception()


    def _remove(self, item):
        queue_entry = self._queue_entry_dict.pop(item)
        queue_entry[1] = self._removed


    def __bool__(self):
        return bool(self._queue)


def dijkstra(graph, start, end = None):
    move_weights = {start: 0}
    moves = {}
    move_queue = MinPriorityQueue()

    for vertex in graph.vertices:
        if vertex != start:
            move_weights[vertex] = float("inf")
            moves[vertex] = None
        move_queue.add_with_priority(vertex, move_weights[vertex])

    steps = 0
    while move_queue:
        min_vertex = move_queue.pop()
        steps += 1
        if end and min_vertex == end:
            break
        for neighbour in graph.edges[min_vertex]:
            move_weight = move_weights[min_vertex] + graph.weights[min_vertex, neighbour]
            if move_weight < move_weights[neighbour]:
                move_weights[neighbour] = move_weight
                moves[neighbour] = min_vertex
                move_queue.add_with_priority(min_vertex, move_weight)
                print("{} -> {}: {}".format(min_vertex, neighbour, move_weight))

    return moves, move_weights, steps


def main():
    graph = Graph()

    graph.add_edge_with_cost("A", "B", 4)
    graph.add_edge_with_cost("A", "C", 9)
    graph.add_edge_with_cost("B", "C", 3)
    graph.add_edge_with_cost("B", "D", 5)
    graph.add_edge_with_cost("C", "E", 6)
    graph.add_edge_with_cost("D", "E", 7)

    start = "A"
    end = "E"

    dijkstra_moves, weights, steps = dijkstra(graph, start)
    path = []
    current = end

    while current:
        path.append(current)
        if current == start:
            break
        current = dijkstra_moves[current]

    print("Steps: {}. Path length: {}".format(steps, weights[end]))
    print(" -> ".join(reversed(path)))


if __name__ == "__main__":
    main()
