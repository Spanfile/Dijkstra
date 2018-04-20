import csv
from glob import glob


def main():
    with open("aggregated.csv", "w") as aggregated_file:
        writer = csv.writer(aggregated_file)
        writer.writerow(["Graph size", "Average time", "Average steps", "Average length", "Average nodes", "Average length per node"])

        for filename in glob("*.csv"):
            if filename == "aggregated.csv":
                continue

            with open(filename, "r") as csv_file:
                graph_size = filename.split(".")[0]

                reader = csv.DictReader(csv_file)

                times = []
                steps = []
                lengths = []
                nodes = []

                for row in reader:
                    times.append(float(row["Time"]))
                    steps.append(int(row["Steps"]))
                    lengths.append(int(row["Length"]))
                    nodes.append(int(row["Nodes"]))

                avg_time = sum(times) / len(times)
                avg_steps = sum(steps) / len(steps)
                avg_length = sum(lengths) / len(lengths)
                avg_nodes = sum(nodes) / len(nodes)
                length_per_node = avg_length / avg_nodes

                writer.writerow([graph_size, avg_time, avg_steps, avg_length, avg_nodes, length_per_node])


if __name__ == "__main__":
    main()
