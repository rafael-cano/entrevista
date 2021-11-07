from rest_framework import serializers
from base.models import Candidate, Team, SelectionProcess, Contribution


class ContributionResultSerializer(serializers.ModelSerializer):
    name = serializers.SerializerMethodField(read_only=True)

    class Meta:

        model = Contribution
        fields = ['id','name', 'contribution']
    def to_representation(self, instance):
        representation = super(ContributionResultSerializer, self).to_representation(instance)

        representation['id'] = instance.candidate.id

        return representation
    
    def get_name(self, obj):
        return obj.candidate.name

class ContributionSerializer(serializers.ModelSerializer):
    candidate = serializers.ReadOnlyField(source='candidate.name')
    team = serializers.ReadOnlyField(source='team.name')
    class Meta:
        model = Contribution
        fields = ['candidate','team', 'contribution']
    def to_representation(self, instance):
        representation = super(ContributionSerializer, self).to_representation(instance)
        representation['team_id'] = instance.team.id
        representation['team'] = instance.team.name
        representation['candidate_id'] = instance.candidate.id
        representation['candidate'] = instance.candidate.name

        return representation


class CandidateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Candidate
        fields = '__all__'

class TeamSerializer(serializers.ModelSerializer):
    class Meta:
        model = Team
        fields = '__all__'

class SelectionProcessSerializer(serializers.ModelSerializer):
    candidates = ContributionSerializer(source='contribution_set', many=True, read_only=True)
    teams = TeamSerializer(many=True)
    class Meta:
        model = SelectionProcess
        fields = '__all__'


        