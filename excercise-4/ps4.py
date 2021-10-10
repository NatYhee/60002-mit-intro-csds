# Problem Set 4: Simulating the Spread of Disease and Bacteria Population Dynamics
# Name:
# Collaborators (Discussion):
# Time:

import math
import numpy as np
import pylab as pl
import random
import copy

#setting seed for debugging
random.seed(0)

##########################
# End helper code
##########################

class NoChildException(Exception):
    """
    NoChildException is raised by the reproduce() method in the SimpleBacteria
    and ResistantBacteria classes to indicate that a bacteria cell does not
    reproduce. You should use NoChildException as is; you do not need to
    modify it or add any code.
    """


def make_one_curve_plot(x_coords, y_coords, x_label, y_label, title):
    """
    Makes a plot of the x coordinates and the y coordinates with the labels
    and title provided.

    Args:
        x_coords (list of floats): x coordinates to graph
        y_coords (list of floats): y coordinates to graph
        x_label (str): label for the x-axis
        y_label (str): label for the y-axis
        title (str): title for the graph
    """
    pl.figure()
    pl.plot(x_coords, y_coords)
    pl.xlabel(x_label)
    pl.ylabel(y_label)
    pl.title(title)
    pl.show()


def make_two_curve_plot(x_coords,
                        y_coords1,
                        y_coords2,
                        y_name1,
                        y_name2,
                        x_label,
                        y_label,
                        title):
    """
    Makes a plot with two curves on it, based on the x coordinates with each of
    the set of y coordinates provided.

    Args:
        x_coords (list of floats): the x coordinates to graph
        y_coords1 (list of floats): the first set of y coordinates to graph
        y_coords2 (list of floats): the second set of y-coordinates to graph
        y_name1 (str): name describing the first y-coordinates line
        y_name2 (str): name describing the second y-coordinates line
        x_label (str): label for the x-axis
        y_label (str): label for the y-axis
        title (str): the title of the graph
    """
    pl.figure()
    pl.plot(x_coords, y_coords1, label=y_name1)
    pl.plot(x_coords, y_coords2, label=y_name2)
    pl.legend()
    pl.xlabel(x_label)
    pl.ylabel(y_label)
    pl.title(title)
    pl.show()

def execute_two_curve_plot(ls_y1:list, ls_y2:list):
    num_step = len(ls_y1[0])
    x_axis = [i for i in range(num_step)]

    ls_avg_y1 = [calc_pop_avg(populations=ls_y1, n=index) for index in range(num_step)]
    ls_avg_y2 = [calc_pop_avg(populations=ls_y2, n=index) for index in range(num_step)]

    make_two_curve_plot(x_coords=x_axis,
                        y_coords1=ls_avg_y1,
                        y_coords2=ls_avg_y2,
                        y_name1="avg bacteria pop",
                        y_name2="avg resit bacteria pop",
                        x_label="steps",
                        y_label="population",
                        title="resistant bacteria")


##########################
# PROBLEM 1
##########################

class SimpleBacteria(object):
    """A simple bacteria cell with no antibiotic resistance"""

    def __init__(self, birth_prob:float, death_prob:float) -> None:
        """
        Args:
            birth_prob (float in [0, 1]): Maximum possible reproduction
                probability
            death_prob (float in [0, 1]): Maximum death probability
        """
        self._birth_prob = birth_prob #treated as threshold for reproduction
        self._death_prob = death_prob #treated as threshold for death

    def is_killed(self):
        """
        Stochastically determines whether this bacteria cell is killed in
        the patient's body at a time step, i.e. the bacteria cell dies with
        some probability equal to the death probability each time step.

        Returns:
            bool: True with probability self.death_prob, False otherwise.
        """
        survive_prob = random.random()
        return survive_prob <= self._death_prob

    def reproduce(self, pop_density:float) -> object:
        """
        Stochastically determines whether this bacteria cell reproduces at a
        time step. Called by the update() method in the Patient and
        TreatedPatient classes.

        The bacteria cell reproduces with probability
        self.birth_prob * (1 - pop_density).

        If this bacteria cell reproduces, then reproduce() creates and returns
        the instance of the offspring SimpleBacteria (which has the same
        birth_prob and death_prob values as its parent).

        Args:
            pop_density (float): The population density, defined as the
                current bacteria population divided by the maximum population

        Returns:
            SimpleBacteria: A new instance representing the offspring of
                this bacteria cell (if the bacteria reproduces). The child
                should have the same birth_prob and death_prob values as
                this bacteria.

        Raises:
            NoChildException if this bacteria cell does not reproduce.
        """
        offspring_prob = random.random()

        if offspring_prob <= self._birth_prob*(1 - pop_density):
            return SimpleBacteria(birth_prob=self._birth_prob, death_prob=self._death_prob)
        else:
            raise NoChildException()


