import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
crimes = pd.read_csv("/content/drive/MyDrive/Crime_Data_from_2020_to_Present.csv/file.csv")
crimes.head()
crimes.info()
crimes["TIME OCC"].head(50)
crimes['TIME OCC'] = crimes['TIME OCC'].astype(str)
def add_leading_and_trailing_zeros(time):
    if len(time) == 1:
        return '000' + time
    elif len(time) == 2:
        return '00' + time
    elif len(time) == 3:
        return '0' + time
    else:
        return time

crimes["TIME OCC"] = crimes["TIME OCC"].apply(add_leading_and_trailing_zeros)
time_error = crimes[crimes['TIME OCC'].str.len() > 4]
time_error
crimes["Date Rptd"] = pd.to_datetime(crimes["Date Rptd"], infer_datetime_format='True')
crimes["DATE OCC"] = pd.to_datetime(crimes["DATE OCC"], infer_datetime_format='True')
crimes[["Date Rptd", "DATE OCC"]].head()
crimes["DATE OCC"] = crimes["DATE OCC"].astype(str)
crimes["DATETIME OCC"] = crimes["DATE OCC"] + " " + crimes["TIME OCC"]
crimes["DATETIME OCC"] = pd.to_datetime(crimes["DATETIME OCC"])
crimes["Year OCC"] = crimes["DATETIME OCC"].dt.year
crimes["Month OCC"] = crimes["DATETIME OCC"].dt.month
crimes["Month Name OCC"] = crimes["DATETIME OCC"].dt.strftime("%b")
crimes["WDay OCC"] = crimes["DATETIME OCC"].dt.strftime("%a")
crimes["Hour OCC"] = crimes["DATETIME OCC"].dt.hour
crimes[["Date Rptd", "DATE OCC", "TIME OCC", "DATETIME OCC",
        "Year OCC", "Month OCC", "Month Name OCC", "WDay OCC", "Hour OCC"]].head()
cols_to_drop = ["DR_NO", "DATE OCC", "TIME OCC", "Crm Cd 2", "Crm Cd 3", "Crm Cd 4", "Cross Street"]
crimes = crimes.drop(cols_to_drop, axis=1)
crimes["Vict Sex"].value_counts()
crimes["Vict Sex"] = crimes["Vict Sex"].astype(str)
crimes["Vict Sex"].value_counts()
def replace_gender_abb(abb):
    if abb == "F":
        return "Female"
    elif abb == "M":
        return "Male"
    elif abb == "X":
        return "Unspecified"
    else:
        return "Unknown"
crimes["Vict Sex"] = crimes["Vict Sex"].apply(replace_gender_abb)
crimes["Weapon Used Cd"].value_counts()
print(crimes.groupby(["Weapon Used Cd", "Weapon Desc"]).size().head(40))
print(crimes.groupby(["Weapon Used Cd", "Weapon Desc"]).size().tail(40))
def weapon_category(code):
    if 100 <= code <= 125:
        return "Firearm"
    elif 200 <= code <= 223:
        return "Sharp Object"
    elif 300 <= code <= 312:
        return "Blunt Object"
    elif code == 400:
        return "Strong Arms"
    elif 500 <= code <= 516:
        return "Other Weapon"
    else:
        return "Null"

crimes["Weapon Used Category"] = crimes["Weapon Used Cd"].apply(weapon_category)
crimes["Weapon Used Category"].value_counts()
crimes.info()
earliest_time = crimes["DATETIME OCC"].min()
latest_time = crimes["DATETIME OCC"].max()

print("Earliest Time:", earliest_time)
print("Latest Time:", latest_time)
crimes_excl_2023 = crimes[crimes["Year OCC"] !=2023]
yrly_crimes = crimes_excl_2023["Year OCC"].value_counts().reset_index()
yrly_crimes.columns = ["Year OCC", "Number Of Crimes"]
yrly_crimes
figure, axes = plt.subplots(1, 2, figsize=(13,9))

