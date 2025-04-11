from django.shortcuts import render
from .models import ScholarsProgram

def scholars_program_overview(request):
    programs = ScholarsProgram.objects.all()
    return render(request, 'scholars/scholars_program_overview.html', {
        'programs': programs
    })
