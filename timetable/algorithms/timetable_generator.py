from deap import base, creator, tools, algorithms
import random
from timetable.models import Teacher, Subject, Class, Room, TimeSlot, Allocation
from .clash_detector import check_clashes

def generate_timetable():
    # Fetch data
    teachers = Teacher.objects.all()
    subjects = Subject.objects.all()
    classes = Class.objects.all()
    rooms = Room.objects.all()
    timeslots = TimeSlot.objects.all()

    # Define genetic algorithm setup
    creator.create("FitnessMin", base.Fitness, weights=(-1.0,))
    creator.create("Individual", list, fitness=creator.FitnessMin)

    def init_individual():
        # Randomly assign teacher, subject, class, room, timeslot
        return [random.choice(teachers).id, random.choice(subjects).id,
                random.choice(classes).id, random.choice(rooms).id,
                random.choice(timeslots).id]

    def evaluate(individual):
        teacher_id, subject_id, class_id, room_id, timeslot_id = individual
        clashes = check_clashes(teacher_id, room_id, timeslot_id)
        return clashes,  # Minimize clashes

    toolbox = base.Toolbox()
    toolbox.register("individual", tools.initRepeat, creator.Individual, init_individual, n=1)
    toolbox.register("population", tools.initRepeat, list, toolbox.individual)
    toolbox.register("evaluate", evaluate)
    toolbox.register("mate", tools.cxTwoPoint)
    toolbox.register("mutate", tools.mutShuffleIndexes, indpb=0.2)
    toolbox.register("select", tools.selTournament, tournsize=3)

    # Run genetic algorithm
    population = toolbox.population(n=100)
    for gen in range(50):
        offspring = algorithms.varAnd(population, toolbox, cxpb=0.5, mutpb=0.2)
        fits = toolbox.map(toolbox.evaluate, offspring)
        for ind, fit in zip(offspring, fits):
            ind.fitness.values = fit
        population = toolbox.select(offspring, k=len(population))

    # Save best solution
    best_ind = tools.selBest(population, k=1)[0]
    Allocation.objects.create(
        teacher_id=best_ind[0],
        subject_id=best_ind[1],
        class_id=best_ind[2],
        room_id=best_ind[3],
        timeslot_id=best_ind[4]
    )
    return best_ind