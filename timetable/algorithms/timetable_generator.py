from deap import base, creator, tools, algorithms
import random
import logging
from timetable.models import Teacher, Subject, Class, Room, TimeSlot
from allocation.models import Allocation, TeacherPreference
from .clash_detector import check_clashes
from datetime import datetime

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

class FastClashChecker:
    def __init__(self, teachers, timeslots):
        self.teacher_availability = {}  # teacher_id -> {day: [(start, end)]}
        self.timeslot_info = {}  # timeslot_id -> (day, start, end)
        
        # Cache timeslot info
        for ts in timeslots:
            self.timeslot_info[ts.id] = (ts.day, ts.start_time, ts.end_time)
        
        # Cache and parse teacher availability
        for teacher in teachers:
            availability = {}
            for day, ranges in teacher.availability.items():
                times = []
                for time_range in ranges:
                    try:
                        start, end = time_range.split("-")
                        start_time = datetime.strptime(start.strip(), "%H:%M").time()
                        end_time = datetime.strptime(end.strip(), "%H:%M").time()
                        times.append((start_time, end_time))
                    except (ValueError, AttributeError):
                        continue
                if times:
                    availability[day] = times
            self.teacher_availability[teacher.id] = availability

    def check_availability(self, teacher_id, timeslot_id):
        if teacher_id not in self.teacher_availability:
            return False
        
        day, start, end = self.timeslot_info[timeslot_id]
        for avail_start, avail_end in self.teacher_availability[teacher_id].get(day, []):
            if avail_start <= start and end <= avail_end:
                return True
        return False

