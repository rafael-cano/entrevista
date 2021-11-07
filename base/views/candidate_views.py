from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from base.models import Candidate, SelectionProcess
from base.serializer import CandidateSerializer
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.conf import settings


@api_view(['GET'])
def getCandidates(request):

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

    items = Candidate.objects.filter(**filters)

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

    serializer = CandidateSerializer(items, many=True)

    return Response({'status': status.HTTP_200_OK, 'list_candidates': serializer.data, 'page': page, 'pages': paginator.num_pages, 'filters': filtersResponse}, status=status.HTTP_200_OK)


@api_view(['GET'])
def getCandidateDetails(request):

    try:
        id = int(request.query_params.get('id'))
    except:
        message = 'Faltando parâmetro ID'
        return Response({'status': status.HTTP_400_BAD_REQUEST, 'candidate_details': message}, status=status.HTTP_400_BAD_REQUEST)

    try:
        item = Candidate.objects.get(id=id)
    except:
        message = 'Candidato não encontrado'
        return Response({'status': status.HTTP_404_NOT_FOUND, 'candidate_details': message}, status=status.HTTP_404_NOT_FOUND)
    
    serializer = CandidateSerializer(item, many=False)

    return Response({'status': status.HTTP_200_OK, 'candidate_details': serializer.data}, status=status.HTTP_200_OK)

@api_view(['POST'])
def createCandidate(request):
    
    data = request.data

    try:

        item = Candidate.objects.create(
            name = data['name'],
        )
        serializer = CandidateSerializer(item, many=False)
        return Response({'status': status.HTTP_201_CREATED, 'create_candidate': serializer.data}, status=status.HTTP_201_CREATED)
    
     
    except:
        message = 'Erro ao criar o candidato. Verifique se o nome já existe.'
        return Response({'status': status.HTTP_404_NOT_FOUND, 'create_candidate': message}, status=status.HTTP_404_NOT_FOUND)


@api_view(['DELETE'])
def deleteCandidate(request):

    try:
        id = int(request.query_params.get('id'))
    except:
        message = 'Faltando parâmetro ID'
        return Response({'status': status.HTTP_400_BAD_REQUEST, 'delete_candidate': message}, status=status.HTTP_400_BAD_REQUEST)
    
    try:
        item = Candidate.objects.get(id=id)
    except:
        message = 'Candidato não encontrado'
        return Response({'status': status.HTTP_404_NOT_FOUND, 'delete_candidate': message}, status=status.HTTP_404_NOT_FOUND)

    try:
        item.delete()
    except:
        message = 'Candidato não pode ser apagado, existem processos seletivos nos quais ele se encontra cadastrado.'
        return Response({'status': status.HTTP_428_PRECONDITION_REQUIRED, 'delete_candidate': message}, status=status.HTTP_428_PRECONDITION_REQUIRED)
    
    
    return Response({'status': status.HTTP_200_OK, 'delete_candidate': {"id": id, "name": item.name}}, status=status.HTTP_200_OK)


@api_view(['PUT'])
def updateCandidate(request):

    try:
        id = int(request.query_params.get('id'))
    except:
        message = 'Faltando parâmetro ID'
        return Response({'status': status.HTTP_400_BAD_REQUEST, 'update_candidate': message}, status=status.HTTP_400_BAD_REQUEST)
    
    try:
        item = Candidate.objects.get(id=id)
    except:
        message = 'Candidato não encontrada'
        return Response({'status': status.HTTP_404_NOT_FOUND, 'update_candidate': message}, status=status.HTTP_404_NOT_FOUND)

    data = request.data

    try:

        item.name = data['name']
        item.save()
        serializer = CandidateSerializer(item, many=False)
        
        return Response({'status': status.HTTP_200_OK, 'update_candidate': serializer.data}, status=status.HTTP_200_OK)

    except:
        message = 'Erro ao atualizar Candidato'
        return Response({'status': status.HTTP_404_NOT_FOUND, 'update_candidate': message}, status=status.HTTP_404_NOT_FOUND)