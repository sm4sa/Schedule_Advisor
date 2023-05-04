import datetime

from django.shortcuts import render, get_object_or_404

from scheduling_app.authentication_decorators import account_type_required
from scheduling_app.models import StudentSchedule, Course
from scheduling_app.sis_api import By, Semester
from scheduling_app.sis_api.populate_database import fill_database_by_query
from scheduling_app.views.utilities import create_schedule_if_unique, get_user_schedules


def course_view(request, course_pk):
    context = {
        'course': get_object_or_404(Course, pk=course_pk),
        'midnight': datetime.time(0, 0, 0)
    }
    return render(request, 'scheduling_app/course-detail.html', context)

@account_type_required()
def course_table_view(request):
    if request.method == 'POST':
        form = request.POST
        if 'filter_form' in form:
            return course_table_filter_form(request)
        elif 'create_schedule_form' in form:
            return course_table_create_schedule_form(form, request)
        elif 'add_course_to_schedule_form' in form:
            return course_table_add_course_to_schedule_form(form, request)
    else:
        return course_table_base_page(request)


def course_table_base_page(request):
    return render(request, 'scheduling_app/course-table.html', context=get_base_context(request))


def get_base_context(request):
    context = {
        'schedules': get_user_schedules(request.user)
    }
    if 'filters' in (session := request.session):
        context['courses'] = Course.objects.filter(**session['filters'])
    else:
        context['courses'] = []
    return context


def course_table_add_course_to_schedule_form(form, request):
    schedule_pk = int(form['add_schedule'])
    student_schedule = get_object_or_404(StudentSchedule, pk=schedule_pk)
    course_pk = int(form['add_course'])
    course = get_object_or_404(Course, pk=course_pk)
    context = get_base_context(request)
    if student_schedule.has_course(course):
        context['message'] = {
            'title': 'Error!',
            'body': 'The selected course is already within the schedule.',
            'type': 'error'
        }
    elif student_schedule.overlaps(course):
        context['message'] = {
                'title': 'Error!',
                'body': 'The selected courses conflict. Please select a different course.',
                'type': 'error'
        }
    else:
        student_schedule.courses.add(course.pk)
        context['message'] = {
            'title': 'Success!',
            'body': f'"{course.course_identifier.course_description}" was successfully added to "{student_schedule.name}"',
            'type': 'success'
        }
    return render(request, 'scheduling_app/course-table.html', context=context)


def course_table_create_schedule_form(form, request):
    context = get_base_context(request)
    context['message'] = create_schedule_if_unique(request.user, form['schedule_name'])
    return render(request, 'scheduling_app/course-table.html', context=context)

def get_database_filters(form):
    database_filter = {}
    if subject := form['subject']:
        database_filter['course_identifier__subject__icontains'] = subject
    if catalog_number := form['catalog_number']:
        database_filter['course_identifier__catalog_number'] = catalog_number
    if class_number := form['class_number']:
        database_filter['registration_information__class_number'] = class_number
    if professor := form['professor']:
        database_filter['instructors__name__icontains'] = professor
    if keyword := form['keyword']:
        database_filter['course_identifier__course_description__icontains'] = keyword
    return database_filter

def get_api_filters_base():
    return [By.term(2023, Semester.SUMMER)]

def are_api_filters_set(filters):
    return filters != get_api_filters_base()

def get_api_filters(form):
    course_filter = get_api_filters_base()
    if form['subject']:
        course_filter.append(By.subject(form['subject'].upper()))
    if form['catalog_number']:
        course_filter.append(By.catalog_number(form['catalog_number']))
    if form['class_number']:
        course_filter.append(By.class_number(form['class_number']))
    if form['professor']:
        course_filter.append(By.instructor(form['professor']))
    if form['keyword']:
        course_filter.append(By.keyword(form['keyword']))
    return course_filter

def course_table_filter_form(request):
    kwargs = get_database_filters(request.POST)
    course_filter = get_api_filters(request.POST)
    courses = Course.objects.all().filter(**kwargs)
    if are_api_filters_set(course_filter):
        request.session['filters'] = kwargs
        if not courses:
            courses = fill_database_by_query(*course_filter)
        context = {
            'courses': courses,
            'schedules': get_user_schedules(request.user)
        }
    else:
        context = get_base_context(request)
        context['message'] = {
                'title': 'Error! Invalid Filter',
                'body': 'Please select at least one filter',
                'type': 'error'
        }
    return render(request, 'scheduling_app/course-table.html', context=context)
