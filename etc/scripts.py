# import pandas as pd
# import random
# # from datetime import date, timedelta, datetime
# # from django.contrib.auth.models import User

# df = pd.read_csv('../etc/names.csv')
# df1 = pd.read_csv('../etc/stations.csv')
# df2 = pd.read_csv('../etc/wards.csv')

# import os
# import pandas as pd

# # Read the input CSV file
# df = pd.read_csv('./stations.csv')

# # Group the data by County Code
# grouped = df.groupby('County Code')

# # Create a folder to store the files
# folder_path = 'output_folder'
# os.makedirs(folder_path, exist_ok=True)

# # Iterate over each group and save to separate files
# for county_code, group_df in grouped:
#     filename = f'county_{county_code}.csv'
#     file_path = os.path.join(folder_path, filename)
#     group_df.to_csv(file_path, index=False)
#     print(f'Saved data for County Code {county_code} to {file_path}')


# def cs():
#     for i in range (len(df2)):
#         id = df2['id'][i]
#         c = df2['County'][i]
#         County.objects.create(name=c, id=id)

# def cs2():
#     for i in range (len(df2)):
#         county = df1['County'][i] 
#         cs = df1['Constituency_name'][i] 
#         w = df1['Ward'][i] 
#         id = df1['id'][i] 
#         if Consituency.objects.get(name__icontains=cs):
#             cs1 = Consituency.objects.get(name__icontains=cs)
#         else:
#             cs1 = Consituency.objects.create(name=const, id=cid, county=county)


# def cs1(id):
#     # cid, wid, cid2 = 1, 1, 1
#     f = f"../etc/output_folder/county_{id}.csv"
#     df1 = pd.read_csv(f)
#     for i in range (len(df1)):
#         c1, c2, c3  = '', '', ''
#         cid = Consituency.objects.latest('id').id + 1
#         wid = Ward.objects.latest('id').id + 1
#         cid2 = PollingCenter.objects.latest('id').id + 1
#         # ct1 = df1['County Name'][i] 
#         county = County.objects.get(id=id)       
#         const = df1['Const Name'][i]
#         try:
#             c1 = Consituency.objects.get(name__icontains=const)
#         except:
#             c1 = Consituency.objects.create(name=const, id=cid, county=county)
#             print()
#             print(const)
#         ward = df1['CAW Name'][i]
#         try:
#             c2 = Ward.objects.get(name__icontains=ward)
#         except:
#             c2 = Ward.objects.create(name=ward, id=wid, constituency=c1)
#             print(ward)
#         center = df1['Reg Centre Name'][i]
#         try:
#             c3 = PollingCenter.objects.get(name__icontains=center)
#         except:
#             c3 = PollingCenter.objects.create(name=center, id=cid2, ward=c2)
#             print(center, end='---')
#         sid = df1['Polling Station Code'][i]
#         station = df1['Polling Station Name'][i]
#         voters = df1['Registered Voters'][i]
#         try:
#             PollingStation.objects.create(name=station, id=sid, center=c3, voter_no=voters)
#             print(sid, end='--')
#         except:
#             pass

# def nms():
#     for i in range (len(df)):
#         gender = df['Gender'][i]
#         if gender == 'boy':
#             g = "M"
#         else:
#             g = "F"
#         if i % 2 == 0:
#             fname = df['Name'][i]
#         else:
#             lname = df['Name'][i]
#             random_date = generate_random_date()
#             today = datetime.today()
#             years = today.year - random_date.year
#             nid = random.randint(10000000, 99999999)
#             letters = ['C', 'F']
#             occ = random.choice(letters)
#             user = User.objects.create_user(f"{nid}","a@m.com",f"{random_date}")
#             profile = UserProfile.objects.create(dob=random_date,first_name=fname,last_name=lname,gender=g,occupation=occ,user=user,id_number=nid,age=years)
#             print(fname, lname,random_date, years, occ, nid, g, profile)



# def generate_random_date():
#     start_year = 1920
#     end_year = 2005
#     start_date = date(start_year, 1, 1)
#     end_date = date(end_year, 12, 31)

#     time_between_dates = end_date - start_date
#     days_between_dates = time_between_dates.days

#     random_number_of_days = random.randint(0, days_between_dates)
#     random_date = start_date + timedelta(days=random_number_of_days)

#     return random_date

# # Example usage

# us = UserProfile.objects.all()[:100]

# def vt():
#     for u in us:
#         n = random.randint(700000000, 999999999)
#         sta = PollingStation.objects.all()[0]
#         Voter.objects.create(
#             profile=u,
#             voter_id = n,
#             station = sta
#             ,)

