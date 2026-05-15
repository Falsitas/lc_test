from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import permission_classes
from contextvars import ContextVar
from datetime import datetime

from services.registry import get_agent
from security.context import security_context

@csrf_exempt
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def chat(request):
    body = json.loads(request.body)
    query = body.get("query")
    token = security_context.set({
        "user": request.user,
        "ip": request.META.get('REMOTE_ADDR'),
        "time": datetime.now()
    })
    agent = get_agent(request.user)
    response = agent.run_query(query)
    print(response)
    security_context.reset(token)
    return JsonResponse({"response": response["messages"][-1].content})