class Patient(object):
    """
    Representation of a simplified patient. The patient does not take any
    antibiotics and his/her bacteria populations have no antibiotic resistance.
    """
    def __init__(self, bacteria:list, max_pop:int) -> None:
        """
        Args:
            bacteria (list of SimpleBacteria): The bacteria in the population
            max_pop (int): Maximum possible bacteria population size for
                this patient
        """
        self._bacteria = bacteria
        self._max_pop = max_pop

    def get_total_pop(self) -> int:
        """
        Gets the size of the current total bacteria population.

        Returns:
            int: The total bacteria population
        """
        return int(len(self._bacteria))

    def update(self) -> int:
        """
        Update the state of the bacteria population in this patient for a
        single time step. update() should execute the following steps in
        this order:

        1. Determine whether each bacteria cell dies (according to the
           is_killed method) and create a new list of surviving bacteria cells.

        2. Calculate the current population density by dividing the surviving
           bacteria population by the maximum population. This population
           density value is used for the following steps until the next call
           to update()

        3. Based on the population density, determine whether each surviving
           bacteria cell should reproduce and add offspring bacteria cells to
           a list of bacteria in this patient. New offspring do not reproduce.

           Note: New offspring do not reproduce.

        4. Reassign the patient's bacteria list to be the list of surviving
           bacteria and new offspring bacteria

        Returns:
            int: The total bacteria population at the end of the update
        """
        ls_survived_bacteria = [bacteria for bacteria in self._bacteria if not bacteria.is_killed()]
        population_density = float(len(ls_survived_bacteria)/self._max_pop)

        #ls_all_bacteria = survived bacteria and new offspring bacteria
        ls_all_bacteria = copy.deepcopy(ls_survived_bacteria)

        #Finind that which bacteria cell giving an offspring
        for bacteria in ls_survived_bacteria:
            try:
                offspring = bacteria.reproduce(pop_density=population_density)
                ls_all_bacteria.append(offspring)
            except NoChildException:
                pass
        
        self._bacteria = ls_all_bacteria
        return self.get_total_pop()


##########################
# PROBLEM 2
##########################

def calc_pop_avg(populations:list, n:int) -> float:
    """
    Finds the average bacteria population size across trials at time step n

    Args:
        populations (list of lists or 2D array): populations[i][j] is the
            number of bacteria in trial i at time step j

    Returns:
        float: The average bacteria population size at time step n
    """
    total_sum = float(0)

    for population in populations:
        total_sum += float(population[n])
    
    return total_sum/len(populations)


def simulation_without_antibiotic(num_bacteria:int,
                                  max_pop:int,
                                  birth_prob:float,
                                  death_prob:float,
                                  num_trials:int) -> list:
    """
    Run the simulation and plot the graph for problem 2. No antibiotics
    are used, and bacteria do not have any antibiotic resistance.

    For each of num_trials trials:
        * instantiate a list of SimpleBacteria
        * instantiate a Patient using the list of SimpleBacteria
        * simulate changes to the bacteria population for 300 timesteps,
          recording the bacteria population after each time step. Note
          that the first time step should contain the starting number of
          bacteria in the patient
    note: timesteps is exclicitly declared to be 300

    Then, plot the average bacteria population size (y-axis) as a function of
    elapsed time steps (x-axis) You might find the make_one_curve_plot
    function useful.

    Args:
        num_bacteria (int): number of SimpleBacteria to create for patient
        max_pop (int): maximum bacteria population for patient
        birth_prob (float in [0, 1]): maximum reproduction
            probability
        death_prob (float in [0, 1]): maximum death probability
        num_trials (int): number of simulation runs to execute

    Returns:
        populations (list of lists or 2D array): populations[i][j] is the
            number of bacteria in trial i at time step j
    """
    timesteps = 300
    ls_population = []

    for _ in range(num_trials):
        ls_population_trial = []
        ls_bacteria = [SimpleBacteria(birth_prob=birth_prob, death_prob=death_prob) for _ in range(num_bacteria)]
        patient = Patient(bacteria=ls_bacteria, max_pop=max_pop)

        for step in range(timesteps + 1):

            if step == 0:
                ls_population_trial.append(num_bacteria)
            else:
                ls_population_trial.append(patient.update())

        ls_population.append(ls_population_trial)
    
    return ls_population