# import csv

# def delete_columns(input_file, output_file, columns_to_delete):
#     with open(input_file, 'r') as file:
#         reader = csv.reader(file)
#         header = next(reader)  # Read the header row
#         indices_to_delete = [header.index(col) for col in columns_to_delete]
#         filtered_header = [col for col in header if col not in columns_to_delete]
#         rows = [[row[i] for i in range(len(row)) if i not in indices_to_delete] for row in reader]

#     with open(output_file, 'w', newline='') as file:
#         writer = csv.writer(file)
#         writer.writerow(filtered_header)
#         writer.writerows(rows)

# # Usage example
# input_file = './output.csv'
# output_file = './output1.csv'
# columns_to_delete = ['emp1', 'emp2']
# delete_columns(input_file, output_file, columns_to_delete)

# import csv
# import re

# def clean_registered_voters(input_file, output_file):
#     with open(input_file, 'r') as file:
#         reader = csv.DictReader(file)
#         fieldnames = reader.fieldnames
#         rows = []

#         for row in reader:
#             registered_voters = row['Registered Voters']
#             cleaned_value = re.sub('[^0-9]', '', registered_voters)
#             row['Registered Voters'] = cleaned_value
#             rows.append(row)

#     with open(output_file, 'w', newline='') as file:
#         writer = csv.DictWriter(file, fieldnames=fieldnames)
#         writer.writeheader()
#         writer.writerows(rows)

# # Usage example
# input_file = './output1.csv'
# output_file = './output2.csv'
# clean_registered_voters(input_file, output_file)


# import csv
# from datetime import datetime, timedelta
# import random

# def generate_birthdate(age_group):
#     today = datetime.today()
#     min_age, max_age = age_group
#     random_days = random.randint(min_age * 365, max_age * 365)
#     birthdate = today - timedelta(days=random_days)
#     return birthdate.strftime("%Y-%m-%d")

# # Define the age groups and their corresponding percentage ranges
# age_groups = {
#     "18-25": (18, 25),
#     "26-35": (26, 35),
#     "36-45": (36, 45),
#     "46-55": (46, 55),
#     "56 and above": (56, 100)
# }

# # Define the percentage ranges for each age group
# percentage_ranges = {
#     "18-25": (15, 23),
#     "26-35": (15, 23),
#     "36-45": (10, 15),
#     "46-55": (7, 10),
#     "56 and above": (3, 7)
# }

# # Read the CSV file with names
# with open('./names.csv', 'r') as file:
#     reader = csv.reader(file)
#     headers = next(reader)  # Read and store the header row

#     # Add new column headers
#     headers.extend(["Age Group", "Birthdate"])

#     # Create a new CSV file with updated columns
#     with open('./updated_names.csv', 'w', newline='') as outfile:
#         writer = csv.writer(outfile)
#         writer.writerow(headers)

#         for row in reader:
#             name = row[0]
#             age_group = random.choices(list(age_groups.keys()), weights=[19, 19, 12, 8, 5], k=1)[0]
#             percentage_range = percentage_ranges[age_group]
#             min_percentage, max_percentage = percentage_range
#             random_percentage = random.uniform(min_percentage, max_percentage)
#             birthdate = generate_birthdate(age_groups[age_group])

#             # Update the row with the new values
#             row.extend([age_group, birthdate])

#             # Write the updated row to the new CSV file
#             writer.writerow(row)


# import csv
# import random

# # Read the CSV file with names
# with open('updated_names.csv', 'r') as file:
#     reader = csv.reader(file)
#     headers = next(reader)  # Read and store the header row
#     rows = list(reader)  # Convert the reader to a list to shuffle the rows

#     # Shuffle the rows randomly
#     random.shuffle(rows)

#     # Create a new CSV file with shuffled entries
#     with open('shuffled_names.csv', 'w', newline='') as outfile:
#         writer = csv.writer(outfile)
#         writer.writerow(headers)  # Write the header row

#         for row in rows:
#             writer.writerow(row)

# import csv
# import random

# # Read the CSV file
# with open('updated_names.csv', 'r') as file:
#     reader = csv.reader(file)
#     headers = next(reader)  # Read and store the header row

#     # Shuffle the entries
#     entries = list(reader)
#     random.shuffle(entries)

#     # Create a new CSV file with shuffled entries and rearranged columns
#     with open('shuffled_names.csv', 'w', newline='') as outfile:
#         writer = csv.writer(outfile)
#         writer.writerow(['name1', 'name2', 'gender', 'birthdate', 'age'])

#         for row in entries:
#             name1 = row[0]
#             name2 = row[1]
#             gender = row[2]
#             birthdate = row[3]
#             age = row[4]

