from django.shortcuts import render
from django.http import JsonResponse
from rest_framework.decorators import action
from rest_framework import viewsets
from .backgroundTask import TaskHandler, TaskProgress
from .helper import generateReport

class StoreReportingViewSet(viewsets.ViewSet):
    # Create your views here.
    @action(methods=['GET'],  detail=False, name='Start report generation in background' )
    def trigger_report( self, request ):

        report_id = TaskHandler().start_task( generateReport, [ '' ] )

        return JsonResponse({'report_id':report_id})

    @action(methods=['GET'],  detail=False, name='Get Report/Report Progress' )
    def get_report( self, request ):

        report_id = request.GET[ 'report_id' ]

        task_progress : TaskProgress = TaskHandler.get_task_progress( report_id )

        if task_progress:
            result = vars(task_progress)
            if result.get("status") == 'SUCCESS':
                response = {
                    "report_id": report_id, "status": result.get("status"), "report file": result.get("output")
                }
            else : 
                response = {
                    "report_id": report_id, "status": result.get("status")
                }

            return JsonResponse( response )
        else:
            return JsonResponse( { "report_id": report_id, "status": "LOST", "progress_message": "Report Id cannot be found"} )
