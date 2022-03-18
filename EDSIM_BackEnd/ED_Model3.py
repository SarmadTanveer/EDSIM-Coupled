# imports below
import simpy
import random
from EDSIM_BackEnd.ED_Patient import Patient, ambulancePatient, walkInPatient
from functools import partial
from EDSIM_BackEnd.Reource_monitor import patch_resource, monitor
import pandas as pd


class Writer:

    def ConvertToDataFrame(runList):
        patientData = pd.DataFrame(runList)
        print(patientData)
        print(patientData.columns)
        print(patientData.shape)
        print(patientData.dtypes)
        print(patientData.describe())
        return patientData

    def writeToCsv(patientData, name):
        patientData.to_csv(name, index=False)

# start of global class Data
# It organizes all the parameters
class Data:
    def __init__(self, simParameters):
        # resource capacities
        self.doctorCap = simParameters['resCapacity']['doctor']
        self.nurseCap = simParameters['resCapacity']['nurse']
        self.bedCap = simParameters['resCapacity']['beds']
        self.rBedCap = simParameters['resCapacity']['rBeds']

        # interarrival times
        self.pInterAmbulance = simParameters['pInterArrival']['ambulance']
        self.pInterWalkIn = simParameters['pInterArrival']['walkIn']

        # service times
        self.priorAssessment = simParameters['serTimes']['priorAssessment']
        self.bedAssignment = simParameters['serTimes']['bedAssignment']
        self.ctasAssessment = simParameters['serTimes']['ctasAssessment']
        self.discharge = simParameters['serTimes']['discharge']
        self.initialAssessment = simParameters['serTimes']['initialAssessment']
        self.registration = simParameters['serTimes']['registration']
        self.treatment = simParameters['serTimes']['treatment']
        self.resuscitation = simParameters['serTimes']['resuscitation']

        # standard deviations
        self.priorAssessment_std_dev = simParameters['stdDeviations']['priorAssessment_Deviation']
        self.bedAssignment_std_dev = simParameters['stdDeviations']['bedAssignment_Deviation']
        self.ctasAssessment_std_dev = simParameters['stdDeviations']['ctasAssessment_Deviation']
        self.discharge_std_dev = simParameters['stdDeviations']['discharge_Deviation']
        self.initialAssessment_std_dev = simParameters['stdDeviations']['initialAssessment_Deviation']
        self.registration_std_dev = simParameters['stdDeviations']['registration_Deviation']
        self.treatment_std_dev = simParameters['stdDeviations']['treatment_Deviation']
        self.resuscitation_std_dev = simParameters['stdDeviations']['resuscitation_Deviation']

        # ctas distribution - ambulance
        self.ambulanceCtas = simParameters['ctasDist']['ambulance']

        # ctas distribution - walkin
        self.walkInCtas = simParameters['ctasDist']['walkIn']

        # Number of iterations
        self.iterations = simParameters['iter']

        # Warm up Period
        self.warmUp = simParameters['warmUp']

        # Length of Sim
        self.length = simParameters['length']