#             writer.writerow([name1, name2, gender, birthdate, age])

# import csv

# # Read the shuffled CSV file
# with open('shuffled_names.csv', 'r') as file:
#     reader = csv.reader(file)
#     headers = next(reader)  # Read and store the header row

#     # Initialize counters for each age group
#     age_group_counts = {
#         '18-25': 0,
#         '26-35': 0,
#         '36-45': 0,
#         '46-55': 0,
#         '56 and above': 0
#     }

#     total_entries = 0

#     # Iterate over the shuffled entries
#     for row in reader:
#         age = int(row[4])
#         if 18 <= age <= 25:
#             age_group_counts['18-25'] += 1
#         elif 26 <= age <= 35:
#             age_group_counts['26-35'] += 1
#         elif 36 <= age <= 45:
#             age_group_counts['36-45'] += 1
#         elif 46 <= age <= 55:
#             age_group_counts['46-55'] += 1
#         elif age >= 56:
#             age_group_counts['56 and above'] += 1

#         total_entries += 1

#     # Calculate and print the percentage for each age group
#     print('Age Group\tPercentage')
#     for age_group, count in age_group_counts.items():
#         percentage = (count / total_entries) * 100
#         print(f'{age_group}\t{percentage:.2f}%')

# import csv

# # Read the shuffled CSV file
# with open('shuffled_names.csv', 'r') as file:
#     reader = csv.reader(file)
#     headers = next(reader)  # Read and store the header row

#     # Create a new CSV file for updated entries
#     with open('updated_shuffled_names.csv', 'w', newline='') as outfile:
#         writer = csv.writer(outfile)
#         writer.writerow(headers)

#         # Iterate over the shuffled entries
#         for row in reader:
#             name1 = row[0]
#             name2 = row[2]
#             gender = row[1]  # Assuming the gender column is in index 2
#             birthdate = row[3]
#             age = row[4]

#             # Convert gender entry to 'Male' or 'Female'
#             if gender.lower() == 'm' or gender.lower() == 'boy':
#                 gender = 'Male'
#             elif gender.lower() == 'f' or gender.lower() == 'girl':
#                 gender = 'Female'

#             # Write the updated row to the new CSV file
#             writer.writerow([name1, name2, gender, birthdate, age])

# import csv
# import random

# # Read the CSV file
# with open('./updated_shuffled_names.csv', 'r') as file:
#     reader = csv.reader(file)
#     headers = next(reader)  # Read and store the header row

#     # Add the 'id_number' header to the existing headers
#     headers.append('id')

#     # Iterate over the CSV rows and update each row with a random ID number based on age
#     updated_rows = []
#     for row in reader:
#         age = int(row[4])  # Assuming age is in the 5th column (index 4)

#         # Generate a random ID number based on age
#         id_number = random.randint(10000000, 99999999 - age)

#         # Append the ID number to the current row
#         row.append(str(id_number))

#         # Append the updated row to the list of updated rows
#         updated_rows.append(row)

# # Write the updated rows to a new CSV file
# with open('users.csv', 'w', newline='') as outfile:
#     writer = csv.writer(outfile)
#     writer.writerow(headers)
#     writer.writerows(updated_rows)

# import csv

# # Read the CSV file
# with open('./users.csv', 'r') as file:
#     reader = csv.reader(file)
#     headers = next(reader)  # Read and store the header row

#     # Find the maximum existing ID number
#     existing_ids = set()
#     for row in reader:
#         existing_ids.add(int(row[5]))  # Assuming ID number is in the 6th column (index 5)
#     max_existing_id = max(existing_ids)

#     # Calculate the ID range for rearranging
#     id_range = max_existing_id - 10000000 + 1

#     # Rearrange the ID numbers based on age
#     updated_rows = []
#     for row in reader:
#         age = int(row[4])  # Assuming age is in the 5th column (index 4)

#         # Assign the rearranged ID number
#         id_number = max_existing_id - age

#         # Append the ID number to the current row
#         row.append(str(id_number))

#         # Append the updated row to the list of updated rows
#         updated_rows.append(row)

# # Write the updated rows to a new CSV file
# with open('updated_user.csv', 'w', newline='') as outfile:
#     writer = csv.writer(outfile)
#     writer.writerow(headers)
#     writer.writerows(updated_rows)
# import csv

# # Read the CSV file
# with open('users.csv', 'r') as file:
#     reader = csv.reader(file)
#     headers = next(reader)  # Read and store the header row

#     # Create a dictionary to store the ID numbers for each row
#     id_numbers = {}

