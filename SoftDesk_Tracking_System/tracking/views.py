from django.shortcuts import render


from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import Ticket
from .serializers import TicketSerializer

@api_view(['GET'])
def ticket_list(request):
    tickets = Ticket.objects.all()
    serializer = TicketSerializer(tickets, many=True)
    return Response(serializer.data)

@api_view(['POST'])
def create_ticket(request):
    serializer = TicketSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=201)
    return Response(serializer.errors, status=400)

@api_view(['GET'])
def ticket_detail(request, pk):
    ticket = Ticket.objects.get(pk=pk)
    serializer = TicketSerializer(ticket)
    return Response(serializer.data)

@api_view(['PUT'])
def update_ticket(request, pk):
    ticket = Ticket.objects.get(pk=pk)
    serializer = TicketSerializer(instance=ticket, data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)
    return Response(serializer.errors, status=400)

@api_view(['DELETE'])
def delete_ticket(request, pk):
    ticket = Ticket.objects.get(pk=pk)
    ticket.delete()
    return Response(status=204)