# Creating bar graph
barplot = sns.barplot(data=yrly_crimes, x="Year OCC", y="Number Of Crimes", ax=axes[0], palette="rocket")
axes[0].set_xlabel("Year", fontweight="bold", fontsize=12)
axes[0].set_ylabel("Number Of Crimes", fontweight="bold", fontsize=12)
axes[0].set_title("Number Of Crimes Over Years", fontweight="bold", fontsize=14)

# Setting bar labels
for p in barplot.patches:
    barplot.annotate(f"{p.get_height()}", (p.get_x() + p.get_width() / 2, p.get_height()), ha="center", va="bottom", fontsize=9)

#Creating pie chart
sizes1 = yrly_crimes["Number Of Crimes"]
labels1 = yrly_crimes["Year OCC"]

explode = [0.05, 0.05, 0.05]
axes[1].pie(sizes1, labels=labels1, autopct="%1.1f%%", startangle=90, explode=explode, shadow=True)
axes[1].set_title("Distribution Of Crimes by Years", fontweight="bold", fontsize=14)

plt.show()
yrly_crimes_incl2023 = crimes["Year OCC"].value_counts().reset_index()
yrly_crimes_incl2023.columns = ["Year OCC", "Number Of Crimes"]
yrly_crimes_incl2023
plt.figure(figsize=(12, 6))

barplot = sns.barplot(data=yrly_crimes_incl2023, x="Year OCC", y="Number Of Crimes", palette="rocket")
plt.xlabel("Year Of Occurence", fontweight="bold", fontsize=12)
plt.ylabel("Number Of Crimes", fontweight="bold", fontsize=12)
plt.title("Number Of Crimes Over Years", fontweight="bold", fontsize=14)

for p in barplot.patches:
    barplot.annotate(f"{p.get_height()}", (p.get_x() + p.get_width() / 2, p.get_height()), ha="center", va="bottom")
plt.show()
mnthly_crimes = crimes_excl_2023.groupby(["Month Name OCC"]).size().reset_index(name="Number Of Crimes")
print(mnthly_crimes.head())

print("\n")

yrly_mnthly_crimes = crimes_excl_2023.groupby(["Year OCC", "Month Name OCC"]).size().reset_index(name="Number Of Crimes")
print(yrly_mnthly_crimes.head())
figure, axes=plt.subplots(1, 2, figsize=(15, 8))

# Order of months
mnths_order = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
mnthly_crimes["Month Name OCC"] = pd.Categorical(mnthly_crimes["Month Name OCC"], categories=mnths_order, ordered=True)

# First bar plot creation
sns.barplot(data=mnthly_crimes, x="Month Name OCC", y="Number Of Crimes", palette="plasma", ax=axes[0])
axes[0].set_xlabel("Month", fontweight="bold", fontsize=12)
axes[0].set_ylabel("Number Of Crimes", fontweight="bold", fontsize=12)
axes[0].set_title("Number Of Crimes During Months Of The Year", fontweight="bold", fontsize=14)

# Order of months
yrly_mnthly_crimes["Month Name OCC"] = pd.Categorical(yrly_mnthly_crimes["Month Name OCC"], categories=mnths_order, ordered=True)

# Second bar plot creation
sns.barplot(data=yrly_mnthly_crimes, x="Year OCC", y="Number Of Crimes", hue="Month Name OCC", palette="rocket", ax=axes[1])
axes[1].set_xlabel("Year", fontweight="bold", fontsize=12)
axes[1].set_ylabel("Number Of Crimes", fontweight="bold", fontsize=12)
axes[1].set_title("No Of Crimes Throughout The Years, 2020 To 2022", fontweight="bold", fontsize=14)
axes[1].legend(title="Month Of Occurence", bbox_to_anchor=(1.05,1), loc="upper left")

plt.show()

weekly_crimes = crimes_excl_2023.groupby(["WDay OCC"]).size().reset_index(name="Number Of Crimes")
weekly_crimes
plt.figure(figsize=(12, 6))

# Order of days of week
wday_order = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]
weekly_crimes["WDay OCC"] = pd.Categorical(weekly_crimes["WDay OCC"], categories=wday_order, ordered=True)

