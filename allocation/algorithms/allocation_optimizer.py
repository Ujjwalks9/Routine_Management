from timetable.models import Teacher, Subject
from allocation.models import Allocation
from allocation.models import TeacherPreference
from deap import base, creator, tools, algorithms
import random

def allocate_teachers():
    teachers = Teacher.objects.all()
    subjects = Subject.objects.all()
    preferences = TeacherPreference.objects.all()

    # Define genetic algorithm for allocation
    creator.create("FitnessMax", base.Fitness, weights=(1.0,))
    creator.create("Individual", list, fitness=creator.FitnessMax)

    def init_individual():
        return [random.choice(teachers).id for _ in subjects]

    def evaluate(individual):
        score = 0
        for subject_id, teacher_id in enumerate(individual, 1):
            pref = preferences.filter(teacher_id=teacher_id, subject_id=subject_id).first()
            score += pref.priority if pref else 0
        return score,

    toolbox = base.Toolbox()
    toolbox.register("individual", tools.initRepeat, creator.Individual, init_individual, n=len(subjects))
    toolbox.register("population", tools.initRepeat, list, toolbox.individual)
    toolbox.register("evaluate", evaluate)
    toolbox.register("mate", tools.cxTwoPoint)
    toolbox.register("mutate", tools.mutShuffleIndexes, indpb=0.2)
    toolbox.register("select", tools.selTournament, tournsize=3)

    # Run genetic algorithm
    population = toolbox.population(n=50)
    for gen in range(30):
        offspring = algorithms.varAnd(population, toolbox, cxpb=0.5, mutpb=0.2)
        fits = toolbox.map(toolbox.evaluate, offspring)
        for ind, fit in zip(offspring, fits):
            ind.fitness.values = fit
        population = toolbox.select(offspring, k=len(population))

    # Save best allocation
    best_ind = tools.selBest(population, k=1)[0]
    for subject_id, teacher_id in enumerate(best_ind, 1):
        Allocation.objects.update_or_create(
            subject_id=subject_id,
            defaults={'teacher_id': teacher_id}
        )
    return best_ind