#     # Update the ID numbers based on age
#     for row in reader:
#         age = int(row[4])  # Assuming age is in the 5th column (index 4)

#         # Assign the ID number based on age
#         id_numbers[row[5]] = max(id_numbers.get(row[5], 0), age)

#     # Reset the file pointer to the beginning of the file
#     file.seek(0)
#     next(reader)  # Skip the header row

#     # Update the rows with rearranged ID numbers based on age
#     updated_rows = []
#     for row in reader:
#         id_number = id_numbers[row[5]]

#         # Update the ID number in the row
#         row[5] = str(id_number)

#         # Append the updated row to the list of updated rows
#         updated_rows.append(row)

# # Write the updated rows to a new CSV file
# with open('a.csv', 'w', newline='') as outfile:
#     writer = csv.writer(outfile)
#     writer.writerow(headers)
#     writer.writerows(updated_rows)

# import csv

# # Read the CSV file
# with open('./users.csv', 'r') as file:
#     reader = csv.reader(file)
#     headers = next(reader)  # Read and store the header row

#     # Create a dictionary to store the age and ID mapping
#     age_id_mapping = {}

#     # Update the dictionary with age and ID information from each row
#     for row in reader:
#         age = int(row[4])  # Assuming age is in the 5th column (index 4)
#         id_number = int(row[5])  # Assuming ID number is in the 6th column (index 5)

#         age_id_mapping[age] = id_number

#     # Find the maximum and minimum ages
#     min_age = min(age_id_mapping.keys())
#     max_age = max(age_id_mapping.keys())

#     # Rearrange the ID numbers based on age
#     for age in age_id_mapping.keys():
#         age_id_mapping[age] = max_age - (age - min_age)

#     # Reset the file pointer to the beginning of the file
#     file.seek(0)
#     next(reader)  # Skip the header row

#     # Update the rows with rearranged ID numbers based on age
#     updated_rows = []
#     for row in reader:
#         age = int(row[4])  # Assuming age is in the 5th column (index 4)
#         id_number = age_id_mapping[age]

#         # Update the ID number in the row
#         row[5] = str(id_number)

#         # Append the updated row to the list of updated rows
#         updated_rows.append(row)

# # Write the updated rows to a new CSV file
# with open('aa.csv', 'w', newline='') as outfile:
#     writer = csv.writer(outfile)
#     writer.writerow(headers)
#     writer.writerows(updated_rows)


# import csv

# # Read the CSV file
# with open('users.csv', 'r') as file:
#     reader = csv.reader(file)
#     headers = next(reader)  # Read and store the header row

#     # Sort the rows based on age
#     sorted_rows = sorted(reader, key=lambda row: int(row[4]))  # Assuming age is in the 5th column (index 4)

# # Rearrange the columns in the desired order
# rearranged_rows = [row[:2] + [row[3], row[2], row[4], row[5]] for row in sorted_rows]

# # Write the sorted and rearranged rows to a new CSV file
# with open('aaa.csv', 'w', newline='') as outfile:
#     writer = csv.writer(outfile)
#     writer.writerow(['name1', 'name2', 'gender', 'birthdate', 'age', 'id_number'])
#     writer.writerows(rearranged_rows)


# import csv

# # Read the CSV file
# with open('aaa.csv', 'r') as file:
#     reader = csv.reader(file)
#     headers = next(reader)  # Read and store the header row

#     # Extract the ID numbers from the 'users' CSV file
#     id_numbers = [row[5] for row in reader]  # Assuming the ID number column is in the 6th column (index 5)

# # Write the extracted ID numbers to a new CSV file
# with open('id_numbers.csv', 'w', newline='') as outfile:
#     writer = csv.writer(outfile)
#     writer.writerow(['id_number'])
#     writer.writerows([[id_number] for id_number in id_numbers])

# import csv

# # Read the 'id_numbers' CSV file
# with open('id_numbers.csv', 'r') as file:
#     reader = csv.reader(file)
#     headers = next(reader)  # Read and store the header row

#     # Sort the ID numbers in descending order
#     id_numbers = sorted(reader, key=lambda row: int(row[0]), reverse=True)

# # Write the sorted ID numbers to a new CSV file
# with open('id_numbers_sorted.csv', 'w', newline='') as outfile:
#     writer = csv.writer(outfile)
#     writer.writerow(headers)
#     writer.writerows(id_numbers)
# import csv

# # Read the sorted ID numbers from the 'id_numbers_sorted' CSV file
# with open('id_numbers_sorted.csv', 'r') as file:
#     reader = csv.reader(file)
#     next(reader)  # Skip the header row
#     id_numbers = [row[0] for row in reader]