# Bar plot creation
sns.barplot(data=weekly_crimes, x="WDay OCC", y="Number Of Crimes")
plt.xlabel("Day Of Week", fontweight="bold", fontsize=12)
plt.ylabel("Number Of Crimes", fontweight="bold", fontsize=12)
plt.title("Number Of Crimes Over Days Of Week", fontweight="bold", fontsize=14)

plt.show()

yrly_weekly_crimes = crimes_excl_2023.groupby(["Year OCC", "WDay OCC"]).size().reset_index(name="Number Of Crimes")
yrly_weekly_crimes.head()
plt.figure(figsize=(13,7))

yrly_weekly_crimes["WDay OCC"] = pd.Categorical(yrly_weekly_crimes["WDay OCC"], categories=wday_order, ordered=True)

sns.barplot(data=yrly_weekly_crimes, x="Year OCC", y="Number Of Crimes", hue="WDay OCC")
plt.xlabel("Day Of Week", fontweight="bold", fontsize=12)
plt.ylabel("Number Of Crimes", fontweight="bold", fontsize=12)
plt.title("Number Of Crimes Over Years And Days Of Week", fontweight="bold", fontsize=14)
plt.legend(title="Day Of Week", bbox_to_anchor=(1.05,1), loc="upper left")

plt.show()
gender_crimes = crimes_excl_2023.groupby(["Vict Sex"]).size().reset_index(name="Number Of Crimes")
gender_crimes
yrly_gender_crimes = crimes_excl_2023.groupby(["Year OCC", "Vict Sex"]).size().reset_index(name="Number Of Crimes")
yrly_gender_crimes.head()
figre, axes= plt.subplots(2, 1, figsize=(15, 14))

# Creating barplot
barplot = sns.barplot(data=yrly_gender_crimes, x="Year OCC", y="Number Of Crimes", hue="Vict Sex", ax=axes[1])
axes[1].set_xlabel("Year", fontweight="bold", fontsize=12)
axes[1].set_ylabel("Number Of Crimes", fontweight="bold", fontsize=12)
axes[1].set_title("Distribution Of Victims of Crimes Over Years By Gender", fontweight="bold", fontsize=14)

legend_obj = axes[1].legend(title="Gender", bbox_to_anchor=(1.05,1), loc="upper left")
title = legend_obj.get_title()
title.set_fontsize(11), title.set_fontweight("bold")

# Setting bar labels
for p in barplot.patches:
    barplot.annotate(f"{p.get_height()}", (p.get_x() + p.get_width() / 2, p.get_height()), ha="center", va="bottom", fontsize=9)

# Pie chart data preparation
labels2 = gender_crimes["Vict Sex"]
sizes2 = gender_crimes["Number Of Crimes"]

# Creating pie chart
explode = [0.05, 0.05, 0.05, 0.05]
axes[0].pie(sizes2, labels=labels2, autopct="%0.2f%%", startangle=90, explode=explode, shadow=True)
axes[0].set_title("Distribution Of Victims of Crimes by Gender", fontweight="bold", fontsize=14)


plt.show()
area_crimes = crimes_excl_2023.groupby(["AREA NAME"]).size().reset_index(name="Number Of Crimes")
area_crimes = area_crimes.sort_values(by="Number Of Crimes", ascending=False)
plt.figure(figsize=(13,7))
sns.barplot(data=area_crimes, x="Number Of Crimes", y="AREA NAME", palette="rocket")
plt.xlabel("Number Of Crimes", fontweight="bold", fontsize=12)
plt.ylabel("Area Name", fontweight="bold", fontsize=12)
plt.title("Number Of Crimes Recorded In Different Los Angeles Police Departments", fontweight="bold", fontsize=14)

plt.show()
top_20_crimes = crimes_excl_2023.groupby(["Crm Cd", "Crm Cd Desc"]).size().reset_index(name="Number Of Crimes")
top_20_crimes = top_20_crimes.nlargest(20, "Number Of Crimes")
top_20_crimes
plt.figure(figsize=(15,9))

# Bar plot creation
sns.barplot(data=top_20_crimes, x="Crm Cd", y="Number Of Crimes", palette="rocket",
            order=top_20_crimes.sort_values("Number Of Crimes", ascending=False)["Crm Cd"])
