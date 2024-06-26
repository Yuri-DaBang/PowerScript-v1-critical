import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation

# Constants
NUM_CITIES = 69
NUM_ANTS = int(69/3)
NUM_ITERATIONS = 100
ALPHA = 1.0  # Pheromone importance
BETA = 5.0   # Distance importance
EVAPORATION_RATE = 0.52
Q = 100  # Pheromone constant

# Generate random cities
np.random.seed(42)
cities = np.random.rand(NUM_CITIES, 2)

# Calculate the distance matrix
def calculate_distance_matrix(cities):
    num_cities = len(cities)
    distance_matrix = np.zeros((num_cities, num_cities))
    for i in range(num_cities):
        for j in range(num_cities):
            if i != j:
                distance_matrix[i][j] = np.linalg.norm(cities[i] - cities[j])
    return distance_matrix

distance_matrix = calculate_distance_matrix(cities)

# Initialize pheromones
pheromones = np.ones((NUM_CITIES, NUM_CITIES))

# Ant class
class Ant:
    def __init__(self, num_cities):
        self.num_cities = num_cities
        self.visited = []
        self.total_distance = 0.0

    def visit_city(self, city):
        if self.visited:
            last_city = self.visited[-1]
            self.total_distance += distance_matrix[last_city][city]
        self.visited.append(city)

    def reset(self):
        self.visited = []
        self.total_distance = 0.0

# ACO algorithm
def aco(cities, num_ants, num_iterations, alpha, beta, evaporation_rate, Q):
    num_cities = len(cities)
    pheromones = np.ones((num_cities, num_cities))
    best_path = None
    best_distance = float('inf')

    fig, ax = plt.subplots()

    def update(frame):
        nonlocal best_path, best_distance, pheromones

        ax.clear()
        ants = [Ant(num_cities) for _ in range(num_ants)]

        for ant in ants:
            ant.visit_city(np.random.randint(num_cities))
            for _ in range(num_cities - 1):
                current_city = ant.visited[-1]
                probabilities = []
                for next_city in range(num_cities):
                    if next_city not in ant.visited:
                        pheromone = pheromones[current_city][next_city] ** alpha
                        heuristic = (1.0 / distance_matrix[current_city][next_city]) ** beta
                        probabilities.append(pheromone * heuristic)
                    else:
                        probabilities.append(0)
                probabilities = np.array(probabilities)
                probabilities /= probabilities.sum()
                next_city = np.random.choice(range(num_cities), p=probabilities)
                ant.visit_city(next_city)

            ant.visit_city(ant.visited[0])

            if ant.total_distance < best_distance:
                best_distance = ant.total_distance
                best_path = ant.visited.copy()

        pheromones *= (1 - evaporation_rate)
        for ant in ants:
            for i in range(num_cities):
                from_city = ant.visited[i]
                to_city = ant.visited[(i + 1) % num_cities]
                pheromones[from_city][to_city] += Q / ant.total_distance

        # Plotting cities and paths
        ax.scatter(cities[:, 0], cities[:, 1], c='blue', label='Cities', s=20)  # Smaller points
        for i, city in enumerate(cities):
            ax.text(city[0], city[1], str(i), fontsize=10, color='green')  # Smaller text

        if best_path:
            path_cities = cities[best_path]
            ax.plot(path_cities[:, 0], path_cities[:, 1], 'r-', label='Best Path', linewidth=1)  # Thinner lines
            ax.plot([path_cities[-1, 0], path_cities[0, 0]], [path_cities[-1, 1], path_cities[0, 1]], 'r-', linewidth=1)  # Thinner lines

        ax.set_title(f"Iteration {frame + 1}/{num_iterations}, Best distance: {best_distance:.2f}")
        ax.legend()

    ani = animation.FuncAnimation(fig, update, frames=num_iterations, repeat=False)
    plt.show()

    return best_path, best_distance

best_path, best_distance = aco(cities, NUM_ANTS, NUM_ITERATIONS, ALPHA, BETA, EVAPORATION_RATE, Q)
