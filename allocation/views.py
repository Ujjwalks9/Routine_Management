from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_exempt
from .algorithms.allocation_optimizer import allocate_teachers
from .models import TeacherPreference
from timetable.models import Teacher, Subject

@csrf_exempt
def allocate_teacher_view(request):
    if request.method == 'POST':
        teacher_id = request.POST.get('teacher')
        subject_id = request.POST.get('subject')
        priority = request.POST.get('priority', 1)
        TeacherPreference.objects.create(teacher_id=teacher_id, subject_id=subject_id, priority=priority)
        allocate_teachers()  # Run optimization
        return redirect('view_timetable')
    teachers = Teacher.objects.all()
    subjects = Subject.objects.all()
    return render(request, 'allocation/allocate_teacher.html', {
        'teachers': teachers,
        'subjects': subjects
    })