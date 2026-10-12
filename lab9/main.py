import pandas as pd
import matplotlib.pyplot as plt

file_path_s = 'lab9/staff.csv'
file_path_p = 'lab9/projects.csv' 

df_s = pd.read_csv(file_path_s)
df_p = pd.read_csv(file_path_p)
#1
print("\n Кількість працівників по проектах")
employees_per_project = df_s['current_project_id'].value_counts().sort_index()
print(employees_per_project)
#2
print("\n\n Розподіл рівнів (levels) по проектах: ")
levels_per_project = df_s.groupby(['current_project_id', 'level']).size().unstack(fill_value=0)
print(levels_per_project)
#3
print("\n\n Сумарні зарплати по кожному з проектів: ")
salaries_per_project = df_s.groupby('current_project_id')['salary'].sum()
print("Сумарні зарплати по кожному проекту:")
print(salaries_per_project)
#4
df_p['start_date'] = pd.to_datetime(df_p['start_date'])
df_p['end_date'] = pd.to_datetime(df_p['end_date'])
duration_in_days = (df_p['end_date'] - df_p['start_date']).dt.days
df_p['contract_duration_months'] = duration_in_days / 30.4375
df_p['contract_duration_months'] = df_p['contract_duration_months'].round().astype(int)
df_p['monthly_budget'] = df_p['budget'] / df_p['contract_duration_months']

df_p['monthly_salary_cost'] = df_p['project_id'].map(salaries_per_project)

df_p['monthly_profit'] = df_p['monthly_budget'] - df_p['monthly_salary_cost']

print("\n\nМісячний прибуток по кожному проекту:\n\n")

print(df_p[['project_name', 'monthly_budget', 'monthly_salary_cost', 'monthly_profit']].round(2))

#6
print("\n\n Працівники, що знають Python з ЗП > 3000")
knows_python = df_s['skills'].str.contains('Python', case=False, na=False)

high_salary = df_s['salary'] > 3000
    
filtered_staff = df_s[knows_python & high_salary]
print(filtered_staff[['first_name', 'last_name', 'position', 'salary', 'skills']])
#7
print("\n\n Проекти з прибутковістю > 20%")
df_p['total_salary_cost'] = df_p['monthly_salary_cost'] * df_p['contract_duration_months']
df_p['total_profit'] = df_p['budget'] - df_p['total_salary_cost']
df_p['profitability_margin'] = df_p['total_profit'] / df_p['budget']
highly_profitable_projects = df_p[df_p['profitability_margin'] > 0.20]
print(highly_profitable_projects[['project_name', 'budget', 'total_salary_cost', 'total_profit', 'profitability_margin']])
#8
print("\n\nПроекти з прибутковістю > 20%")

df_p['total_salary_cost'] = df_p['monthly_salary_cost'] * df_p['contract_duration_months']
df_p['total_profit'] = df_p['budget'] - df_p['total_salary_cost']
df_p['profitability_margin'] = df_p['total_profit'] / df_p['budget']

highly_profitable_projects = df_p[df_p['profitability_margin'] > 0.20]
print(highly_profitable_projects[['project_name', 'budget', 'total_salary_cost', 'total_profit', 'profitability_margin']])

print("\n\n аналіз (Senior ЗП +20%)")

total_current_profit = df_p['monthly_profit'].sum()
print(f"Поточний загальний місячний прибуток: {total_current_profit:,.2f}")

df_s_whatif = df_s.copy()
df_s_whatif.loc[df_s_whatif['level'] == 'Senior', 'salary'] *= 1.20
new_salaries_per_project = df_s_whatif.groupby('current_project_id')['salary'].sum()
df_p['new_monthly_salary_cost'] = df_p['project_id'].map(new_salaries_per_project)
df_p['new_monthly_profit'] = df_p['monthly_budget'] - df_p['new_monthly_salary_cost']
total_new_monthly_profit = df_p['new_monthly_profit'].sum()

print(f"Новий загальний місячний прибуток (Senior ЗП +20%): {total_new_monthly_profit:,.2f}")
print(f"Різниця (втрата прибутку): {total_new_monthly_profit - total_current_profit:,.2f}")

