"""
@author: Mikayla Karkoski and Hannah Wimpy
NUIDs: 002179361 and 002277836
Author emails: karkoski.m@northeastern.edu & wimpy.h@northeastern.edu
DS2001 Programming with Data Practicum
Final Project Code; Graphing Program

"""
# Import needed libraries for file opening, statistics, and graphing
import csv
import matplotlib.pyplot as plt
import numpy as np
from scipy.stats import t

def get_avgs(filename):
    """
    This function reads a CSV file containing statistics info, extracts the averages from
    the file, and appends them to a list. 

    Parameters
    ----------
    filename : str
        CSV file that is read.

    Returns
    -------
    avgs_ls : list
        List of averages from the CSV file. 

    """
    # Empty lists created
    avgs_ls = []
    
    # Technique to read csv source: https://docs.python.org/3/library/csv.html
    # Source for list function: https://www.w3schools.com/python/ref_func_list.asp
    
    # CSV file opened, read with csvreader, set to variable, converted to a list of 
    # rows using list function
    with open(filename) as file:
        csvreader = csv.reader(file, delimiter=',')
        rows = list(csvreader)
    
    # Source for eval() function: https://www.programiz.com/python-programming/methods/built-in/eval
    
    # Data in rows set to variable, list of tuples evaluated as python expression
    # using eval() function, first and second elements of tuple (average movement and standard deviation) 
    # converted to float and appended to respective lists
    for data in rows:
        movement_data = eval(data[0])
        avg = float(movement_data[0])
        avgs_ls.append(avg)
    return avgs_ls

def std_errors_scatter(filename):
    """
    This function reads a CSV file containing statistics info, extracts the standard 
    deviations from the file, calculates the standard errors using the standard deviations,
    and appends them to a list.

    Parameters
    ----------
    filename : str
        CSV file that is read.

    Returns
    -------
    std_error_ls : list
        List of standard errors from the CSV file. 

    """
    # Empty list created
    std_error_ls = []
    
    # Technique to read csv source: https://docs.python.org/3/library/csv.html
    # Source for list function: https://www.w3schools.com/python/ref_func_list.asp
    # Technique for finding standard errors source: https://www.statology.org/standard-error-of-mean-python/
    
    # CSV file opened, read with csvreader, set to variable, converted to a list of 
    # rows using list function
    with open(filename) as file:
        csvreader = csv.reader(file, delimiter=',')
        rows = list(csvreader)
    
    # Source for eval() function: https://www.programiz.com/python-programming/methods/built-in/eval
    
    # Data in rows set to variable, list of tuples evaluated as python expression
    # using eval() function, first and second elements of tuple (average movement and standard deviation) 
    # converted to float and appended to respective lists
    for data in rows:
        movement_data = eval(data[0])
        std_error = np.std(movement_data, ddof = 1) / np.sqrt(np.size(movement_data))
        std_error_ls.append(std_error)
    return std_error_ls

def std_errors_bar(avgs_list):
    """
    This function calculates the standard error of a list of averages.

    Parameters
    ----------
    avgs_list : list
        List of averages from the CSV file.

    Returns
    -------
    std_error : float
        The calculated standard error of the values from the inputted list. 

    """
    # Technique for finding standard errors source: https://www.statology.org/standard-error-of-mean-python/
    avgs = avgs_list
    
    # standard errors found using numpy function
    std_error = np.std(avgs, ddof = 1) / np.sqrt(np.size(avgs))
    
    return std_error

def average(avgs_list):
    """
    This function takes in a list of averages and finds the average of the list,
    and returns this average. 

    Parameters
    ----------
    avgs_list : list
        List of averages from the CSV file. 

    Returns
    -------
    average : float
        The calculated average of the values from the inputted list. 

    """
    # Average found by dividing the sum of the list by the length of the list
    average = sum(avgs_list) / len(avgs_list)
    return average

def variance(control_avgs_ls, adhd_avgs_ls):
    """
    This function calculates the variance ratio of two sets of data.

    Parameters
    ----------
    control_avgs_ls : list
        List of averages of the control group.
    adhd_avgs_ls : list
        List of averages of the ADHD group.

    Returns
    -------
    variance_ratio : float
        The calculated variance ratio of the two sets of data.

    """
    # Source for variance: https://www.geeksforgeeks.org/how-to-conduct-a-two-sample-t-test-in-python/
    
    # lists converted to numpy arrays
    data_control = np.array(control_avgs_ls)
    data_adhd = np.array(adhd_avgs_ls)
    
    # variance found using numpy variance function
    control_variance = np.var(data_control)
    adhd_variance = np.var(data_adhd)
    
    # variance ratio found using formula
    variance_ratio = adhd_variance / control_variance
    
    return round(variance_ratio, 2)

