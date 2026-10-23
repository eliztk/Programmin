import pandas
import matplotlib.pyplot as plt

print("\n///--- POKEMON.CSV ---///")
pokemon = pandas.read_csv('pokemon.csv')

print("\n--- Перші 5 рядків ---")
print(pokemon.head())
print("\n--- Інформація щодо файлу ---")
pokemon.info()
print("\n--- Назви стовпців ---")
print(pokemon.columns.tolist())
print("\n--- Розмір таблиці ---")
print(pokemon.shape)

print("\n--- Статистика характеристик ---")
print(pokemon.describe())

print("\n--- Частота різних типів ---")
print(pokemon['Type 1'].value_counts())

print("\n--- Типи даних ---")
print(pokemon.dtypes)

print("\n--- Пошук пропусків ---")
print(pokemon.isnull().sum())

pokemon_test = pokemon.copy()
pokemon_test['Type 2'] = pokemon_test['Type 2'].fillna('Unknown')
print(pokemon_test['Type 2'].isnull().sum())

data1 = pokemon.loc[:, ["Attack", "Defense", "Speed"]]

print("\n--- Залежність Attack від Defense ---")
data1.plot(kind="scatter", x="Attack", y="Defense")
plt.show()

print("\n--- Розподіл Defense ---")
data1.plot(
    kind="hist",
    y="Defense",
    bins=50,
    range=(0, 250),
    density=True
)
plt.show()

print("\n///--- COMBATS.CSV ---///")
combats = pandas.read_csv('combats.csv')

print("\n--- Перші 5 рядків ---")
print(combats.head())
print("\n--- Інформація щодо файлу ---")
combats.info()
print("\n--- Назви стовпців ---")
print(combats.columns.tolist())
print("\n--- Розмір таблиці ---")
print(combats.shape)

print("\n--- Скільки разів виявляється переможцем кожен ідентифікатор ---")
print(combats['Winner'].value_counts())

print("\n--- Розподіл кількості перемог покемонів ---")

winner_counts = combats['Winner'].value_counts()

winner_counts.plot(kind='hist', bins=20)
plt.title('Розподіл кількості перемог покемонів')
plt.xlabel('Кількість перемог')
plt.ylabel('Кількість покемонів')
plt.tight_layout()
plt.show()

print("\n///--- TESTS.CSV ---///")
tests = pandas.read_csv('tests.csv')

print("\n--- Перші 5 рядків ---")
print(tests.head())
print("\n--- Інформація щодо файлу ---")
tests.info()
print("\n--- Назви стовпців ---")
print(tests.columns.tolist())
print("\n--- Розмір таблиці ---")
print(tests.shape)

print("\n--- Пошук пропусків ---")
print(tests.isnull().sum())
