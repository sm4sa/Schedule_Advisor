from django.shortcuts import render, get_object_or_404

from scheduling_app.authentication_decorators import student_required, advisor_required
from scheduling_app.models import StudentSchedule
from scheduling_app.views.utilities import get_pending_schedules_or_none, create_schedule_if_unique, get_user_schedules


def home_view(request):
    return render(request, 'scheduling_app/about.html')


def number_status(schedules, status):
    status_list = [schedule.status for schedule in schedules]
    return status_list.count(str(status))


@student_required()
def student_schedules_view(request):
    context = {}
    if request.method == 'POST':
        form = request.POST
        if 'delete_course_form' in form:
            course_pk = int(form['course_pk'])
            schedule_pk = int(form['schedule_pk'])

            schedule = get_object_or_404(StudentSchedule, pk=schedule_pk)
            schedule.courses.remove(course_pk)
            schedule.save()
        elif 'edit_schedule_form' in form:
            schedule_pk = int(form['schedule_pk'])
            schedule = get_object_or_404(StudentSchedule, pk=schedule_pk)
            if 'submit' in form:
                schedule.status = StudentSchedule.Status.PENDING
                schedule.save()
            elif 'withdraw' in form:
                schedule.status = StudentSchedule.Status.NOT_SUBMITTED
                schedule.save()
            elif 'delete' in form:
                schedule.delete()
        elif 'create_schedule_form' in form:
            context['message'] = create_schedule_if_unique(request.user, form['schedule_name'])
    schedules = get_user_schedules(request.user)
    context['schedules'] = schedules
    context['num_not_submitted'] = number_status(schedules, StudentSchedule.Status.NOT_SUBMITTED)
    context['num_pending'] = number_status(schedules, StudentSchedule.Status.PENDING)
    context['num_rejected'] = number_status(schedules, StudentSchedule.Status.REJECTED)
    context['num_approved'] = number_status(schedules, StudentSchedule.Status.APPROVED)
    return render(request, 'scheduling_app/student-schedule-table.html', context=context)


@advisor_required()
def advisor_schedules_view(request):
    if request.method == 'POST':
        form = request.POST
        if 'edit_schedule_status_form' in form:
            schedule_pk = int(form['schedule_pk'])
            schedule = get_object_or_404(StudentSchedule, pk=schedule_pk)
            if 'approve' in form:
                schedule.status = StudentSchedule.Status.APPROVED
                schedule.save()
            elif 'reject' in form:
                schedule.status = StudentSchedule.Status.REJECTED
                schedule.save()
    context = {
        'schedules': get_pending_schedules_or_none()
    }
    return render(request, 'scheduling_app/advisor-schedule-table.html', context)
