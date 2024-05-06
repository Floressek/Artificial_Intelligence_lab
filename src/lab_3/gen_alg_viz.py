#########################################################
#                         import                        #
#########################################################

import numpy as np
import random
import tkinter as tk
from tkinter import ttk
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

Gen_max = 100
pop_size = 50


#########################################################
#                          rules                        #
#########################################################
def fitness(x):
    return 2 * x[0] ** 2 + x[1] ** 3 - x[2] ** 2 + 7 * x[3] ** 2 - 2 * x[4] ** 5


def generate_individual():
    return np.array([
        random.randint(0, 10),  # x0, constrained to <= 10
        random.choice([i for i in range(1, 26) if i % 10 in range(1, 8)]),  # x1, mod 10 in {1,...,7}
        random.randint(1, 25),  # x2, >= 1
        random.randint(0, 20),  # x3, <= 20
        random.randint(6, 25)  # x4, > 5
    ])


def crossover(parent1, parent2):
    return np.array([parent1[i] if random.random() < 0.5 else parent2[i] for i in range(len(parent1))])


def mutate(individual, mutation_rate=0.1):
    print(f"Child: {individual}")
    for i in range(len(individual)):
        if random.random() < mutation_rate:
            individual[i] = generate_individual()[i]
    print(f"Mutated child: {individual}")
    return individual


# def on_hover(event):
#     if line.contains(event)[0]:
#         ind = int(event.xdata)  # the index of the point
#         if ind is not None and ind < len(best_fitnesses):
#             value_label.config(
#                 text=f"Generation: {ind + 1}\nBest Fitness: {best_fitnesses[ind]}\nBest set: {population_data[ind]}")
#             print(f"HOVER => Generation: {ind + 1}, Best Fitness: {best_fitnesses[ind]}, Best set: {population_data[ind]}")

def on_hover(event):
    # Display tooltip if hovering over a line point
    if line.contains(event)[0]:
        tooltip_text.set(
            f"Generation: {int(event.xdata) + 1}\nBest Fitness: {best_fitnesses[int(event.xdata)]}\nBest set: {population_data[int(event.xdata)]}")
        print(f"HOVER => Generation: {int(event.xdata) + 1}, Best Fitness: {best_fitnesses[int(event.xdata)]}, Best set: {population_data[int(event.xdata)]}")
        tooltip.place(x=event.x, y=event.y)  # Position the tooltip at the cursor location
        canvas_widget.config(cursor="hand2")  # Change the cursor
    else:
        tooltip.place_forget()  # Hide the tooltip if not hovering over the line
        canvas_widget.config(cursor="")


#########################################################
#                           Main                        #
#########################################################

# Define the main genetic algorithm function
def run_genetic_algorithm(update_interval):
    global population, ax, canvas, line, best_fitnesses, running, current_generation, value_label, population_data

    #   for generation in range(1):  # Just a single generation per call
    if not running or current_generation >= Gen_max:
        return
    fitnesses = [fitness(ind) for ind in population]
    best_fitness = max(fitnesses)
    best_fitnesses.append(best_fitness)
    best_index = np.argmax(fitnesses)
    population_data.append(population[best_index])  # Store the best individual of the generation

    # Update the graph
    line.set_ydata(best_fitnesses)
    line.set_xdata(range(len(best_fitnesses)))
    ax.relim()
    ax.autoscale_view()
    canvas.draw()

    # Update display values
    current_generation += 1
    value_label.config(text=f"Generation: {current_generation}\nBest Fitness: {best_fitness}"
                            f"\nBest set: {population[np.argmax(fitnesses)]}")
    print(f"Generation {current_generation}, Best fitness: {best_fitness}",
          f"Best set: {population[np.argmax(fitnesses)]}")

    # Select, crossover, and mutate to create a new generation
    population = [mutate(crossover(population[np.argmax(fitnesses)], random.choice(population))) for _ in
                  range(len(population))]

    if running:
        root.after(update_interval, run_genetic_algorithm, update_interval)  # Schedule the next generation


def start():
    global running, current_generation, best_fitnesses, population, population_data
    current_generation = 0
    best_fitnesses = []
    population_data = []
    population = [generate_individual() for _ in range(pop_size)]
    running = True
    run_genetic_algorithm(100)


def stop():
    global running
    running = False


def resume():
    global running, current_generation, best_fitnesses, population
    running = True
    # population = [generate_individual() for _ in range(pop_size)]
    run_genetic_algorithm(100)


# Initialize population and set up the GUI
population = [generate_individual() for _ in range(pop_size)]
best_fitnesses = []
population_data = []  # Store the best individual of each generation
current_generation = 0
running = False


#########################################################
#                           GUI                         #
#########################################################
root = tk.Tk()
root.title("Genetic Algorithm Simulation")

style = ttk.Style()
style.theme_use('clam')  # Using 'clam' which allows for more customization
style.configure('TButton', background='#333', foreground='cyan', font=('Helvetica', 12))
style.configure('TLabel', background='#333', foreground='magenta', font=('Helvetica', 12))

frame = ttk.Frame(root, style='TFrame')
frame.pack(fill=tk.BOTH, expand=True)

fig, ax = plt.subplots()
fig.patch.set_facecolor('#333333')  # Setting the background color of the plot
ax.set_facecolor('#333333')
line, = ax.plot([], [], 'r', label='Best Fitness')  # Start with an empty red line
ax.set_title("Best Fitness Over Generations", color='white')
ax.tick_params(axis='x', colors='cyan')
ax.tick_params(axis='y', colors='cyan')
canvas = FigureCanvasTkAgg(fig, master=frame)
canvas_widget = canvas.get_tk_widget()
canvas_widget.pack(fill=tk.BOTH, expand=True)
canvas.mpl_connect('motion_notify_event', on_hover)  # Connect the hover event

tooltip_text = tk.StringVar()
tooltip = ttk.Label(frame, textvariable=tooltip_text, background='white', foreground='black', relief='solid', borderwidth=1, padding=5)

start_button = ttk.Button(root, text="Start/Restart", command=start)
start_button.pack(side=tk.LEFT, padx=5, pady=5)

stop_button = ttk.Button(root, text="Stop", command=stop)
stop_button.pack(side=tk.LEFT, padx=5, pady=5)

stop_button = ttk.Button(root, text="Resume", command=resume)
stop_button.pack(side=tk.LEFT, padx=5, pady=5)

value_label = ttk.Label(root, text="Generation: 0\nBest Fitness: 0\n Best set: 0", style='TLabel')
value_label.pack(side=tk.RIGHT, padx=5, pady=5)

root.mainloop()
