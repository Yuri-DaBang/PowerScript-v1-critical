import numpy as np
from scipy.sparse import dok_matrix
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from concurrent.futures import ThreadPoolExecutor

# Constants
NUM_CITIES = 50
NUM_ANTS = 45
NUM_ITERATIONS = 100
ALPHA = 1.0  # Pheromone importance
BETA = 5.0   # Distance importance
EVAPORATION_RATE = 0.5
Q = 100  # Pheromone constant

# Generate random cities
np.random.seed(42)
cities = np.random.rand(NUM_CITIES, 2)

# Calculate the distance matrix
def calculate_distance_matrix(cities):
    return np.linalg.norm(cities[:, None] - cities, axis=-1)

distance_matrix = calculate_distance_matrix(cities)

# Initialize pheromones
# pheromones = dok_matrix((NUM_CITIES, NUM_CITIES))
# pheromones.update({(i, j): 1.0 for i in range(NUM_CITIES) for j in range(NUM_CITIES)})
pheromones = np.ones((NUM_CITIES, NUM_CITIES))

# Precompute probabilities and heuristics
heuristics = 1.0 / distance_matrix
np.fill_diagonal(heuristics, 0)  # Avoid division by zero
probabilities = np.zeros_like(distance_matrix)

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
    best_path = None
    best_distance = float('inf')

    fig, ax = plt.subplots()

    def update(frame):
        nonlocal best_path, best_distance

        ax.clear()
        ants = [Ant(NUM_CITIES) for _ in range(num_ants)]

        with ThreadPoolExecutor() as executor:
            futures = []
            for ant in ants:
                ant.visit_city(np.random.randint(NUM_CITIES))
                futures.append(executor.submit(move_ant, ant))

            for future in futures:
                future.result()

        for ant in ants:
            if ant.total_distance < best_distance:
                best_distance = ant.total_distance
                best_path = ant.visited.copy()

        pheromones *= (1 - evaporation_rate)
        for ant in ants:
            for i in range(NUM_CITIES):
                from_city = ant.visited[i]
                to_city = ant.visited[(i + 1) % NUM_CITIES]
                pheromones[from_city, to_city] += Q / ant.total_distance

        # Plotting cities and paths
        ax.scatter(cities[:, 0], cities[:, 1], c='blue', label='Cities', s=5)  # Smaller points
        if best_path:
            path_cities = cities[best_path]
            ax.plot(path_cities[:, 0], path_cities[:, 1], 'r-', label='Best Path', linewidth=0.5)  # Thinner lines
            ax.plot([path_cities[-1, 0], path_cities[0, 0]], [path_cities[-1, 1], path_cities[0, 1]], 'r-', linewidth=0.5)  # Thinner lines

        ax.set_title(f"Iteration {frame + 1}/{num_iterations}, Best distance: {best_distance:.2f}")
        ax.legend()

    ani = animation.FuncAnimation(fig, update, frames=num_iterations, repeat=False)
    plt.show()

    return best_path, best_distance

def move_ant(ant):
    for _ in range(NUM_CITIES - 1):
        current_city = ant.visited[-1]
        probabilities[current_city] = np.where(np.isin(range(NUM_CITIES), ant.visited), 0, pheromones[current_city] ** ALPHA * heuristics[current_city] ** BETA)
        probabilities[current_city] /= probabilities[current_city].sum()
        next_city = np.random.choice(range(NUM_CITIES), p=probabilities[current_city])
        ant.visit_city(next_city)

    ant.visit_city(ant.visited[0])

aco(cities, NUM_ANTS, NUM_ITERATIONS, ALPHA, BETA, EVAPORATION_RATE, Q)
