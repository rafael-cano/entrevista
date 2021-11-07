from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from base.models import Candidate, SelectionProcess, Contribution
from base.serializer import SelectionProcessSerializer, ContributionResultSerializer
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.conf import settings
from django.db.models import Max, Sum


@api_view(['GET'])
def getSelectionProcess(request):

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

    items = SelectionProcess.objects.filter(**filters)

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

    serializer = SelectionProcessSerializer(items, many=True)

    return Response({'status': status.HTTP_200_OK, 'list_selection_processs': serializer.data, 'page': page, 'pages': paginator.num_pages, 'filters': filtersResponse}, status=status.HTTP_200_OK)


@api_view(['GET'])
def getSelectionProcessDetails(request):

    try:
        id = int(request.query_params.get('id'))
    except:
        message = 'Faltando parâmetro ID'
        return Response({'status': status.HTTP_400_BAD_REQUEST, 'selection_process_details': message}, status=status.HTTP_400_BAD_REQUEST)

    try:
        item = SelectionProcess.objects.get(id=id)
    except:
        message = 'Processo seletivo não encontrado'
        return Response({'status': status.HTTP_404_NOT_FOUND, 'selection_process_details': message}, status=status.HTTP_404_NOT_FOUND)
    
    serializer = SelectionProcessSerializer(item, many=False)

    return Response({'status': status.HTTP_200_OK, 'selection_process_details': serializer.data}, status=status.HTTP_200_OK)

@api_view(['POST'])
def createSelectionProcess(request):
    
    data = request.data

    try:

        item = SelectionProcess.objects.create(
            name = data['name'],
        )
        item.teams.set(data['teams'])
        item.save()
        serializer = SelectionProcessSerializer(item, many=False)
        return Response({'status': status.HTTP_201_CREATED, 'create_selection_process': serializer.data}, status=status.HTTP_201_CREATED)
    
     
    except:
        message = 'Erro ao criar o processo seletivo. Verifique se o nome já existe.'
        return Response({'status': status.HTTP_404_NOT_FOUND, 'create_selection_process': message}, status=status.HTTP_404_NOT_FOUND)


@api_view(['DELETE'])
def deleteSelectionProcess(request):

    try:
        id = int(request.query_params.get('id'))
    except:
        message = 'Faltando parâmetro ID'
        return Response({'status': status.HTTP_400_BAD_REQUEST, 'delete_selection_process': message}, status=status.HTTP_400_BAD_REQUEST)
    
    try:
        item = SelectionProcess.objects.get(id=id)
    except:
        message = 'Processo seletivo não encontrado'
        return Response({'status': status.HTTP_404_NOT_FOUND, 'delete_selection_process': message}, status=status.HTTP_404_NOT_FOUND)

    try:
        item.delete()
    except:
        message = 'Processo seletivo não pode ser apagado, erro.'
        return Response({'status': status.HTTP_428_PRECONDITION_REQUIRED, 'delete_selection_process': message}, status=status.HTTP_428_PRECONDITION_REQUIRED)
    
    
    return Response({'status': status.HTTP_200_OK, 'delete_selection_process': {"id": id, "name": item.name}}, status=status.HTTP_200_OK)


@api_view(['PATCH'])
def updateSelectionProcess(request):

    try:
        id = int(request.query_params.get('id'))
    except:
        message = 'Faltando parâmetro ID'
        return Response({'status': status.HTTP_400_BAD_REQUEST, 'update_selection_process': message}, status=status.HTTP_400_BAD_REQUEST)

    
    try:
        item = SelectionProcess.objects.get(id=id)
    except:
        message = 'Processo seletivo não encontrado'
        return Response({'status': status.HTTP_404_NOT_FOUND, 'update_selection_process': message}, status=status.HTTP_404_NOT_FOUND)

    data = request.data

    try:

        item.name = data['name']
        item.teams.set(data['teams'])
        item.save()
        serializer = SelectionProcessSerializer(item, many=False)
        
        return Response({'status': status.HTTP_200_OK, 'update_selection_process': serializer.data}, status=status.HTTP_200_OK)

    except:
        message = 'Erro ao atualizar o processo seletivo'
        return Response({'status': status.HTTP_404_NOT_FOUND, 'update_selection_process': message}, status=status.HTTP_404_NOT_FOUND)