# When you are ready to run the simulation, uncomment the next line
# populations = simulation_without_antibiotic(100, 1000, 0.1, 0.025, 50)

# avg_populations = [calc_pop_avg(populations=populations,n=index) for index in range(len(populations[0]))]
# x_axis = [i for i in range(len(avg_populations))]
# make_one_curve_plot(x_coords=x_axis, y_coords=avg_populations, x_label="number of steps", y_label="average population", title="SimpleBacteria Populations")

##########################
# PROBLEM 3
##########################

#adding function mean
def calc_pop_std(populations:list, t:int) -> float:
    """
    Finds the standard deviation of populations across different trials
    at time step t by:
        * calculating the average population at time step t
        * compute average squared distance of the data points from the average
          and take its square root

    You may not use third-party functions that calculate standard deviation,
    such as numpy.std. Other built-in or third-party functions that do not
    calculate standard deviation may be used.

    Args:
        populations (list of lists or 2D array): populations[i][j] is the
            number of bacteria present in trial i at time step j
        t (int): time step

    Returns:
        float: the standard deviation of populations across different trials at
             a specific time step
    """
    #prepare example
    population_t = [population[t] for population in populations]
    n_sample = len(population_t)

    #calculate mean
    expected_t = float(sum(population_t)/n_sample)
    
    #calculate standard deviation
    var = 0
    for sample in population_t:
        var += 1/(n_sample)*((sample - expected_t)**2)
    
    std = float(var**(1/2))
    return std


def calc_95_ci(populations:list, t:int) -> tuple:
    """
    Finds a 95% confidence interval around the average bacteria population
    at time t by:
        * computing the mean and standard deviation of the sample
        * using the standard deviation of the sample to estimate the
          standard error of the mean (SEM)
        * using the SEM to construct confidence intervals around the
          sample mean

    Args:
        populations (list of lists or 2D array): populations[i][j] is the
            number of bacteria present in trial i at time step j
        t (int): time step

    Returns:
        mean (float): the sample mean
        width (float): 1.96 * SEM

        I.e., you should return a tuple containing (mean, width)
    """
    std = calc_pop_std(populations=populations, t=t)
    std_error = std/(len(populations)**(1/2))
    width = std_error*1.96

    #prepare example
    population_t = [population[t] for population in populations]
    n_sample = len(population_t)

    #calculate mean
    expected_t = float(sum(population_t)/n_sample)
    return (expected_t, width)

##########################
# PROBLEM 4
##########################