# # Read the 'aaa' CSV file and replace the 'id_number' column
# with open('aaa.csv', 'r') as file:
#     reader = csv.reader(file)
#     headers = next(reader)  # Read and store the header row
#     rows = list(reader)  # Convert the reader to a list to access rows by index

# # Replace the 'id_number' column in the 'aaa' rows with the sorted ID numbers
# for i, row in enumerate(rows):
#     row[-1] = id_numbers[i]  # Assuming 'id_number' is the last column

# # Write the updated 'aaa' rows to a new CSV file
# with open('aaa_updated.csv', 'w', newline='') as outfile:
#     writer = csv.writer(outfile)
#     writer.writerow(headers)
#     writer.writerows(rows)

# import csv
# import random

# # Read the 'aaa_updated.csv' file
# with open('aaa_updated.csv', 'r') as file:
#     reader = csv.reader(file)
#     headers = next(reader)  # Read and store the header row
#     rows = list(reader)  # Convert the reader to a list to access rows by index

# # Shuffle the rows
# random.shuffle(rows)

# # Write the shuffled rows to a new CSV file
# with open('aaa_shuffled.csv', 'w', newline='') as outfile:
#     writer = csv.writer(outfile)
#     writer.writerow(headers)
#     writer.writerows(rows)


import csv
from datetime import datetime
from django.contrib.auth.models import User
from myapp.models import UserProfile  # Replace 'myapp' with the actual name of your Django app

# Read the shuffled CSV file
# with open('../etc/aaa_shuffled.csv', 'r') as file:
#     reader = csv.DictReader(file)
#     for row in reader:
#         first_name = row['name1']
#         last_name = row['name2']
#         gender = row['gender']
#         birthdate = datetime.strptime(row['birthdate'], '%Y-%m-%d').date()
#         age = int(row['age'])
#         id_number = row['id_number']

#         # Map the gender values from "Female" to "F" and "Male" to "M"
#         if gender == "Female":
#             gender = "F"
#         elif gender == "Male":
#             gender = "M"

#         # Create a new user with the id number as the username and the birthdate as the password
#         user = User.objects.create_user(username=id_number, password=str(birthdate))

#         # Create a new UserProfile instance
#         profile = UserProfile.objects.create(
#             id_number=id_number,
#             user=user,
#             age=age,
#             dob=birthdate,
#             first_name=first_name,
#             last_name=last_name,
#             gender=gender,
#         )
#         print(first_name,last_name,id_number,age)


# from random import sample

# def transfer_user_profiles_to_voters(percentage=0.99, voter_limit=100):
#     # Retrieve a percentage of UserProfile objects
#     user_profiles = UserProfile.objects.all()
#     num_profiles = int(len(user_profiles) * percentage)
#     selected_user_profiles = sample(list(user_profiles), num_profiles)

#     # Retrieve the first polling stations with available slots
#     polling_stations = PollingStation.objects.all()
#     available_stations = polling_stations.filter(voter_no__lt=voter_limit)[:num_profiles]

#     # Iterate over selected UserProfiles and assign them to polling stations
#     for i, user_profile in enumerate(selected_user_profiles):
#         if i >= len(available_stations):
#             break  # Stop assigning if there are no more available stations

#         # Create a Voter instance and assign it to the selected polling station
#         polling_station = available_stations[i]
#         voter = Voter.objects.create(profile=user_profile, station=polling_station)
#         polling_station.voters.add(voter)
#         polling_station.voter_no += 1
#         polling_station.save()

# from django.contrib.auth.models import User
# from yourapp.models import UserProfile, Voter

# def ppp():
#     # Get all UserProfiles that are not registered as voters
#     user_profiles = UserProfile.objects.all()

#     for profile in user_profiles:
#         try: 
#             voter = Voter.objects.get(profile=profile)
#         except:
#             # Create a Voter instance for the UserProfile
#             voter = Voter.objects.create(
#                 profile=profile,
#                 id=profile.id_number,
#                 # Set other fields as needed
#             )         

#             print(f"Added Voter: {voter}")

#     print("Voter creation completed.")

# # Run the script
# add_voters_from_userprofiles()

def ppp():
    polling_centers = PollingCenter.objects.all()

    for center in polling_centers:
        stations = PollingStation.objects.filter(center=center)
        if len(stations) > 5:
            added_voters = Voter.objects.filter(center__isnull=True)[:500]

            for voter in added_voters:
                # Create a Voter instance and associate it with the center
                voter.center=center
                voter.save()
                print(f"Added Voter {voter} to Polling Center {center}")

    print("Voter addition to polling centers completed.")

