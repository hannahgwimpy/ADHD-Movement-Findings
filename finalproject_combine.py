"""
@authors: Mikayla Karkoski and Hannah Wimpy
Author emails: karkoski.m@northeastern.edu & wimpy.h@northeastern.edu
NUIDs: 002179361 and 002277836
DS2001 Programming with Data Practicum
Final Project Code; Data Sorting, Combining, & Statistics Program

"""
# csv imported to allow csv files to be written
import csv

def read_movement(filename, split_by = ','):
    """
    This function takes in a file name as a parameter, reads the file, 
    gets the movement data from each row and appends it to a list to form 
    a list of movement data for the participant.

    Parameters
    ----------
    filename : str
        The name of the participant's movement data file.
    split_by : str, optional
        The punctuation to split the data by. The default is ','.

    Returns
    -------
    movement_ls : list
        List of movement data for one participant.

    """
    
    # Empty list created
    movement_ls = []
    
    # Code is tried to check for errors (to see if file exists)
    try:
        
        # File opened, lines read and set to lines variable
        with open(filename, "r") as file:
           lines = file.readlines()
           
           # For loop iterates through all lines except header line, sets each line
           # equal to a variable, removes whitespace, and splits it by a semicolon
           for line in lines[1:]:
               line_data = line.strip().split(';')
               
               # If data in movement cell is not empty, data is set to variable, 
               # converted to integer, and appended to the list 
               if line_data[1] != "": 
                   patient_movement = int(line_data[1]) # Patient movement
                   movement_ls.append(patient_movement)
    
    # If error is encountered (file does not exist), above code not run and pass 
    # allows no errors to occur and for program to continue running
    except:
        pass
    return movement_ls

    # try/except source: https://www.geeksforgeeks.org/python-try-except/
    # pass source: https://www.w3schools.com/python/ref_keyword_pass.asp

def calculate_statistics(movement_data):
    """
    This function takes in a list of movement data, finds the average and standard
    deviation and returns them.

    Parameters
    ----------
    movement_data : list
        List of movement data for one participant.

    Returns
    -------
    average : float
        The calculated average of the inputted movement list.
    std_dev : float
        The calculated standard deviation of the inputted movement list.

    """
    # Function run if list has a length, avoids "ZeroDivisionError"
    if len(movement_data) > 0:
        
        # Average calculated by dividing sum of list by length of list
        average = sum(movement_data) / len(movement_data)
        
        # Standard deviation calculated by finding variance then square rooting it using 
        # formula from https://byjus.com/maths/variance-and-standard-deviation/
        variance = sum((x - average) ** 2 for x in movement_data) / len(movement_data)
        std_dev = variance ** 0.5
    
        return average, std_dev

def make_patient_info_dict(filename, split_by = ','):
    """
    This function takes in a patient information filename, reads it, and creates a 
    patient information dictionary from it. 

    Parameters
    ----------
    filename : str
        The name of the patient info csv file.
    split_by : str, optional
        The punctuation to split the data by. The default is ','.

    Returns
    -------
    patient_info : dict
        Patient information dictionary with the patient ids as the keys and the patient
        sex and adhd statuses as the values.

    """
    # Empty dictionary created 
    patient_info = {}
    
    # File opened, lines read except headers, each line set to variable, stripped of whitespace, 
    # and split by semicolons
    with open(filename, "r") as file:
        lines = file.readlines()
        for line in lines[1:]:
            line_data = line.strip().split(';')
            
            # If patient id exists, patient id, sex, and adhd status assigned to variables if 
            # sex and adhd status data exists, sex and adhd data variables converted to int
            if line_data[0] != "":
                patient_id = line_data[0]
                patient_sex = int(line_data[1]) if line_data[1] else None 
                patient_adhd = int(line_data[10]) if line_data[10] else None
                
                # Dictionary entry created with patient id as key and patient sex and adhd status as
                # values 
                patient_info[patient_id] = {"sex": patient_sex, "adhd status": patient_adhd}
    return patient_info 

