from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from base.models import Team
from base.serializer import TeamSerializer
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.conf import settings


@api_view(['GET'])
def getTeams(request):

    filters = {}
    filtersResponse = {}

    nameFilter = request.query_params.get('name')
    idFilter = request.query_params.get('id')

    pagination = request.query_params.get('pagination')

    try:
        pagination = int(pagination)
    except:
        pagination = settings.DEFAULT_PAGINATION


    if nameFilter and nameFilter != '':
        filters['name__icontains'] = nameFilter
        filtersResponse['name'] = nameFilter


    try:
        idFilter = int(idFilter)
    except:
        idFilter = None

    if idFilter:
        filters['id'] = idFilter
        filtersResponse['id'] = idFilter

    items = Team.objects.filter(**filters)

    page = request.query_params.get('page')
    paginator = Paginator(items, pagination)

    try:
        items = paginator.page(page)
    except PageNotAnInteger:
        items = paginator.page(1)
    except EmptyPage:
        items = paginator.page(paginator.num_pages)

    if page == None:
        page = 1

    page = int(page)      

    serializer = TeamSerializer(items, many=True)

    return Response({'status': status.HTTP_200_OK, 'list_teams': serializer.data, 'page': page, 'pages': paginator.num_pages, 'filters': filtersResponse}, status=status.HTTP_200_OK)


@api_view(['GET'])
def getTeamDetails(request):

    try:
        id = int(request.query_params.get('id'))
    except:
        message = 'Faltando parâmetro ID'
        return Response({'status': status.HTTP_400_BAD_REQUEST, 'team_details': message}, status=status.HTTP_400_BAD_REQUEST)

    try:
        item = Team.objects.get(id=id)
    except:
        message = 'Equipe não encontrada'
        return Response({'status': status.HTTP_404_NOT_FOUND, 'team_details': message}, status=status.HTTP_404_NOT_FOUND)
    
    serializer = TeamSerializer(item, many=False)

    return Response({'status': status.HTTP_200_OK, 'team_details': serializer.data}, status=status.HTTP_200_OK)

@api_view(['POST'])
def createTeam(request):
    
    data = request.data

    try:

        item = Team.objects.create(
            name = data['name'],
        )
        serializer = TeamSerializer(item, many=False)
        return Response({'status': status.HTTP_201_CREATED, 'create_team': serializer.data}, status=status.HTTP_201_CREATED)
    
     
    except:
        message = 'Erro ao criar a equipe. Verifique se o nome já existe.'
        return Response({'status': status.HTTP_404_NOT_FOUND, 'create_team': message}, status=status.HTTP_404_NOT_FOUND)


@api_view(['DELETE'])
def deleteTeam(request):

    try:
        id = int(request.query_params.get('id'))
    except:
        message = 'Faltando parâmetro ID'
        return Response({'status': status.HTTP_400_BAD_REQUEST, 'delete_team': message}, status=status.HTTP_400_BAD_REQUEST)
    
    try:
        item = Team.objects.get(id=id)
    except:
        message = 'Equipe não encontrada'
        return Response({'status': status.HTTP_404_NOT_FOUND, 'delete_team': message}, status=status.HTTP_404_NOT_FOUND)

    try:
        item.delete()
    except:
        message = 'Equipe não pode ser apagada, existem processos seletivos nos quais se encontra cadastrada.'
        return Response({'status': status.HTTP_428_PRECONDITION_REQUIRED, 'delete_team': message}, status=status.HTTP_428_PRECONDITION_REQUIRED)
    
    
    return Response({'status': status.HTTP_200_OK, 'delete_team': {"id": id, "name": item.name}}, status=status.HTTP_200_OK)


@api_view(['PUT'])
def updateTeam(request):

    try:
        id = int(request.query_params.get('id'))
    except:
        message = 'Faltando parâmetro ID'
        return Response({'status': status.HTTP_400_BAD_REQUEST, 'update_team': message}, status=status.HTTP_400_BAD_REQUEST)
    
    try:
        item = Team.objects.get(id=id)
    except:
        message = 'Equipe não encontrada'
        return Response({'status': status.HTTP_404_NOT_FOUND, 'update_team': message}, status=status.HTTP_404_NOT_FOUND)

    data = request.data

    try:

        item.name = data['name']
        item.save()
        serializer = TeamSerializer(item, many=False)
        
        return Response({'status': status.HTTP_200_OK, 'update_team': serializer.data}, status=status.HTTP_200_OK)

    except:
        message = 'Erro ao atualizar a equipe'
        return Response({'status': status.HTTP_404_NOT_FOUND, 'update_team': message}, status=status.HTTP_404_NOT_FOUND)