plt.xlabel("Crime Code", fontweight="bold", fontsize=12)
plt.ylabel("Number Of Crimes", fontweight="bold", fontsize=12)
plt.title("Top 20 Crimes", fontweight="bold", fontsize=14)

# Legend creation and tweaking
legend_labels = [f"{code} - {desc}" for code, desc in zip(top_20_crimes["Crm Cd"], top_20_crimes["Crm Cd Desc"])]
legend_obj = plt.legend(legend_labels, title='Crime Codes and Descriptions', bbox_to_anchor=(1.05, 1), loc='upper left')
title = legend_obj.get_title()
title.set_fontsize(12), title.set_fontweight("bold")
plt.show()
top_crimes = [510, 624, 354 ,330, 740]

top_3_crimes = crimes[crimes["Crm Cd"].isin(top_crimes)]
yrly_top_3_crimes = top_3_crimes.groupby(["Year OCC", "Crm Cd Desc"]).size().reset_index(name="Number Of Crimes")
yrly_top_3_crimes = yrly_top_3_crimes.sort_values(by=["Year OCC", "Number Of Crimes"], ascending=[True, False])
yrly_top_3_crimes.head()
plt.figure(figsize=(15, 9))

# Bar plot creation
sns.barplot(data=yrly_top_3_crimes, x="Year OCC", y="Number Of Crimes", hue="Crm Cd Desc")
plt.xlabel("Year", fontweight="bold", fontsize=12)
plt.ylabel("Number Of Crimes", fontweight="bold", fontsize=12)
plt.title("Evolution Of The Top 5 Crimes Over Years", fontweight="bold", fontsize=14)

# Legend creation and tweaking
legend_obj= plt.legend(title="Crime", bbox_to_anchor=(1.05,1), loc="upper left")
title = legend_obj.get_title()
title.set_fontsize(12), title.set_fontweight("bold")

plt.show()
crimes_male = crimes_excl_2023[crimes_excl_2023["Vict Sex"] == "Male"]
crimes_female = crimes_excl_2023[crimes_excl_2023["Vict Sex"] == "Female"]

top_10_crimes_male = crimes_male.groupby(["Vict Sex", "Crm Cd", "Crm Cd Desc"]).size().reset_index(name="No Of Crimes")
top_10_crimes_male = top_10_crimes_male.nlargest(10, "No Of Crimes")

top_10_crimes_female = crimes_female.groupby(["Vict Sex", "Crm Cd", "Crm Cd Desc"]).size().reset_index(name="No Of Crimes")
top_10_crimes_female = top_10_crimes_female.nlargest(10, "No Of Crimes")
figure, axes=plt.subplots(2, 1, figsize=(16, 16))

# First barplot
barplot = sns.barplot(data=top_10_crimes_male, x="Crm Cd", y="No Of Crimes", ax=axes[0], palette="rocket",
            order=top_10_crimes_male.sort_values(by="No Of Crimes", ascending=False)["Crm Cd"])
axes[0].set_xlabel("Crime Code", fontweight="bold", fontsize=12)
axes[0].set_ylabel("Number Of Crimes", fontweight="bold", fontsize=12)
axes[0].set_title("Top 10 Crimes: Male Victims", fontweight="bold", fontsize=14)

# Setting legend
legend = [f"{code} - {description}" for code, description in zip (top_10_crimes_male["Crm Cd"], top_10_crimes_male["Crm Cd Desc"])]
legend_obj = axes[0].legend(legend, title="Crime Codes and Descriptions", bbox_to_anchor=(1.05, 1), loc="upper left")
title = legend_obj.get_title()
title.set_fontsize(12), title.set_fontweight("bold")
# Setting bar labels
for p in barplot.patches:
    barplot.annotate(f"{p.get_height()}", (p.get_x() + p.get_width() / 2, p.get_height()), ha="center", va="bottom", fontsize=11)

# Second barplot
barplot = sns.barplot(data=top_10_crimes_female, x="Crm Cd", y="No Of Crimes", ax=axes[1], palette="magma",
            order=top_10_crimes_female.sort_values(by="No Of Crimes", ascending=False)["Crm Cd"])