def make_lists(patient_info):   
    """
    This function takes in a patient information dictionary, reads through each patient activity file
    using patient ids, and adds data to lists based on sex and adhd status.

    Parameters
    ----------
    patient_info : dict
        Patient information dictionary with the patient ids as the keys and the patient
        sex and adhd statuses as the values.

    Returns
    -------
    combined_data_f : list
        List of averages and standard deviations for female patients with ADHD.
    combined_data_m : list
        List of averages and standard deviations for male patients with ADHD.
    combined_data_c_f : list
        List of averages and standard deviations for female patients without ADHD.
    combined_data_c_m : list
        List of averages and standard deviations for male patients without ADHD.

    """
    # Empty sex and adhd status lists created
    combined_data_f = []
    combined_data_m = []
    combined_data_c_f = []
    combined_data_c_m = []
    
    # For loop iterates through each patient movement file with index correspondin to patient id 
    for i in range (1, 109):
        patient_id_str = str(i)
        
        # If patient id found in patient info file, activity file set to variable using index/id,
        # movement data for patient read using readz_movement function, avg and std found using 
        # calculate_statistics function, and movement stat set to variable
        if patient_id_str in patient_info:
            if i <= 9:
                activity_file_name = "patient_activity_0" + str(i) + ".csv"
                data_movement_stat = calculate_statistics(read_movement(activity_file_name))
            elif 10 <= i <= 108:
                activity_file_name = "patient_activity_" + str(i) + ".csv"
                data_movement_stat = calculate_statistics(read_movement(activity_file_name))
            
            # Patient dict set to variable, sex and adhd info extracted from dict using index
            patient_data = patient_info[patient_id_str]
            sex_info = patient_data["sex"]
            adhd_info = patient_data["adhd status"]
            
            # for sex, 0 is female and 1 is male, for adhd, 0 is no adhd and 1 is adhd
            # patient activity data appended to respected lists based on sex and adhd status
            if data_movement_stat:
                if sex_info == 0 and adhd_info == 1: 
                        combined_data_f.append(data_movement_stat)
                elif sex_info == 1 and adhd_info == 1: 
                        combined_data_m.append(data_movement_stat)
                elif sex_info == 0 and adhd_info == 0:
                        combined_data_c_f.append(data_movement_stat)
                elif sex_info == 1 and adhd_info == 0:
                        combined_data_c_m.append(data_movement_stat)
    return combined_data_f, combined_data_m, combined_data_c_f, combined_data_c_m

def create_csv(filename, data):
    """
    This function takes in a file name to create, a list of data to add to the file, 
    and adds the data to the file.

    Parameters
    ----------
    filename : str
        Name of file to create
    data : list
        List of data to write to file

    Returns
    -------
    None.

    """
    # Technique to write csv source: https://blog.enterprisedna.co/how-to-write-a-list-to-csv-in-python/
    
    # File created, csv writer to write each row of the list to the csv file
    with open(filename, 'w', newline='') as file:
        writer = csv.writer(file)
        for row in data:
            writer.writerow([row])  
   
    
def main():
    
    # Patient info dictionary created using make_patient_info_dict function using dataset provided file
    patient_info = make_patient_info_dict("patient_info.csv")
    
    # File names set to variables
    combined_file_f = "patient_activity_combined_f.csv"
    combined_file_m = "patient_activity_combined_m.csv"
    combined_file_c_f = "patient_activity_c_combined_f.csv"
    combined_file_c_m = "patient_activity_c_combined_m.csv"
    
    # Patient activity average and stdev lists created based on sex and adhd status using make_lists function
    # and lists set to variable
    combined_data_f = make_lists(patient_info)[0]
    combined_data_m = make_lists(patient_info)[1]
    combined_data_c_f = make_lists(patient_info)[2]
    combined_data_c_m = make_lists(patient_info)[3]
    
    # Patient csvs created using lists based on attributes, specified filenames, and the create_csv function
    create_csv(combined_file_f, combined_data_f)
    create_csv(combined_file_m, combined_data_m)
    create_csv(combined_file_c_f, combined_data_c_f)
    create_csv(combined_file_c_m, combined_data_c_m)
    
          
# testing center: 
    
    # print("Female ADHD combined list:", combined_data_f)
    # print("Male ADHD combined list:", combined_data_m)
    
    # patient_movement_11 = read_movement("patient_activity_11.csv")
    
    # patient_11_stats = calculate_statistics(patient_movement_11)
    
    # print(patient_11_stats)
   
    

main()