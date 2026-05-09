from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import permission_classes

from services.agent import static_agent

@csrf_exempt
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def chat(request):
    body = json.loads(request.body)
    query = body.get("query")
    response = static_agent.run_query(query)
    return JsonResponse({"response": response["messages"][-1].content})