def p_value(control_avgs_ls, adhd_avgs_ls, correction, alpha = 0.2):
    """
    This function calculates the p-value for the significance test between two groups.

    Parameters
    ----------
    control_avgs_ls : list
        List of averages of the control group.
    adhd_avgs_ls : list
        List of averages of the ADHD group.
    correction : bool
        Correction for equal variances.
    alpha : float, optional
        Alpha value for significance. Default is 0.2.

    Returns
    -------
    p_value : float
        The calculated p-value for the significance test.

    """
    # Source for t test: https://www.geeksforgeeks.org/how-to-find-a-p-value-from-a-t-score-in-python/ 
    
    # averages found using average function
    mean1 = average(control_avgs_ls)
    mean2 = average(adhd_avgs_ls)
    
    # standard deviations found using numpy functions
    std1 = np.std(control_avgs_ls, ddof=1) 
    std2 = np.std(adhd_avgs_ls, ddof=1)
    
    # length of data lists found using len function
    n1 = len(control_avgs_ls)
    n2 = len(adhd_avgs_ls)
    
    # t score and degrees of freedomn calculated using formulas
    t_score = (mean1 - mean2) / np.sqrt((std1**2 / n1) + (std2**2 / n2))
    df = n1 + n2 - 2  # For a two-sample t-test
        
    # two tailed p value found using scipy stats module function and numpy absolute value function (for negative t values)
    p_value = 2 * (1 - t.cdf(np.abs(t_score), df))
    
    # printed if null hypothesis is rejected or not using alpha and p value
    if p_value < alpha:
        print("\nP value =", round(p_value, 2), "<", alpha, "= alpha. Reject the null hypothesis. There is a statistically significant difference.")
    else:
        print("\nP value =", round(p_value, 2), ">", alpha, "= alpha. Fail to reject the null hypothesis. There is no statistically significant difference.")
    
    return round(p_value, 2)

def scatter(adhd_f_avgs, adhd_m_avgs, c_f_avgs, c_m_avgs, c_f_avg, c_m_avg, adhd_f_avg, adhd_m_avg, adhd_f_std_errors, adhd_m_std_errors, c_f_std_errors, c_m_std_errors, p_alpha=0.05):    
    """
    This function creates a scatterplot of movement averages for each participant based on gender and ADHD status.

    Parameters
    ----------
    adhd_f_avgs : list
        List of movement averages of females with ADHD from the CSV file.
    adhd_m_avgs : list
        List of movement averages of males with ADHD from the CSV file.
    c_f_avgs : list
        List of movement averages of females without ADHD from the CSV file.
    c_m_avgs : list
        List of movement averages of males without ADHD from the CSV file.
    c_f_avg : float
        Average movement of control females.
    c_m_avg : float
        Average movement of control males.
    adhd_f_avg : float
        Average movement of ADHD females.
    adhd_m_avg : float
        Average movement of ADHD males.
    adhd_f_std_errors : list
        List of standard errors for ADHD females.
    adhd_m_std_errors : list
        List of standard errors for ADHD males.
    c_f_std_errors : list
        List of standard errors for control females.
    c_m_std_errors : list
        List of standard errors for control males.

    Returns
    -------
    None.

    """
    # Source for adding error bars: https://www.geeksforgeeks.org/use-error-bars-in-a-matplotlib-scatter-plot/
    # Source for adding horizontal lines at averages of averages:  https://www.geeksforgeeks.org/plot-a-horizontal-line-in-matplotlib/
    
    # Figure  size and pixelation set; number of participants found for x values using range() and len() functions,
    # starting at 1 because python indexes start at 0
    plt.figure(figsize=(7, 7), dpi=800)
    adhd_f_part = range(1, len(adhd_f_avgs) + 1)
    adhd_m_part = range(1, len(adhd_m_avgs) + 1)
    control_f_part = range(1, len(c_f_avgs) + 1)
    control_m_part = range(1, len(c_m_avgs) + 1)
    
    # Data scatterplotted for each group, averages for each group's total data plotted as horizontal line, standard error bars added
    plt.scatter(adhd_f_part, adhd_f_avgs, color='pink', label="ADHD Females")
    plt.axhline(y=adhd_f_avg, color='pink', linestyle='-')
    plt.errorbar(adhd_f_part, adhd_f_avgs, yerr=adhd_f_std_errors, fmt="o", color='pink')
    plt.scatter(adhd_m_part, adhd_m_avgs, color='green', label="ADHD Males")
    plt.axhline(y=adhd_m_avg, color='green', linestyle='-')
    plt.errorbar(adhd_m_part, adhd_m_avgs, yerr=adhd_m_std_errors, fmt="o", color='green')
    plt.scatter(control_f_part, c_f_avgs, color='purple', label="Control Females")
    plt.axhline(y=c_f_avg, color='purple', linestyle='-')
    plt.errorbar(control_f_part, c_f_avgs, yerr=c_f_std_errors, fmt="o", color='purple')
    plt.scatter(control_m_part, c_m_avgs, color='blue', label="Control Males")
    plt.axhline(y=c_m_avg, color='blue', linestyle='-')
    plt.errorbar(control_m_part, c_m_avgs, yerr=c_m_std_errors, fmt="o", color='blue')
    
    # Title, axes labels, y range, & legend added; figured saved and shown
    plt.title("Average Movement of Each Participant Based on Gender and ADHD Status")
    plt.xlabel("Participants")
    plt.ylabel("Movement")
    plt.ylim(0, 600)
    plt.legend()
    plt.savefig("adhd_vs_control_movement_scatter_across_genders.jpg")
    plt.show()