axes[1].set_xlabel("Crime Code", fontweight="bold", fontsize=12)
axes[1].set_ylabel("Number Of Crimes", fontweight="bold", fontsize=12)
axes[1].set_title("Top 10 Crimes: Female Victims", fontweight="bold", fontsize=14)

# Setting legend
legend = [f"{code} - {description}" for code, description in zip (top_10_crimes_female["Crm Cd"], top_10_crimes_female["Crm Cd Desc"])]
legend_obj = axes[1].legend(legend, title="Crime Codes and Descriptions", bbox_to_anchor=(1.05, 1), loc="upper left")
title = legend_obj.get_title()
title.set_fontsize(12), title.set_fontweight("bold")

# Setting bar labels
for p in barplot.patches:
    barplot.annotate(f"{p.get_height()}", (p.get_x() + p.get_width() / 2, p.get_height()), ha="center", va="bottom", fontsize=11)

plt.show()
top_20_weapons = crimes_excl_2023.groupby(["Weapon Used Cd", "Weapon Desc"]).size().reset_index(name="Number Of Crimes")
top_20_weapons = top_20_weapons.nlargest(20, "Number Of Crimes")
top_20_weapons.head()
plt.figure(figsize=(16, 12))

# Bar plot generation
sns.barplot(data=top_20_weapons, x="Weapon Used Cd", y="Number Of Crimes", palette="rocket",
            order=top_20_weapons.sort_values(by="Number Of Crimes", ascending=False)["Weapon Used Cd"])
plt.xlabel("Code Of Weapon Used", fontweight="bold", fontsize=12)
plt.ylabel("Number Of Crimes", fontweight="bold", fontsize=12)
plt.title("Top 20 Weapons Used In Criminal Ativities", fontweight="bold", fontsize=14)

# Legend creation and tweaking
legend = [f"{code} - {description}" for code, description in zip (top_20_weapons["Weapon Used Cd"], top_20_weapons["Weapon Desc"])]
legend_obj = plt.legend(legend, title="Weapons Used Codes and Descriptions", bbox_to_anchor=(1.05, 1), loc="upper left")
title = legend_obj.get_title()
title.set_fontsize(12), title.set_fontweight("bold")

plt.show()
weapons_category = crimes_excl_2023[crimes_excl_2023["Weapon Used Category"] != "Null"]
weapons_used = weapons_category.groupby(["Weapon Used Category"]).size().reset_index(name="No Of Crimes")
weapons_used
figure, axes=plt.subplots(1, 2, figsize=(15, 6))

# Bar plot creation
barplot = sns.barplot(data=weapons_used, x="Weapon Used Category", y="No Of Crimes", palette="rocket", ax=axes[0],
            order=weapons_used.sort_values(by="No Of Crimes", ascending= False)["Weapon Used Category"])
axes[0].set_xlabel("Weapons Used", fontweight="bold", fontsize=12)
axes[0].set_ylabel("Number Of Crimes", fontweight="bold", fontsize=12)
axes[0].set_title("Weapons Used In Commiting Crimes", fontweight="bold", fontsize=14)
# Bar labels
for p in barplot.patches:
    barplot.annotate(f"{p.get_height()}", (p.get_x() + p.get_width() / 2, p.get_height()), ha="center", va="bottom")

# Pie chart data preparation
labels3 = weapons_used["Weapon Used Category"]
sizes3 = weapons_used["No Of Crimes"]
explode3 = [0.01, 0.01, 0.01, 0.01, 0.01]

# Pie chart creation
axes[1].pie(sizes3, labels=labels3, autopct="%0.2f%%", explode=explode3, startangle=90, pctdistance=.8, shadow=True)
axes[1].set_title("Distribution Of Weapons Used In Crimes", fontweight="bold", fontsize=14)

plt.show()
gender_weapons = weapons_category.groupby(["Vict Sex", "Weapon Used Category"]).size().reset_index(name="No Of Crimes")
genders = ["Male", "Female"]
gender_weapons = gender_weapons[gender_weapons["Vict Sex"].isin(genders)]
gender_weapons.head()
plt.figure(figsize=(14,7))

