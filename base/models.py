from django.db import models


# Equipes, inicialmente somente Backend e Frontend, mas com espaço para escalabilidade, 
# por isso escolhi criar uma entidade equipe.
class Team(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255, unique=True)

    def __str__(self):
        return self.name

class Candidate(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255, unique=True)

    def __str__(self):
        return self.name

class SelectionProcess(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255, unique=True)
    teams = models.ManyToManyField(Team)
    candidates = models.ManyToManyField(Candidate, through='Contribution')

    def __str__(self):
        return self.name

# Contribuição é por colaborador para cada equipe e será por processo seletivo, 
# pois o mesmo colaborador pode participar de város processos seletivos e ter uma 
# nota de contribuição diferente em cada processo

class Contribution(models.Model):
    selectionProcess = models.ForeignKey(SelectionProcess, on_delete=models.CASCADE)
    team = models.ForeignKey(Team, on_delete=models.DO_NOTHING)
    candidate = models.ForeignKey(Candidate, on_delete=models.DO_NOTHING)
    contribution = models.IntegerField()
    class Meta:
        unique_together = ('selectionProcess', 'team', 'candidate')