class ResistantBacteria(SimpleBacteria):
    """A bacteria cell that can have antibiotic resistance."""

    def __init__(self, birth_prob:float, death_prob:float, resistant:bool, mut_prob:float):
        """
        Args:
            birth_prob (float in [0, 1]): reproduction probability
            death_prob (float in [0, 1]): death probability
            resistant (bool): whether this bacteria has antibiotic resistance
            mut_prob (float): mutation probability for this
                bacteria cell. This is the maximum probability of the
                offspring acquiring antibiotic resistance
        """
        SimpleBacteria.__init__(self, birth_prob, death_prob)
        self._resistant = resistant
        self._mut_prob = mut_prob


    def get_resistant(self) -> bool:
        """Returns whether the bacteria has antibiotic resistance"""
        return self._resistant

    def is_killed(self) -> bool:
        """Stochastically determines whether this bacteria cell is killed in
        the patient's body at a given time step.

        Checks whether the bacteria has antibiotic resistance. If resistant,
        the bacteria dies with the regular death probability. If not resistant,
        the bacteria dies with the regular death probability / 4.

        Returns:
            bool: True if the bacteria dies with the appropriate probability
                and False otherwise.
        """
        if self._resistant:
            death_prob = self._death_prob
        elif not self._resistant:
            death_prob = self._death_prob/4
        
        survive_prob = random.random()
        return survive_prob <= death_prob


    def reproduce(self, pop_density:float) -> object:
        """
        Stochastically determines whether this bacteria cell reproduces at a
        time step. Called by the update() method in the TreatedPatient class.

        A surviving bacteria cell will reproduce with probability:
        self.birth_prob * (1 - pop_density).

        If the bacteria cell reproduces, then reproduce() creates and returns
        an instance of the offspring ResistantBacteria, which will have the
        same birth_prob, death_prob, and mut_prob values as its parent.

        If the bacteria has antibiotic resistance, the offspring will also be
        resistant. If the bacteria does not have antibiotic resistance, its
        offspring have a probability of self.mut_prob * (1-pop_density) of
        developing that resistance trait. That is, bacteria in less densely
        populated environments have a greater chance of mutating to have
        antibiotic resistance.

        Args:
            pop_density (float): the population density

        Returns:
            ResistantBacteria: an instance representing the offspring of
            this bacteria cell (if the bacteria reproduces). The child should
            have the same birth_prob, death_prob values and mut_prob
            as this bacteria. Otherwise, raises a NoChildException if this
            bacteria cell does not reproduce.
        """
        offspring_prob = random.random()
        is_reproduce = (offspring_prob <= self._birth_prob*(1 - pop_density))

        if is_reproduce and self._resistant:
            return ResistantBacteria(birth_prob=self._birth_prob,\
                                        death_prob=self._death_prob,\
                                        resistant=self._resistant,\
                                        mut_prob=self._mut_prob)

        elif is_reproduce and not self._resistant:
            is_mutate = self._is_mutate(pop_density=pop_density)
            if is_mutate:
                return ResistantBacteria(birth_prob=self._birth_prob,\
                                        death_prob=self._death_prob,\
                                        resistant=True,\
                                        mut_prob=self._mut_prob)
            elif not is_mutate:
                return ResistantBacteria(birth_prob=self._birth_prob,\
                        death_prob=self._death_prob,\
                        resistant=False,\
                        mut_prob=self._mut_prob)
        
        else:
            raise NoChildException()
    
    def _is_mutate(self, pop_density:float) -> bool:
        mutate_prob = random.random()
        return mutate_prob <= self._mut_prob * (1-pop_density) 


class TreatedPatient(Patient):
    """
    Representation of a treated patient. The patient is able to take an
    antibiotic and his/her bacteria population can acquire antibiotic
    resistance. The patient cannot go off an antibiotic once on it.
    """
    def __init__(self, bacteria:list, max_pop:int) -> None:
        """
        Args:
            bacteria: The list representing the bacteria population (a list of
                      bacteria instances)
            max_pop: The maximum bacteria population for this patient (int)

        This function should initialize self.on_antibiotic, which represents
        whether a patient has been given an antibiotic. Initially, the
        patient has not been given an antibiotic.

        Don't forget to call Patient's __init__ method at the start of this
        method.
        """
        Patient.__init__(self, bacteria=bacteria, max_pop=max_pop)
        self._on_antibiotic = False

    def set_on_antibiotic(self) -> None:
        """
        Administer an antibiotic to this patient. The antibiotic acts on the
        bacteria population for all subsequent time steps.
        """
        self._on_antibiotic = True

    def get_resist_pop(self) -> int:
        """
        Get the population size of bacteria cells with antibiotic resistance

        Returns:
            int: the number of bacteria with antibiotic resistance
        """
        resist_pop = 0

        for bacteria in self._bacteria:
            if bacteria.get_resistant():
                resist_pop += 1

        return resist_pop

    def update(self) -> int:
        """
        Update the state of the bacteria population in this patient for a
        single time step. update() should execute these actions in order:

        1. Determine whether each bacteria cell dies (according to the
           is_killed method) and create a new list of surviving bacteria cells.

        2. If the patient is on antibiotics, the surviving bacteria cells from
           (1) only survive further if they are resistant. If the patient is
           not on the antibiotic, keep all surviving bacteria cells from (1)

        3. Calculate the current population density. This value is used until
           the next call to update(). Use the same calculation as in Patient

        4. Based on this value of population density, determine whether each
           surviving bacteria cell should reproduce and add offspring bacteria
           cells to the list of bacteria in this patient.

        5. Reassign the patient's bacteria list to be the list of survived
           bacteria and new offspring bacteria

        Returns:
            int: The total bacteria population at the end of the update
        """
        #step 1
        ls_survived_bacteria_wip = [bacteria for bacteria in self._bacteria if not bacteria.is_killed()]

        #step 2
        if self._on_antibiotic:
            ls_survived_bacteria = [bacteria for bacteria in ls_survived_bacteria_wip if bacteria.get_resistant()]
        else:
            ls_survived_bacteria = ls_survived_bacteria_wip
        
        #step 3
        population_density = float(len(ls_survived_bacteria)/self._max_pop)

        #step 4
        ls_all_bacteria = copy.deepcopy(ls_survived_bacteria)

        for bacteria in ls_survived_bacteria:
            try:
                offspring = bacteria.reproduce(pop_density=population_density)
                ls_all_bacteria.append(offspring)
            except NoChildException:
                pass
        
        #step 5
        self._bacteria = ls_all_bacteria
        return self.get_total_pop()