# Bar plot creation
barplot = sns.barplot(data=gender_weapons, x="Vict Sex", y="No Of Crimes", hue="Weapon Used Category")
plt.xlabel("Gender Of Victim", fontweight="bold", fontsize=12)
plt.ylabel("Number Of Crimes", fontweight="bold", fontsize=12)
plt.title("Number Of Crimes Against Gender And Weapons Used", fontweight="bold", fontsize=14)
plt.legend(title="Weapon Used", bbox_to_anchor=(1.05,1), loc="upper left")

# Bar labels
for p in barplot.patches:
    barplot.annotate(f"{p.get_height()}", (p.get_x() + p.get_width() / 2, p.get_height()), ha="center", va="bottom")

plt.show()
top_20_premises = crimes_excl_2023.groupby(["Premis Cd", "Premis Desc"]).size().reset_index(name="Number Of Crimes")
top_20_premises = top_20_premises.nlargest(20, "Number Of Crimes")
top_20_premises.head()
plt.figure(figsize=(15,9))

# Bar plot creation
sns.barplot(data=top_20_premises, x="Premis Cd", y="Number Of Crimes", palette="rocket",
           order=top_20_premises.sort_values(by="Number Of Crimes", ascending=False)["Premis Cd"])
plt.xlabel("Premise Code", fontweight="bold", fontsize=12)
plt.ylabel("Number Of Crimes", fontweight="bold", fontsize=12)
plt.title("Top 20 Premises Where Crimes Occured", fontweight="bold", fontsize=14)

# Legend creation and tweaking
legend = [f"{code} - {description}" for code, description in zip (top_20_premises["Premis Cd"], top_20_premises["Premis Desc"])]
legend_obj = plt.legend(legend, title="Premise Codes And Descriptions", bbox_to_anchor=(1.05,1), loc="upper left")
title = legend_obj.get_title()
title.set_fontsize(12), title.set_fontweight("bold")

plt.show()
crimes_status = crimes_excl_2023.groupby("Status Desc").size().reset_index(name="Number Of Crimes")
crimes_status = crimes_status.sort_values(by="Number Of Crimes", ascending=False)
crimes_status = crimes_status[crimes_status["Status Desc"] != "UNK"]

yrly_crimes_status = crimes_excl_2023.groupby(["Year OCC", "Status Desc"]).size().reset_index(name="Number Of Crimes")
yrly_crimes_status = yrly_crimes_status.sort_values(by="Number Of Crimes", ascending=False)
yrly_crimes_status = yrly_crimes_status[yrly_crimes_status["Status Desc"] != "UNK"]
figure, axes=plt.subplots(2, 1, figsize=(16, 16))

# First bar plot creation
barplot=sns.barplot(data=crimes_status, x="Status Desc", y="Number Of Crimes", palette="rocket", ax=axes[0])
axes[0].set_xlabel("Crime Status", fontweight="bold", fontsize=12)
axes[0].set_ylabel("Number Of Crimes", fontweight="bold", fontsize=12)
axes[0].set_title("Number Of Crimes Vs Their Statuses", fontweight="bold", fontsize=14)

# Bar labels
for p in barplot.patches:
    barplot.annotate(f"{p.get_height()}", (p.get_x() + p.get_width()/ 2, p.get_height()), ha="center", va="bottom")

# Second bar plot creation
barplot=sns.barplot(data=yrly_crimes_status, x="Status Desc", y="Number Of Crimes", palette="rocket", hue="Year OCC", ax=axes[1])
axes[1].set_xlabel("Crime Status", fontweight="bold", fontsize=12)
axes[1].set_ylabel("Number Of Crimes", fontweight="bold", fontsize=12)
axes[1].set_title("Number Of Crimes Vs Their Statuses And Years Of Occurence", fontweight="bold", fontsize=14)
axes[1].legend(title="Year Of Occurence")

# Bar labels
for p in barplot.patches:
    barplot.annotate(f"{p.get_height()}", (p.get_x() + p.get_width()/ 2, p.get_height()), ha="center", va="bottom", fontsize=9)

plt.show()