#11
print("\n\nНайпопулярніша технологія")
all_skills = df_s['skills'].dropna().str.split(';').explode()
cleaned_skills = all_skills.str.strip().str.split(' \(').str[0]

skill_counts = cleaned_skills.value_counts()

top_skill = skill_counts.idxmax()
top_skill_count = skill_counts.max()

print(f"Найпопулярніша технологія: {top_skill} (володіє {top_skill_count} працівників)")
print("\nПовний рейтинг технологій:")
print(skill_counts)

#9
print("\n\n Побудова кругової діаграми віку")
df_s['birth_date'] = pd.to_datetime(df_s['birth_date'])
today = pd.to_datetime('today')     
df_s['age'] = ((today - df_s['birth_date']).dt.days / 365.25).astype(int)
bins = [0, 30, 40, 50, 150] 

labels = ['До 30', '31-40', '41-50', 'Більше 50']   

df_s['age_group'] = pd.cut(df_s['age'], bins=bins, labels=labels, right=True)

age_distribution = df_s['age_group'].value_counts().sort_index()
print("Розподіл працівників за віком:")
print(age_distribution)

plt.figure(figsize=(8, 8))     
age_distribution.plot(kind='pie', autopct='%1.1f%%', startangle=90, colors=['#ff9999','#66b3ff','#99ff99','#ffcc99'])

plt.title('Віковий розподіл працівників')
plt.ylabel('') 
plt.axis('equal') 
plt.show()
#10
print("\n\nПобудова графіку ЗП від стажу")
x_data = df_s['previous_experience_years']
y_data = df_s['salary']
    
plt.figure(figsize=(10, 6))
    
plt.scatter(x_data, y_data, alpha=0.7, color='blue')
    
plt.title('Залежність зарплати від попереднього стажу')
plt.xlabel('Попередній стаж (роки)')
plt.ylabel('Зарплата ($)')
    
plt.grid(True, linestyle='--', alpha=0.5) # Додаємо сітку
plt.tight_layout()
plt.show()

#5
print("\n\n Візуалізація результатів ")
#Графік 1
plt.figure(figsize=(10, 6))
employees_per_project.plot(kind='bar', color='skyblue')

plt.title('Кількість працівників на кожному проекті (Завдання 1)')
plt.xlabel('ID Проекту')
plt.ylabel('Кількість працівників')
plt.xticks(rotation=0)
plt.grid(axis='y', linestyle='--', alpha=0.7)
plt.tight_layout()
plt.show()

#Графік 2
plt.figure(figsize=(10, 7))
levels_per_project.plot(kind='bar', stacked=True, figsize=(10, 7))
plt.title('Розподіл рівнів працівників по проектах (Завдання 2)')
plt.xlabel('ID Проекту')
plt.ylabel('Кількість працівників')
plt.legend(title='Рівень', bbox_to_anchor=(1.05, 1), loc='upper left')
plt.xticks(rotation=0)
plt.tight_layout()
plt.show()

#Графік 3
plt.figure(figsize=(10, 6))
salaries_per_project.plot(kind='bar', color='lightgreen')

plt.title('Сумарні місячні зарплати по проектах (Завдання 3)')
plt.xlabel('ID Проекту')
plt.ylabel('Сумарна зарплата ($)')
plt.xticks(rotation=0)
plt.grid(axis='y', linestyle='--', alpha=0.7)
plt.tight_layout()
plt.show()

#Графік 4
plt.figure(figsize=(10, 6))
profit_plot_data = df_p.set_index('project_name')['monthly_profit']

profit_plot_data.plot(kind='bar', color='salmon')

plt.title('Оціночний місячний прибуток по проектах (Завдання 4)')
plt.xlabel('Назва проекту')
plt.ylabel('Прибуток ($)')
plt.axhline(0, color='black', linewidth=0.8)
plt.xticks(rotation=0)
plt.grid(axis='y', linestyle='--', alpha=0.7)
plt.tight_layout()
plt.show()
