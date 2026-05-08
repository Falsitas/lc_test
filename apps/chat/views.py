from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json

from services.agent import static_agent

@csrf_exempt
def chat(request):
    body = json.loads(request.body)
    query = body.get("query")
    response = static_agent.run_query(query)
    return JsonResponse({"response": response["messages"][-1].content})