def bar_graphs(c_f_avg, c_m_avg, adhd_f_avg, adhd_m_avg, adhd_f_std_error, adhd_m_std_error, c_f_std_error, c_m_std_error, female_p, male_p, alpha):
    """
    This function creates bar graphs of average movement based on ADHD status and gender.

    Parameters
    ----------
    c_f_avg : float
        Average movement of control females.
    c_m_avg : float
        Average movement of control males.
    adhd_f_avg : float
        Average movement of ADHD females.
    adhd_m_avg : float
        Average movement of ADHD males.
    adhd_f_std_error : float
        Standard error for ADHD females.
    adhd_m_std_error : float
        Standard error for ADHD males.
    c_f_std_error : float
        Standard error for control females.
    c_m_std_error : float
        Standard error for control males.
    female_p : float
        The calculated p-value for the significance test for females.
    male_p : float
        The calculated p-value for the significance test for males.
    alpha : float
        Alpha value for significance.

    Returns
    -------
    None.

    """
    # Techninque for adding significance text source: https://bbquercus.medium.com/adding-statistical-significance-asterisks-to-seaborn-plots-9c8317383235
    # used option 2 in source
    # Source for adding error bars: https://www.geeksforgeeks.org/use-error-bars-in-a-matplotlib-scatter-plot/
    
    # font size updated (source: https://www.geeksforgeeks.org/change-font-size-in-matplotlib/)
    plt.rcParams.update({'font.size': 14}) 

    def add_significance_text(p_value, x, y):
        """
        The function takes in a x-y coordinate location and a p value and outputs significance text.

        Parameters
        ----------
        p_value : The calculated p-value for the significance test 
            
        x : int
            The x position for the significance text
        y : int
            The x position for the significance text

        Returns
        -------
        str
            Significance text based on p value

        """
        if p_value <= alpha:
            return "*"
        else:
            return " (n.s.)"

    def plot_bar_graph(title, x_label, y_label, ylim, control_avg, adhd_avg, control_std_error, adhd_std_error, control_color, adhd_color, p_value):
        """
        The function takes in a title, axes labels, a y axis limit, data averages and standard errors, bar colors, and p values and create a bar graph.

        Parameters
        ----------
        title : str
            Title of bar graph
        x_label : str
            x axis label
        y_label : str
            y axis label
        ylim : int
            DESCRIPTION.
        control_avg : float
            Average movement of control group
        adhd_avg : float
            Average movement of ADHD group
        control_std_error : float
            Standard error of control group
        adhd_std_error : float
            Standard error of ADHD group
        control_color : str
            Color of control group
        adhd_color : str
            Color of ADHD group
        p_value : float
            Calculated p value for groups

        Returns
        -------
        None.

        """
        # Figure size, pixelation, title, axes titles, and y limit set
        plt.figure(figsize=(9, 9),dpi=800)
        plt.title(title)
        plt.xlabel(x_label)
        plt.ylabel(y_label)
        plt.ylim(0, 400)
        
        # Bar labels created using significance text function
        control_label = "Control" + add_significance_text(p_value, 0, ylim - 20)
        adhd_label = "ADHD" + add_significance_text(p_value, 0, ylim - 20)

        # Bars and standard error bars plotted and labeled
        plt.bar(control_label, control_avg, width=0.6, color=control_color, label="Control")
        plt.errorbar(control_label, control_avg, yerr=control_std_error, fmt="o", color='black')
        plt.bar(adhd_label, adhd_avg, width=0.6, color=adhd_color, label="ADHD")
        plt.errorbar(adhd_label, adhd_avg, yerr=adhd_std_error, fmt="o", color='black')
        
        # legend added, figure saved and shown
        plt.legend(loc="upper left")
        plt.savefig(str(p_value) + "adhd_vs_control.jpg")
        plt.show()

    # Bar graphs plotted for both groups using plot_bar_graph function
    plot_bar_graph("Average Movement of All Female Participants Based on ADHD Status",
                   "Group", "Average Movement", 300,
                   c_f_avg, adhd_f_avg, c_f_std_error, adhd_f_std_error, 'purple', 'pink', female_p)
    plot_bar_graph("Average Movement of All Male Participants Based on ADHD Status",
                   "Group", "Average Movement", 300,
                   c_m_avg, adhd_m_avg, c_m_std_error, adhd_m_std_error, 'blue', 'green', male_p)


