import pandas as pd
import random
from datetime import date, timedelta, datetime
from django.contrib.auth.models import User

df = pd.read_csv('./names.csv')

def nms():
    for i in range (len(df)):
        gender = df['Gender'][i]
        if gender == 'boy':
            g = "M"
        else:
            g = "F"
        if i % 2 == 0:
            fname = df['Name'][i]
        else:
            lname = df['Name'][i]
            random_date = generate_random_date()
            today = datetime.today()
            years = today.year - random_date.year
            nid = random.randint(10000000, 99999999)
            letters = ['C', 'F']
            occ = random.choice(letters)
            user = User.objects.create_user(f"{nid}","a@m.com",f"{random_date}")
            profile = UserProfile.objects.create(dob=random_date,first_name=fname,last_name=lname,gender=g,occupation=occ,user=user,id_number=nid,age=years)
            print(fname, lname,random_date, years, occ, nid, g, profile)



def generate_random_date():
    start_year = 1920
    end_year = 2005
    start_date = date(start_year, 1, 1)
    end_date = date(end_year, 12, 31)

    time_between_dates = end_date - start_date
    days_between_dates = time_between_dates.days

    random_number_of_days = random.randint(0, days_between_dates)
    random_date = start_date + timedelta(days=random_number_of_days)

    return random_date

# Example usage

