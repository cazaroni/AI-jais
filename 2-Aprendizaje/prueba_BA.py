import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split

# Import random-forest routines
from bosque_aleatorio import entrena_bosque, predice_bosque

# UCI Adult database
column_names = [
    "age", "workclass", "fnlwgt", "education", "education-num",
    "marital-status", "occupation", "relationship", "race", "sex",
    "capital-gain", "capital-loss", "hours-per-week", "native-country", "income"
]
url = "https://archive.ics.uci.edu/ml/machine-learning-databases/adult/adult.data"
df = pd.read_csv(url, header=None, names=column_names, na_values="?", skipinitialspace=True)

df.dropna(inplace=True)

features = ["age", "fnlwgt", "education-num", "capital-gain", "capital-loss", "hours-per-week"]
df = df[features + ["income"]]

X = df[features]
y = df["income"]
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.3, random_state=1, stratify=y
)

train_df = pd.concat([X_train, y_train.rename("income")], axis=1)

num_trees_list     = [1, 5, 10, 20]
max_depth_list     = [None, 5, 10]
vars_per_node_list = [1, 2, 3]

results = []
for M in num_trees_list:
    for depth in max_depth_list:
        for vars_node in vars_per_node_list:
            print(f"Training forest: M={M}, max_depth={depth}, vars_per_node={vars_node}")
            bosque = entrena_bosque(
                datos=train_df,
                target="income",
                clase_default=y_train.mode()[0],
                M=M,
                max_profundidad=depth,
                min_ejemplos=1,
                num_variables=vars_node
            )
            # Predict on test set
            preds = X_test.apply(lambda row: predice_bosque(bosque, row.to_dict()), axis=1)
            acc = (preds == y_test).mean()
            print(f" → Accuracy: {acc:.4f}\n")
            results.append({
                "num_trees":     M,
                "max_depth":     "None" if depth is None else depth,
                "vars_per_node": vars_node,
                "accuracy":      acc
            })

res_df = pd.DataFrame(results)
print("\n=== Results Summary ===")
print(res_df)

plt.figure(figsize=(8,5))
for vars_node in vars_per_node_list:
    subset = res_df[res_df["vars_per_node"] == vars_node]
    plt.plot(subset["num_trees"], subset["accuracy"], marker='o',
             label=f"vars/node = {vars_node}")
plt.xlabel("Number of Trees (M)")
plt.ylabel("Test Accuracy")
plt.title("Effect of M and vars_per_node on Accuracy")
plt.legend()
plt.grid(True)
plt.tight_layout()
plt.show()