# start of model class
class EDModel:

    def __init__(self, parameters):
        # create enviroment
        self.env = simpy.Environment()

        # priority levels
        self.highPrio = 1
        self.medPrio = 2
        self.lowPrio = 3

        # set up resources
        self.nurse = simpy.PriorityResource(self.env, capacity=parameters.nurseCap)
        self.doctor = simpy.PriorityResource(self.env, capacity=parameters.doctorCap)
        self.regular_beds = simpy.PriorityResource(self.env, capacity=parameters.bedCap)
        self.resuscitation_beds = simpy.PriorityResource(self.env, capacity=parameters.rBedCap)

        # initial parameters
        self.parameters = parameters

        # list of patients during this run
        self.patientList = []
        self.resourceMonitor = []
        self.resuscitationBedWait = []

        # create a variable that creates true random values
        # use this instead of random.
        # example trng.expovariate instead of random.expovariate
        self.trueRandom = random.SystemRandom()

    # this generates patients that walked in the ED
    def generate_walk_in_arrivals(self):
        # while length is bigger than the simulation time, generate more patients
        while self.parameters.length >= self.env.now:

            # create walk-in patient (wp)
            # when patient is created is when he arrives
            wp = walkInPatient(ctas_dist=self.parameters.walkInCtas)

            # after patient is created he enters the ED after some time
            self.env.process(self.emergency_department_process(wp))

            # interarrival time for walk-In patients
            interarrival_for_walkIn = self.trueRandom.expovariate(1.0 / self.parameters.pInterWalkIn)
            # after the patient is created we wait some time and create another one
            yield self.env.timeout(interarrival_for_walkIn)

    # this generates patients that arrived by ambulance in the ed
    def generate_ambulance_arrivals(self):
        # while length is bigger than the simulation time, generate more patients
        while self.parameters.length >= self.env.now:
            # create ambulance patient (ab)
            # when patient is created is when he arrives
            ap = ambulancePatient(ctas_dist=self.parameters.ambulanceCtas)

            # after patient is created he enters the ED after some time
            self.env.process(self.emergency_department_process(ap))  # -> problem here

            # interarrival time for ambulance patients
            interarrival_for_ambulance = self.trueRandom.expovariate(1.0 / self.parameters.pInterAmbulance)
            # after the patient is created we wait some time and create another one
            yield self.env.timeout(interarrival_for_ambulance)

    # Cover from priority assessment to bed assigment
    def emergency_department_process(self, patient):

        # Take the arrival time here because all patients pass through here so it is easier
        patient.arrival_time = self.env.now

        # walk in patient goes through priority assessment
        if isinstance(patient, walkInPatient):

            yield self.env.process(self.priority_assessment(patient))

        # three pathways for ambulance patient
        elif isinstance(patient, ambulancePatient):
            # patient requires resuscitation
            if patient.CTAS_Level == 1:
                yield self.env.process(self.resuscitation(patient))

            # patient is not severe but requires immediate care CTAS 2
            elif patient.CTAS_Level == 2:
                yield self.env.process(self.bed_assignment(patient))

            # patient is not severe and can proceed normally through the ed 3,4 and 5
            else:
                yield self.env.process(self.ctas_assessment(patient))

                # Priority assessment Code red or blue

    def priority_assessment(self, patient):
        # patient enters queue

        with self.nurse.request(priority=self.highPrio) as req:
            # wait till nurse is available
            yield req

            # this is how long the patient waited for the nurse
            patient.priority_assessment_time = self.env.now  # do we really need a set function?

            # nurse takes time to assess
            sampled_service_time = self.trueRandom.gauss(self.parameters.priorAssessment, self.parameters.priorAssessment_std_dev)
            sampled_service_time = abs(sampled_service_time)

            yield self.env.timeout(sampled_service_time)

        patient.priority_assessment_time_end = self.env.now

        if patient.CTAS_Level == 1:
            # add patient to resuscitation queue
            self.env.process(self.resuscitation(patient))

        elif patient.CTAS_Level == 2:
            # add patienti to bed assignment queue
            self.env.process(self.bed_assignment(patient))
        else:
            # add patient to ctas queue
            self.env.process(self.ctas_assessment(patient))

    # after priority assessment patient gets ctas assessed
    def ctas_assessment(self, patient):
        # patient enters queue
        patient.ctas_assessment_time_arrival = self.env.now

        # request a nurse
        with self.nurse.request(priority=patient.CTAS_Level) as req:
            # wait until a nurse is avaiable then lock the nurse and continue to the emergency_department_process
            yield req

            # this is how long the patient waited for the nurse
            patient.ctas_assessment_time = self.env.now

            # sampled_xxxx_duration is getting a random value from the mean and then
            # is going to wait that time until it concluded and with that releases the nurse
            sampled_service_time = self.trueRandom.gauss(self.parameters.ctasAssessment, self.parameters.ctasAssessment_std_dev)
            sampled_service_time = abs(sampled_service_time)

            yield self.env.timeout(sampled_service_time)

        patient.ctas_assessment_time_end = self.env.now

        # add patient to registration queue i.e waiting area 1
        self.env.process(self.registration(patient))

    def registration(self, patient):
        # patient enters queue
        patient.registration_time_arrival = self.env.now

        # request a nurse
        with self.nurse.request(priority=patient.CTAS_Level) as req:
            # wait until a nurse is avaiable then lock the nurse and continue to the emergency_department_process
            yield req

            # this is how long the patient waited for the nurse
            patient.registration_time = self.env.now

            # sampled_xxxx_duration is getting a random value from the mean and then
            # is going to wait that time until it concluded and with that releases the nurse
            sampled_service_time = self.trueRandom.gauss(self.parameters.registration, self.parameters.registration_std_dev)
            sampled_service_time = abs(sampled_service_time)

            yield self.env.timeout(sampled_service_time)

        patient.registration_time_end = self.env.now

        # add patient to bed assignment queue i.e waiting area 2
        self.env.process(self.bed_assignment(patient))

    def bed_assignment(self, patient):
        # patient enters queue
        patient.bed_assignment_time_arrival = self.env.now

        bed_request = self.regular_beds.request(priority=patient.CTAS_Level)
        yield bed_request

        patient.bed = bed_request  # bed is available and has been locked

        # resource queueing time: regular bed
        patient.bed_assignment_acquired = self.env.now

        # request a nurse
        with self.nurse.request(priority=patient.CTAS_Level) as req:
            # wait until a nurse and bed is avaiable then lock both
            yield req

            # nurse is available
            patient.bed_assignment_time = self.env.now

            # sampled_xxxx_duration is getting a random value from the mean and then
            # is going to wait that time until it concluded and with that releases the nurse but not bed
            sampled_service_time = self.trueRandom.gauss(self.parameters.bedAssignment, self.parameters.bedAssignment_std_dev)
            sampled_service_time = abs(sampled_service_time)

            yield self.env.timeout(sampled_service_time)

        patient.bed_assignment_time_end = self.env.now

        self.env.process(self.initial_assessment(patient))

    # have to modify this
    def resuscitation(self, patient):
        patient.resuscitation_time_arrival = self.env.now

        with self.resuscitation_beds.request(priority=0) as req:
            yield req

            # resuscitation bed acquired
            patient.resuscitation_bed_acquired = self.env.now

            with self.nurse.request(priority=0) as req1:
                # wait until a nurse and doctor is avaiable
                yield req1

                with self.doctor.request(priority=0) as req2:
                    yield req2

                    patient.resuscitation_time = self.env.now

                    # sampled_xxxx_duration is getting a random value from the mean and then
                    # is going to wait that time until it concluded and with that releases the nurse, doctor and bed
                    sampled_service_time = self.trueRandom.gauss(self.parameters.resuscitation, self.parameters.resuscitation_std_dev)
                    sampled_service_time = abs(sampled_service_time)

                    yield self.env.timeout(sampled_service_time)

        patient.resuscitation_time_end = self.env.now

        # resuscitation will encompass bed assignment, initial assessment and treatment for CTAS level 1
        # after is complete go to discharge decision
        self.env.process(self.discharge_decision(patient))

    # Initial Assessment:
    def initial_assessment(self, patient):
        patient.initial_assessment_time_arrival = self.env.now

        with self.doctor.request(priority=patient.CTAS_Level) as req:
            # wait for doctor
            yield req

            patient.initial_assessment_time = self.env.now

            sampled_service_time = self.trueRandom.gauss(self.parameters.initialAssessment, self.parameters.initialAssessment_std_dev)
            sampled_service_time = abs(sampled_service_time)

            yield self.env.timeout(sampled_service_time)

        patient.initial_assessment_time_end = self.env.now

        self.env.process(self.treatment(patient))

    # Treatment:
    def treatment(self, patient):
        patient.treatment_time_arrival = self.env.now

        with self.nurse.request(priority=patient.CTAS_Level) as req:
            # wait until a nurse is available
            yield req

        with self.doctor.request(priority=patient.CTAS_Level) as req:
            # wait until a doctor is available
            yield req

            patient.treatment_time = self.env.now

            # sampled_xxxx_duration is getting a random value from the mean and then
            # is going to wait that time until it concluded and with that releases the nurse and doctor
            sampled_service_time = self.trueRandom.gauss(self.parameters.treatment, self.parameters.treatment_std_dev)
            sampled_service_time = abs(sampled_service_time)

            yield self.env.timeout(sampled_service_time)

        patient.treatment_time_end = self.env.now

        self.env.process(self.discharge_decision(patient))

    # Discharge Decision
    def discharge_decision(self, patient):
        patient.discharge_decision_time_arrival = self.env.now

        sampled_service_time = self.trueRandom.gauss(self.parameters.discharge, self.parameters.discharge_std_dev)
        sampled_service_time = abs(sampled_service_time)

        yield self.env.timeout(sampled_service_time)

        if patient.CTAS_Level != 1:
            self.regular_beds.release(patient.bed)

        patient.discharge_decision_time_leaving = self.env.now
        patient.calculate_Times()  # calculcate the patient queue times

        self.patientList.append(patient.convertToDict())

    def snapshot(self):
        while self.env.peek() < (self.parameters.length + self.parameters.warmUp):
            self.resourceMonitor.append({'Time Stamp': self.env.now,
                                         'Nurse Queue Length': len(self.nurse.queue),
                                         'Doctor Queue Length': len(self.doctor.queue),
                                         'Regular Bed Queue Length': len(self.regular_beds.queue),
                                         'Resuscitation Bed Queue Length': len(self.resuscitation_beds.queue)
                                         })
            yield self.env.timeout(5)

    def run(self):

        self.env.process(self.generate_walk_in_arrivals())
        self.env.process(self.generate_ambulance_arrivals())
        self.env.process(self.snapshot())
        self.env.run()
        return (self.patientList, self.resourceMonitor)


def runSim(simParameters):
    print("called runsim")
    print(simParameters)
    parameters = Data(simParameters)
    runList = []
    timeSeries = []

    for run in range(parameters.iterations):
        #print('--------------------------------------------------------------------------------')
        #print("Run ", run + 1, " of ", parameters.iterations, sep="")
        ed_model = EDModel(parameters)
        patientList, timeList = ed_model.run()
        runList.extend(patientList)
        timeSeries.extend(timeList)

        # print(runList)
        Patient.p_id = 0
        Patient.run_id += 1
        #print('--------------------------------------------------------------------------------')
        # ed model.run(until=parameters.length)

    Patient.run_id = 1
    #print(timeSeries)
    df = Writer.ConvertToDataFrame(runList=runList)
    df2 = Writer.ConvertToDataFrame(timeSeries)
    #print(df)
    return (df,df2)
