
# coding: utf-8

# In[2]:


import pandas as pd
import numpy as np
import itertools
import operator


# In[3]:





# In[4]:


def find_people_on_committees(committees, arr):
    #given a list of the committees and the array from the excel file, return a list of all people on each committee

    people_on_committees = []

    for i in range(len(committees)):
        committee_members = []
        for j in range(len(arr)):
            if arr[j][i+1] == 'x':
                tup = (arr[j][0], 1)
            elif arr[j][i+1] == 'x vc':
                tup = (arr[j][0], 5)
            elif arr[j][i+1] == 'x C' or arr[j][i+1] == 'xC':
                tup = (arr[j][0], 5)
            else:
                tup = (arr[j][0], 'nan')
            if isinstance(tup[1], int) == True:
                committee_members.append(tup)
        people_on_committees.append(committee_members)
    return people_on_committees


# In[5]:


def common_member(a, b):
    #returns true if there is a common element in a and b, false otherwise

    a_set = set(a)
    b_set = set(b)
    if len(a_set.intersection(b_set)) > 0:
        return(True)
    return(False)


# In[6]:


def find_unique_pairings(committees):
    #Finds all unique committee pairings given a list of the committees

    iterations = list(itertools.combinations(committees,3))
    unique_committee_pairings = []
    for i in iterations:
        for j in iterations:
            common_element = common_member(i,j)
            num = []
            if common_element == False:
                num.extend(i)
                num.extend(j)
                last_two = []
                for k in range(len(committees)):
                    if committees[k] not in num:
                        num.append(committees[k])
            if len(num) != 0:
                unique_committee_pairings.append(num)
    return unique_committee_pairings



# In[7]:


def find_num_missed_meetings2(cmte1, cmte2):
    #given two committees ([(name,type), (name, type),...]), find the number of missed meetings between the two committees.
    #If, in any conflict, the board member is a vice chair or chair for both, set the conflicts to a very high number.
    all_names = cmte1 + cmte2
    conflicts = 0
    people = []

    dict = {}
    for i in range(len(all_names)):
        if all_names[i][0] in dict:
            dict[all_names[i][0]] += all_names[i][1]
        else:
            dict[all_names[i][0]] = all_names[i][1]

    for name in dict:
        if dict[name] > 9:
            conflicts = 100
            return conflicts, people
        elif dict[name] > 4:
            num_cons = dict[name] - 5
            conflicts += num_cons
            if num_cons > 0:
                people.append(name)
        elif dict[name] > 1:
            num_cons = dict[name] - 1
            conflicts += num_cons
            if num_cons > 0:
                people.append(name)

    return conflicts, people



# In[8]:


def find_num_missed_meetings3(cmte1, cmte2, cmte3):
    #given three committees ([(name,type), (name, type),...]), find the number of missed meetings between the two committees.
    #If, in any conflict, the board member is a vice chair or chair for both, set the conflicts to a very high number.

    all_names = cmte1 + cmte2 + cmte3
    conflicts = 0
    people = []

    dict = {}
    for i in range(len(all_names)):
        if all_names[i][0] in dict:
            dict[all_names[i][0]] += all_names[i][1]
        else:
            dict[all_names[i][0]] = all_names[i][1]

    for name in dict:
        if dict[name] > 9:
            conflicts = 100
            return conflicts, people
        elif dict[name] > 4:
            num_cons = dict[name] - 5
            conflicts += num_cons
            if num_cons > 0:
                people.append(name)
        elif dict[name] > 1:
            num_cons = dict[name] - 1
            conflicts += num_cons
            if num_cons > 0:
                people.append(name)

    return conflicts, people


# In[9]:


def find_missed_meetings2(people_on_committees, committees):
    #return an array of arrays, each of which has two committee names, the number of missed meetings between them,
    #and the people missing a meeting

    missed_meetings2 = []

    for i in range(len(committees)):
        for j in range(len(committees)):
            num_conflicts, people = find_num_missed_meetings2(people_on_committees[i], people_on_committees[j])
            array = [[committees[i], committees[j]], num_conflicts, people]
            missed_meetings2.append(array)
    return missed_meetings2


# In[10]:


def find_missed_meetings3(people_on_committees, committees):
    #return an array of arrays, each of which has three committee names, the number of missed meetings between them,
    #and the people missing a meeting

    missed_meetings3 = []

    for i in range(len(committees)-1):
        for j in range(len(committees)-1):
            for k in range(len(committees)-1):
                num_conflicts, people = find_num_missed_meetings3(people_on_committees[i], people_on_committees[j], people_on_committees[k])
                array = [[committees[i], committees[j], committees[k]], num_conflicts, people]
                missed_meetings3.append(array)
    return missed_meetings3


# In[11]:


def calculate_results_array(unique_committee_pairings, missed_meetings2, missed_meetings3):

    final_array = []

    for i in range(len(unique_committee_pairings)):
        num_misses = 0
        names = []

        first_block = unique_committee_pairings[i][0:3]
        sec_block = unique_committee_pairings[i][3:6]
        third_block = unique_committee_pairings[i][6:8]

        for j in missed_meetings3:

            if j[0] == first_block:
                num_misses += j[1]
                names.extend(j[2])
            if j[0] == sec_block:
                num_misses += j[1]
                names.extend(j[2])
        for k in missed_meetings2:
            if k[0] == third_block:
                num_misses += k[1]
                names.extend(k[2])

        data = [unique_committee_pairings[i], names]
        final_array.append((num_misses, data))

    return final_array


# In[12]:


def print_results(results):
    print("Here are your top five schedules with three time slots and as few conflicts as possible:")

    for i in range(0,10,2):
        print("_"*100)
        print("")
        print("%d) %d total missed meetings" % ((i/2)+1, results[i][0]))
        print("")
        print("   Time slot 1:" )
        print("          1. %s" % results[i][1][0][0])
        print("          2. %s" % results[i][1][0][1])
        print("          3. %s" % results[i][1][0][2])

        print("     Time slot 2:")
        print("          1. %s" % results[i][1][0][3])
        print("          2. %s" % results[i][1][0][4])
        print("          3. %s" % results[i][1][0][5])

        print("     Time slot 3:")
        print("          1. %s" % results[i][1][0][6])
        print("          2. %s" % results[i][1][0][7])
        print("")

        print("  If you go with this schedule, the following people will have to miss at least one meeting: ")
        for j in range(len(results[i][1][1])):
            print("        %d. %s" % (j+1, results[i][1][1][j]))


if __name__ == '__main__':
    df = pd.read_excel('committees.xlsx')
    committees = np.array(df.columns[1:])
    committees = committees.tolist()
    arr = df.as_matrix()

    people_on_committees = find_people_on_committees(committees, arr)
    unique_committee_pairings = find_unique_pairings(committees)

    missed_meetings2 = find_missed_meetings2(people_on_committees, committees)
    missed_meetings3 = find_missed_meetings3(people_on_committees, committees)

    results = calculate_results_array(unique_committee_pairings, missed_meetings2, missed_meetings3)
    results.sort(key=operator.itemgetter(0))
    print_results(results)


# In[ ]:


# TO DO
# ensure each committee has at most 2 persons missing their meeting NOT NECESSARY
# get this online TO DO STILL!
# vice-chair, chair stuff DONE
# names of those missing meetings DONE
# prettier output DONE