def main():
    # Files read for participants with adhd using read_csv function, averages set to variable, 
    # and average of those averages found using avg function
    adhd_f_avgs = get_avgs("patient_activity_combined_f.csv")
    adhd_m_avgs = get_avgs("patient_activity_combined_m.csv")
    adhd_f_avg = average(adhd_f_avgs) 
    adhd_m_avg = average(adhd_m_avgs) 
    adhd_f_std_errors = std_errors_scatter("patient_activity_combined_f.csv")
    adhd_m_std_errors= std_errors_scatter("patient_activity_combined_m.csv")
    adhd_f_std_error = std_errors_bar(adhd_f_avgs)
    adhd_m_std_error= std_errors_bar(adhd_m_avgs)
    
    # Files read for participants without adhd using read_csv function, averages set to variable, 
    # and average of those averages found using avg function
    c_f_avgs = get_avgs("patient_activity_c_combined_f.csv")
    c_m_avgs = get_avgs("patient_activity_c_combined_m.csv")
    c_f_avg = average(c_f_avgs) 
    c_m_avg = average(c_m_avgs) 
    c_f_std_errors = std_errors_scatter("patient_activity_c_combined_f.csv")
    c_m_std_errors= std_errors_scatter("patient_activity_c_combined_m.csv")
    c_f_std_error = std_errors_bar(c_f_avgs)
    c_m_std_error= std_errors_bar(c_m_avgs)
    
    # if variances less than 4 : 1, correction is true in t test calculations (variance is assumed to be the same)
    variance_ratio_females = variance(c_f_avgs, adhd_f_avgs)
    print("Variance ratio females:", variance_ratio_females)
    variance_ratio_males = variance(c_m_avgs, adhd_m_avgs)
    print("Variance ratio males:", variance_ratio_males)
    # correction is true
    
    # Significance found using t test function with lists and true correction
    female_p = p_value(c_f_avgs, adhd_f_avgs, True)
    male_p = p_value(c_m_avgs, adhd_m_avgs, True)
   
    
    # Scatterplot created using scatter function and averages of all participants in lists 
    # differentiated by sex and adhd status
    scatter(adhd_f_avgs, adhd_m_avgs, c_f_avgs, c_m_avgs, c_f_avg, c_m_avg, adhd_f_avg, adhd_m_avg, adhd_f_std_errors, adhd_m_std_errors, c_f_std_errors, c_m_std_errors)
    
    # Bar graphs created using bar_graphs function and the averages of the averages of all 
    # participants in lists differentiated by sex and adhd status
    bar_graphs(c_f_avg, c_m_avg, adhd_f_avg, adhd_m_avg, adhd_f_std_error, adhd_m_std_error, c_f_std_error, c_m_std_error, female_p, male_p, 0.2)

# Call to main
main()