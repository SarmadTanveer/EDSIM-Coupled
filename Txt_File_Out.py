
# need to pass the parameters
# when complete just uncomment and delete the test code
# the test is at the end of the program

class txt_file_out:

    def __init__(self, parameters):
        # average time (of all runs) for each CTAS level
        self.ctas_1_wait_time_avg = 1  # total wait time avg for ctas 1
        # self.ctas_1_wait_time_avg = parameters['avgWaitTime']['ctas_1']  # total wait time avg for ctas 1
        self.ctas_2_wait_time_avg = 2  # total wait time avg for ctas 2
        # self.ctas_2_wait_time_avg = parameters['avgWaitTime']['ctas_2']  # total wait time avg for ctas 2
        self.ctas_3_wait_time_avg = 3  # total wait time avg for ctas 3
        # self.ctas_3_wait_time_avg = parameters['avgWaitTime']['ctas_3']  # total wait time avg for ctas 3
        self.ctas_4_wait_time_avg = 4  # total wait time avg for ctas 4
        # self.ctas_4_wait_time_avg = parameters['avgWaitTime']['ctas_4']  # total wait time avg for ctas 4
        self.ctas_5_wait_time_avg = 5  # total wait time avg for ctas 5
        # self.ctas_5_wait_time_avg = parameters['avgWaitTime']['ctas_5']  # total wait time avg for ctas 5

        # average length of stay (of all runs) for each CTAS level
        self.ctas_1_length_stay_avg = 11  # length of stay avg for ctas 1
        # self.ctas_1_length_stay_avg = parameters['avglos']['ctas_1']  # length of stay avg for ctas 1
        self.ctas_2_length_stay_avg = 22  # length of stay avg for ctas 2
        # self.ctas_2_length_stay_avg = parameters['avglos']['ctas_2']  # length of stay avg for ctas 2
        self.ctas_3_length_stay_avg = 33  # length of stay abgs for ctas 3
        # self.ctas_3_length_stay_avg = parameters['avglos']['ctas_3']  # length of stay avg for ctas 3
        self.ctas_4_length_stay_avg = 44  # length of stay avg for ctas 4
        # self.ctas_4_length_stay_avg = parameters['avglos']['ctas_4']  # length of stay avg for ctas 4
        self.ctas_5_length_stay_avg = 55  # length of stay avg for ctas 5
        # self.ctas_5_length_stay_avg = parameters['avglos']['ctas_5']  # length of stay avg for ctas 5

        #  average time from Entry to CTAS Assessment (of all runs) for each CTAS level
        self.ctas_3_entry_asses_avg = 12
        # self.ctas_3_entry_asses_avg = parameters['avg_entry_assessment']['ctas_3']
        self.ctas_4_entry_asses_avg = 13
        # self.ctas_4_entry_asses_avg = parameters['avg_entry_assessment']['ctas_4']
        self.ctas_5_entry_asses_avg = 14
        # self.ctas_5_entry_asses_avg = parameters['avg_entry_assessment']['ctas_5']

        #  average time from triage to Bed Assignment (of all runs) for each CTAS level
        self.ctas_2_triage_bed_avg = 23
        # self.ctas_2_triage_bed_avg = parameters['avg_triage_bed']['ctas_2']
        self.ctas_3_triage_bed_avg = 24
        # self.ctas_3_triage_bed_avg = parameters['avg_triage_bed']['ctas_3']
        self.ctas_4_triage_bed_avg = 25
        # self.ctas_4_triage_bed_avg = parameters['avg_triage_bed']['ctas_4']
        self.ctas_5_triage_bed_avg = 26
        # self.ctas_5_triage_bed_avg = parameters['avg_triage_bed']['ctas_5']

        #  average time from Bed Assignment to Treatment (of all runs) for each CTAS level
        self.ctas_2_bed_treatment_avg = 34
        # self.ctas_2_bed_treatment_avg = parameters['avg_bed_treatment']['ctas_2']
        self.ctas_3_bed_treatment_avg = 35
        # self.ctas_3_bed_treatment_avg = parameters['avg_bed_treatment']['ctas_3']
        self.ctas_4_bed_treatment_avg = 36
        # self.ctas_4_bed_treatment_avg = parameters['avg_bed_treatment']['ctas_4']
        self.ctas_5_bed_treatment_avg = 37
        # self.ctas_5_bed_treatment_avg = parameters['avg_bed_treatment']['ctas_5']

        #  average time from Treatment to Discharge (of all runs) for each CTAS level
        self.ctas_2_treatment_discharge_avg = 45
        # self.ctas_2_treatment_discharge_avg = parameters['avg_treatment_discharge']['ctas_2']
        self.ctas_3_treatment_discharge_avg = 46
        # self.ctas_3_treatment_discharge_avg = parameters['avg_treatment_discharge']['ctas_3']
        self.ctas_4_treatment_discharge_avg = 47
        # self.ctas_4_treatment_discharge_avg = parameters['avg_treatment_discharge']['ctas_4']
        self.ctas_5_treatment_discharge_avg = 48
        # self.ctas_5_treatment_discharge_avg = parameters['avg_treatment_discharge']['ctas_5']

        # average time from Resuscitation to Discharge
        self.ctas_1_resuscitation_discharge_avg = 99.99
        # self.ctas_1_resuscitation_discharge_avg = parameters['avg_resuscitation_discharge']['ctas_1']

        # name of the simulation scenario
        self.name = "SIMULATION NAME"
        # self.name = parameters['name']


    def create_file(self):
        # create a new txt file, if the file already exists it will overwrite it
        f = open(f"Simulation {self.name} Summary.txt", "w+")

        # write into txt file
        # file header
        f.write(f"This is the summary for the {self.name} simulation \n\n")

        # write the average wait times
        f.write(f">*******************************************************************<\n")
        f.write("=> AVERAGE WAIT TIME <=\n")
        f.write(f"CTAS 1 = {self.ctas_1_wait_time_avg} minutes ;\n")
        f.write(f"CTAS 2 = {self.ctas_2_wait_time_avg} minutes ;\n")
        f.write(f"CTAS 3 = {self.ctas_3_wait_time_avg} minutes ;\n")
        f.write(f"CTAS 4 = {self.ctas_4_wait_time_avg} minutes ;\n")
        f.write(f"CTAS 5 = {self.ctas_5_wait_time_avg} minutes ;\n")
        f.write(f">*******************************************************************<\n\n")

        # write the average length of stay
        f.write(f">*******************************************************************<\n")
        f.write("=> AVERAGE LENGTH OF STAY TIME <=\n")
        f.write(f"CTAS 1 = {self.ctas_1_length_stay_avg} minutes ;\n")
        f.write(f"CTAS 2 = {self.ctas_2_length_stay_avg} minutes ;\n")
        f.write(f"CTAS 3 = {self.ctas_3_length_stay_avg} minutes ;\n")
        f.write(f"CTAS 4 = {self.ctas_4_length_stay_avg} minutes ;\n")
        f.write(f"CTAS 5 = {self.ctas_5_length_stay_avg} minutes ;\n")
        f.write(f">*******************************************************************<\n\n")

        # write the average time from Entry to CTAS Assessment
        f.write(f">*******************************************************************<\n")
        f.write("=> AVERAGE TIME FROM ENTRY TO CTAS ASSESSMENT <=\n")
        f.write(f"CTAS 3 = {self.ctas_3_entry_asses_avg} minutes ;\n")
        f.write(f"CTAS 4 = {self.ctas_4_entry_asses_avg} minutes ;\n")
        f.write(f"CTAS 5 = {self.ctas_5_entry_asses_avg} minutes ;\n")
        f.write(f">*******************************************************************<\n\n")

        # Time from triage to Bed Assignment
        f.write(f">*******************************************************************<\n")
        f.write("=> AVERAGE TIME FROM TRIAGE TO BED ASSIGNMENT <=\n")
        f.write(f"CTAS 2 = {self.ctas_2_triage_bed_avg} minutes ;\n")
        f.write(f"CTAS 3 = {self.ctas_3_triage_bed_avg} minutes ;\n")
        f.write(f"CTAS 4 = {self.ctas_4_triage_bed_avg} minutes ;\n")
        f.write(f"CTAS 5 = {self.ctas_5_triage_bed_avg} minutes ;\n")
        f.write(f">*******************************************************************<\n\n")

        # Time from Bed Assignment to Treatment
        f.write(f">*******************************************************************<\n")
        f.write("=> AVERAGE TIME FROM BED ASSIGNMENT TO TREATMENT <=\n")
        f.write(f"CTAS 2 = {self.ctas_2_bed_treatment_avg} minutes ;\n")
        f.write(f"CTAS 3 = {self.ctas_3_bed_treatment_avg} minutes ;\n")
        f.write(f"CTAS 4 = {self.ctas_4_bed_treatment_avg} minutes ;\n")
        f.write(f"CTAS 5 = {self.ctas_5_bed_treatment_avg} minutes ;\n")
        f.write(f">*******************************************************************<\n\n")

        # Time from Treatment to Discharge
        f.write(f">*******************************************************************<\n")
        f.write("=> AVERAGE TIME FROM TREATMENT TO DISCHARGE <=\n")
        f.write(f"CTAS 2 = {self.ctas_2_treatment_discharge_avg} minutes ;\n")
        f.write(f"CTAS 3 = {self.ctas_3_treatment_discharge_avg} minutes ;\n")
        f.write(f"CTAS 4 = {self.ctas_4_treatment_discharge_avg} minutes ;\n")
        f.write(f"CTAS 5 = {self.ctas_5_treatment_discharge_avg} minutes ;\n")
        f.write(f">*******************************************************************<\n\n")

        # Time from Resuscitation to Discharge
        f.write(f">*******************************************************************<\n")
        f.write("=> AVERAGE TIME FROM RESUSCITATION TO DISCHARGE <=\n")
        f.write(f"CTAS 1 = {self.ctas_1_resuscitation_discharge_avg} minutes ;\n")
        f.write(f">*******************************************************************<\n\n")

        # close the file
        f.close()


# test
# delete later
#parameters = 0
#i = txt_file_out(parameters)
#i.create_file()