##########################
# PROBLEM 5
##########################

def get_tot_resist_pop(ls_bacteria):
    tt_resist_pop = 0
    for bacteria in ls_bacteria:
        if bacteria.get_resistant():
            tt_resist_pop += 1
    return tt_resist_pop


def simulation_with_antibiotic(num_bacteria:int,
                               max_pop:int,
                               birth_prob:float,
                               death_prob:float,
                               resistant:float,
                               mut_prob:float,
                               num_trials:int):
    """
    Runs simulations and plots graphs for problem 4.

    For each of num_trials trials:
        * instantiate a list of ResistantBacteria
        * instantiate a patient
        * run a simulation for 150 timesteps, add the antibiotic, and run the
          simulation for an additional 250 timesteps, recording the total
          bacteria population and the resistance bacteria population after
          each time step
    note: 150 timesteps for non antibiotic and 250 timesteps for having antibiotic

    Plot the average bacteria population size for both the total bacteria
    population and the antibiotic-resistant bacteria population (y-axis) as a
    function of elapsed time steps (x-axis) on the same plot. You might find
    the helper function make_two_curve_plot helpful

    Args:
        num_bacteria (int): number of ResistantBacteria to create for
            the patient
        max_pop (int): maximum bacteria population for patient
        birth_prob (float int [0-1]): reproduction probability
        death_prob (float in [0, 1]): probability of a bacteria cell dying
        resistant (bool): whether the bacteria initially have
            antibiotic resistance
        mut_prob (float in [0, 1]): mutation probability for the
            ResistantBacteria cells
        num_trials (int): number of simulation runs to execute

    Returns: a tuple of two lists of lists, or two 2D arrays
        populations (list of lists or 2D array): the total number of bacteria
            at each time step for each trial; total_population[i][j] is the
            total population for trial i at time step j
        resistant_pop (list of lists or 2D array): the total number of
            resistant bacteria at each time step for each trial;
            resistant_pop[i][j] is the number of resistant bacteria for
            trial i at time step j
    """
    timestep_no_antibiotic = 150
    timestep_antibiotic = 250
    timesteps = timestep_no_antibiotic + timestep_antibiotic

    ls_population = []
    ls_resist = []

    for _ in range(num_trials):
        ls_population_trial = []
        ls_resist_trail = []

        ls_bacteria = [ResistantBacteria(birth_prob, death_prob, resistant, mut_prob) for _ in range(num_bacteria)]
        patient = TreatedPatient(bacteria=ls_bacteria, max_pop=max_pop)

        for step in range(timesteps + 1):

            if step == 0:
                ls_population_trial.append(len(ls_bacteria))
                ls_resist_trail.append(get_tot_resist_pop(ls_bacteria))
            
            #has not antibiotic is set as False default
            elif step <= timestep_no_antibiotic:
                ls_population_trial.append(patient.update())
                ls_resist_trail.append(patient.get_resist_pop())
            
            elif step > timestep_no_antibiotic:
                patient.set_on_antibiotic()
                ls_population_trial.append(patient.update())
                ls_resist_trail.append(patient.get_resist_pop())

        ls_population.append(ls_population_trial)
        ls_resist.append(ls_resist_trail)
    
    return (ls_population, ls_resist)


# When you are ready to run the simulations, uncomment the next lines one
# at a time
total_pop, resistant_pop = simulation_with_antibiotic(num_bacteria=100,
                                                      max_pop=1000,
                                                      birth_prob=0.3,
                                                      death_prob=0.2,
                                                      resistant=False,
                                                      mut_prob=0.8,
                                                      num_trials=50)

execute_two_curve_plot(total_pop, resistant_pop)
# total_pop, resistant_pop = simulation_with_antibiotic(num_bacteria=100,
#                                                       max_pop=1000,
#                                                       birth_prob=0.17,
#                                                       death_prob=0.2,
#                                                       resistant=False,
#                                                       mut_prob=0.8,
#                                                       num_trials=50)
