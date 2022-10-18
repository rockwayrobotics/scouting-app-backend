from django.http import HttpResponse
from django.views import View
from django.template import loader

from .models import TeamData
from .opencv import test_function

class MainView(View):
    def get(self, request, team=0):
        if team:
            try:
                team_data = TeamData.objects.get(id=team)
            except TeamData.DoesNotExist:
                raise Http404("Team does not exist")
            template = loader.get_template('GUI/team.html')
            context = {
                    'team': team_data,
            }
            return HttpResponse(template.render(context, request))

        else:
            # start OpenCV stuff here

            test_function()
            latest_data_list = TeamData.objects.order_by('-record_date')[:5]
            template = loader.get_template('GUI/index.html')
            context = {
                    'latest_data_list': latest_data_list,
            }
            return HttpResponse(template.render(context, request))
