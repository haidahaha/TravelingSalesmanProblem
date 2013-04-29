import abc

class GeneticAlgorithm:
    @abc.abstractmethod
    def performEvolution(self):
        pass

class GeneticAlgorithmProblem:

    @abc.abstractmethod
    def fitness(self, instance):
        pass

    @abc.abstractmethod
    def getPotentialGenes(self):
        pass

    @abc.abstractmethod
    def performEvolution(self):
        pass

    @abc.abstractmethod
    def selection(self):
        pass

    @abc.abstractmethod
    def crossover(self):
        pass

    @abc.abstractmethod
    def mutation(self):
        pass

class GeneticAlgorithmInstance:

    phenotype = 0;
    genotype = [];

    def getGenotype(self):
        return self.genotype

    def setPhenotype(self, phenotype):
        self.phenotype = phenotype

    def getPhenotype(self):
        return self.phenotype

    def setGenotype(self, genotype):
        self.genotype = genotype


