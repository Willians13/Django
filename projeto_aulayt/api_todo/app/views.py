
from app.serializers import TodoSerializer
from app.models import Todo

from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import status

@api_view(['GET', 'POST'])
def todo_list(resquest):
    if resquest.method == 'GET':
        todo = Todo.objects.all()
        serializer = TodoSerializer(todo, many=True)
        return Response(serializer.data)
    elif resquest.method == 'POST':
        serializer = TodoSerializer(data = resquest.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_created)
        return Response(serializer.data, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET', 'PUT', 'DELETE'])
def todo_detail_change_and_delete(resquest, pk):
    try:
        todo = Todo.objects.get(pk=pk)
    except Todo.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if resquest.method =='GET':
        serializer = TodoSerializer(todo)
        return Response(serializer.data)
    elif resquest.method == 'PUT':
        serializer = TodoSerializer(todo, data=resquest.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    elif resquest.method == 'DELETE':
        todo.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    