@api_view(['PATCH'])
def insertCandidate(request):

    try:
        id = int(request.query_params.get('id'))
    except:
        message = 'Faltando parâmetro ID'
        return Response({'status': status.HTTP_400_BAD_REQUEST, 'selection_process_insert_candidates': message}, status=status.HTTP_400_BAD_REQUEST)

    try:
        item = SelectionProcess.objects.get(id=id)
    except:
        message = 'Processo seletivo não encontrado'
        return Response({'status': status.HTTP_404_NOT_FOUND, 'selection_process_insert_candidates': message}, status=status.HTTP_404_NOT_FOUND)

    

    

    try:

        data = request.data
        
        Contribution.objects.create(
            selectionProcess = item,
            team_id = int(data['team_id']),
            candidate_id = int(data['candidate_id']),
            contribution = int(data['contribution']),
        )
        
    
    except:
        message = 'Erro ao atualizar o processo seletivo. Verifique se o candidato já não está cadastrado nesta equipe para esse processo seletivo.'
        return Response({'status': status.HTTP_404_NOT_FOUND, 'update_selection_process': message}, status=status.HTTP_404_NOT_FOUND)

    serializer = SelectionProcessSerializer(item, many=False)
        
    return Response({'status': status.HTTP_200_OK, 'selection_process_insert_candidates': serializer.data}, status=status.HTTP_200_OK)


@api_view(['PATCH'])
def removeCandidate(request):

    try:
        id = int(request.query_params.get('id'))
    except:
        message = 'Faltando parâmetro ID'
        return Response({'status': status.HTTP_400_BAD_REQUEST, 'selection_process_remove_candidates': message}, status=status.HTTP_400_BAD_REQUEST)

    try:
        item = SelectionProcess.objects.get(id=id)
    except:
        message = 'Processo seletivo não encontrado'
        return Response({'status': status.HTTP_404_NOT_FOUND, 'selection_process_remove_candidates': message}, status=status.HTTP_404_NOT_FOUND)

    data = request.data

    try:
        register = Contribution.objects.get(selectionProcess=item, team_id=int(data['team_id']), candidate_id = int(data['candidate_id']))
        register.delete()
    except:
        message = 'Erro'
        return Response({'status': status.HTTP_404_NOT_FOUND, 'selection_process_remove_candidates': message}, status=status.HTTP_404_NOT_FOUND)

    
    
    serializer = SelectionProcessSerializer(item, many=False)
        
    return Response({'status': status.HTTP_200_OK, 'selection_process_remove_candidates': serializer.data}, status=status.HTTP_200_OK)

@api_view(['GET'])
def getSelectionProcessResult(request):

    try:
        id = int(request.query_params.get('id'))
    except:
        message = 'Faltando parâmetro ID'
        return Response({'status': status.HTTP_400_BAD_REQUEST, 'approved_candidates': message}, status=status.HTTP_400_BAD_REQUEST)

    try:
        item = SelectionProcess.objects.get(id=id)
    except:
        message = 'Processo seletivo não encontrado'
        return Response({'status': status.HTTP_404_NOT_FOUND, 'approved_candidates': message}, status=status.HTTP_404_NOT_FOUND)

    data = {}

    contributionList = Contribution.objects.filter(selectionProcess_id=item.id)

    for team in item.teams.all():       
        
        contributionListTeam = contributionList.filter(team=team)
        
        contributionListTeamID = contributionListTeam.values('candidate_id')
        
        sumContributionList = contributionList.values('candidate_id').filter(candidate_id__in=contributionListTeamID).annotate(sum_contribution=Sum('contribution'))

        higherContribution = sumContributionList.aggregate(max_contribution=Max('sum_contribution'))['max_contribution']
        
        higherContributionIDs = sumContributionList.filter(sum_contribution=higherContribution).values('candidate_id')

        contributionListTeamAprroved = contributionListTeam.filter(candidate_id__in=higherContributionIDs)

        data[team.name]= ContributionResultSerializer(contributionListTeamAprroved, many=True).data


        
    return Response({'status': status.HTTP_200_OK, 'max_contribution': higherContribution,'approved_candidates': data}, status=status.HTTP_200_OK)

    