def generate_timetable():
    # Fetch all data upfront
    teachers = list(Teacher.objects.all())
    subjects = list(Subject.objects.all())
    classes = list(Class.objects.all())
    rooms = list(Room.objects.all())
    timeslots = list(TimeSlot.objects.all())
    preferences = list(TeacherPreference.objects.all())
    
    # Initialize fast clash checker
    checker = FastClashChecker(teachers, timeslots)

    logger.debug(f"Teachers: {len(teachers)}, Subjects: {len(subjects)}, Classes: {len(classes)}, Rooms: {len(rooms)}, Timeslots: {len(timeslots)}, Preferences: {len(preferences)}")

    if not all([teachers, subjects, classes, rooms, timeslots]):
        logger.error("Insufficient data in database")
        raise ValueError("Insufficient data: Ensure teachers, subjects, classes, rooms, and timeslots are populated.")

    # Map teacher preferences, sorted by priority (lowest priority value = highest preference)
    teacher_subjects = {teacher.id: [] for teacher in teachers}
    for pref in preferences:
        if pref.teacher_id in teacher_subjects:
            teacher_subjects[pref.teacher_id].append((pref.subject_id, pref.priority))
    for teacher_id in teacher_subjects:
        teacher_subjects[teacher_id].sort(key=lambda x: x[1])  # Sort by priority (ascending)

    NUM_ALLOCATIONS = max(2, min(10, len(subjects) * len(classes) * len(timeslots)))

    # Clear existing DEAP classes
    if hasattr(creator, 'FitnessMin'):
        del creator.FitnessMin
    if hasattr(creator, 'Individual'):
        del creator.Individual

    creator.create("FitnessMin", base.Fitness, weights=(-1.0, -1.0, -1.0))  # Minimize clashes, preference violations, class coverage
    creator.create("Individual", list, fitness=creator.FitnessMin)

    def init_individual():
        timetable = []
        used_slots = set()
        class_ids = [c.id for c in classes]  # Ensure coverage of all classes
        random.shuffle(class_ids)
        for class_id in class_ids:
            for _ in range(100):  # Increased attempts for valid allocation
                teacher = random.choice(teachers)
                timeslot = random.choice(timeslots)
                room = random.choice(rooms)
                if (teacher.id, timeslot.id) not in used_slots and (room.id, timeslot.id) not in used_slots:
                    if check_clashes(teacher.id, room.id, timeslot.id) == 0:
                        preferred_subjects = [s[0] for s in teacher_subjects.get(teacher.id, [])]
                        subject_id = preferred_subjects[0] if preferred_subjects else random.choice(subjects).id
                        timetable.append([teacher.id, subject_id, class_id, room.id, timeslot.id])
                        used_slots.add((teacher.id, timeslot.id))
                        used_slots.add((room.id, timeslot.id))
                        break
            else:
                continue
        if len(timetable) < NUM_ALLOCATIONS:
            for _ in range(NUM_ALLOCATIONS - len(timetable)):
                for _ in range(100):
                    teacher = random.choice(teachers)
                    timeslot = random.choice(timeslots)
                    room = random.choice(rooms)
                    if (teacher.id, timeslot.id) not in used_slots and (room.id, timeslot.id) not in used_slots:
                        if check_clashes(teacher.id, room.id, timeslot.id) == 0:
                            preferred_subjects = [s[0] for s in teacher_subjects.get(teacher.id, [])]
                            subject_id = preferred_subjects[0] if preferred_subjects else random.choice(subjects).id
                            timetable.append([teacher.id, subject_id, random.choice(classes).id, room.id, timeslot.id])
                            used_slots.add((teacher.id, timeslot.id))
                            used_slots.add((room.id, timeslot.id))
                            break
        if not timetable:
            # Fallback: Exhaustive search for one valid allocation
            for teacher in teachers:
                for timeslot in timeslots:
                    for room in rooms:
                        if (teacher.id, timeslot.id) not in used_slots and (room.id, timeslot.id) not in used_slots:
                            if check_clashes(teacher.id, room.id, timeslot.id) == 0:
                                preferred_subjects = [s[0] for s in teacher_subjects.get(teacher.id, [])]
                                subject_id = preferred_subjects[0] if preferred_subjects else random.choice(subjects).id
                                timetable.append([teacher.id, subject_id, random.choice(classes).id, room.id, timeslot.id])
                                return creator.Individual(timetable)
        return creator.Individual(timetable)

    def evaluate(individual):
        clashes = 0
        preference_violations = 0
        class_coverage_violation = 0
        teacher_slots = set()
        room_slots = set()
        covered_classes = set()
        for allocation in individual:
            if not allocation:
                continue
            teacher_id, subject_id, class_id, room_id, timeslot_id = allocation
            
            # Check teacher and room slot conflicts
            if (teacher_id, timeslot_id) in teacher_slots:
                clashes += 100
            else:
                teacher_slots.add((teacher_id, timeslot_id))
            
            if (room_id, timeslot_id) in room_slots:
                clashes += 100
            else:
                room_slots.add((room_id, timeslot_id))
            
            # Use FastClashChecker for availability
            if not checker.check_availability(teacher_id, timeslot_id):
                clashes += 50
            
            # Check subject preferences
            preferred_subjects = [s[0] for s in teacher_subjects.get(teacher_id, [])]
            if preferred_subjects and subject_id not in preferred_subjects:
                preference_violations += 50
            elif preferred_subjects:
                for idx, (subj_id, priority) in enumerate(teacher_subjects[teacher_id]):
                    if subj_id == subject_id:
                        preference_violations += priority * 20
                        break
            
            covered_classes.add(class_id)
        
        # Penalize missing class coverage
        class_coverage_violation = (len(classes) - len(covered_classes)) * 30
        return clashes, preference_violations, class_coverage_violation

    def custom_crossover(ind1, ind2):
        size = min(len(ind1), len(ind2))
        if size < 2:
            return ind1, ind2
        cxpoint1 = random.randint(1, size - 1)
        cxpoint2 = random.randint(cxpoint1, size - 1)
        child1_list = ind1[:cxpoint1] + ind2[cxpoint1:cxpoint2] + ind1[cxpoint2:]
        child2_list = ind2[:cxpoint1] + ind1[cxpoint1:cxpoint2] + ind2[cxpoint2:]
        for child_list in (child1_list, child2_list):
            teacher_slots = set()
            room_slots = set()
            for i, allocation in enumerate(child_list):
                if not allocation:
                    continue
                teacher_id, subject_id, class_id, room_id, timeslot_id = allocation
                if (teacher_id, timeslot_id) in teacher_slots or (room_id, timeslot_id) in room_slots or check_clashes(teacher_id, room_id, timeslot_id) > 0:
                    for _ in range(100):  # Increased attempts
                        teacher = random.choice(teachers)
                        timeslot = random.choice(timeslots)
                        room = random.choice(rooms)
                        if (teacher.id, timeslot.id) not in teacher_slots and (room.id, timeslot.id) not in room_slots and check_clashes(teacher.id, room.id, timeslot.id) == 0:
                            preferred_subjects = [s[0] for s in teacher_subjects.get(teacher.id, [])]
                            subject_id = preferred_subjects[0] if preferred_subjects else random.choice(subjects).id
                            child_list[i] = [teacher.id, subject_id, class_id, room.id, timeslot.id]
                            teacher_slots.add((teacher.id, timeslot.id))
                            room_slots.add((room.id, timeslot.id))
                            break
                    else:
                        child_list[i] = None
            child_list[:] = [alloc for alloc in child_list if alloc is not None]
        return creator.Individual(child1_list), creator.Individual(child2_list)

    def mutate(individual):
        for i in range(len(individual)):
            if random.random() < 0.2:
                for _ in range(100):  # Increased attempts
                    teacher = random.choice(teachers)
                    timeslot = random.choice(timeslots)
                    room = random.choice(rooms)
                    if check_clashes(teacher.id, room.id, timeslot.id) == 0:
                        preferred_subjects = [s[0] for s in teacher_subjects.get(teacher.id, [])]
                        subject_id = preferred_subjects[0] if preferred_subjects else random.choice(subjects).id
                        individual[i] = [teacher.id, subject_id, random.choice(classes).id, room.id, timeslot.id]
                        break
                else:
                    individual[i] = None
        individual[:] = [alloc for alloc in individual if alloc is not None]
        return individual,

    toolbox = base.Toolbox()
    toolbox.register("individual", init_individual)
    toolbox.register("population", tools.initRepeat, list, toolbox.individual)
    toolbox.register("evaluate", evaluate)
    toolbox.register("mate", custom_crossover)
    toolbox.register("mutate", mutate)
    toolbox.register("select", tools.selTournament, tournsize=3)

    population = toolbox.population(n=100)
    for gen in range(50):
        offspring = algorithms.varAnd(population, toolbox, cxpb=0.5, mutpb=0.2)
        fits = toolbox.map(toolbox.evaluate, offspring)
        for ind, fit in zip(offspring, fits):
            ind.fitness.values = fit
        population = toolbox.select(offspring, k=len(population))

    Allocation.objects.all().delete()
    best_ind = tools.selBest(population, k=1)[0]
    saved_allocations = 0
    teacher_slots = set()
    room_slots = set()
    covered_classes = set()
    for allocation in best_ind:
        if not allocation:
            continue
        teacher_id, subject_id, class_id, room_id, timeslot_id = allocation
        if (teacher_id, timeslot_id) in teacher_slots or (room_id, timeslot_id) in room_slots:
            logger.debug(f"Skipping allocation due to clash: teacher_id={teacher_id}, room_id={room_id}, timeslot_id={timeslot_id}")
            continue
        if check_clashes(teacher_id, room_id, timeslot_id) == 0:
            try:
                teacher = Teacher.objects.get(id=teacher_id)
                subject = Subject.objects.get(id=subject_id)
                class_instance = Class.objects.get(id=class_id)
                room = Room.objects.get(id=room_id)
                timeslot = TimeSlot.objects.get(id=timeslot_id)
                # Ensure highest-priority subject
                preferred_subjects = [s[0] for s in teacher_subjects.get(teacher_id, [])]
                if preferred_subjects and subject_id != preferred_subjects[0]:
                    logger.debug(f"Skipping allocation due to non-optimal subject: teacher={teacher.name}, subject={subject.name}")
                    continue
                logger.debug(f"Creating allocation with teacher={teacher.name}, subject={subject.name}, class={class_instance.name}, room={room.name}, timeslot={timeslot.day} {timeslot.start_time}-{timeslot.end_time}")
                Allocation.objects.create(
                    teacher=teacher,
                    subject=subject,
                    class_id=class_instance,
                    room=room,
                    timeslot=timeslot
                )
                teacher_slots.add((teacher_id, timeslot_id))
                room_slots.add((room_id, timeslot_id))
                covered_classes.add(class_id)
                saved_allocations += 1
            except (Teacher.DoesNotExist, Subject.DoesNotExist, Class.DoesNotExist, Room.DoesNotExist, TimeSlot.DoesNotExist) as e:
                logger.error(f"Invalid ID in allocation: {e}")
                continue
    logger.info(f"Created {saved_allocations} allocations from best timetable")
    return best_ind