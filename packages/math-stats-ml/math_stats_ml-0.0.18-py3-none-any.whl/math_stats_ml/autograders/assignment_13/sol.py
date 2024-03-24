import pandas as pd
import torch


def print_type_error(solution):
    return f"\033[91mYour `{solution[1]}` should be a PyTorch tensor. It is not.\n"


### PROBLEM 1 ###

url = "https://raw.githubusercontent.com/jmyers7/stats-book-materials/main/data/data-12-3.csv"
df = pd.read_csv(url)

X = torch.tensor(df.iloc[:, :6].to_numpy(), dtype=torch.float32)
y = torch.tensor(df["y"].to_numpy(), dtype=torch.float32)

torch.manual_seed(57702)
theta0 = torch.rand(size=(6,))
theta1 = torch.rand(size=(6,))
parameters = {"theta0": theta0, "theta1": theta1}


def phi_link(parameters, y):
    theta0 = parameters["theta0"]
    theta1 = parameters["theta1"]
    return (1 - y).reshape(-1, 1) @ theta0.reshape(1, -1) + y.reshape(
        -1, 1
    ) @ theta1.reshape(1, -1)


phi = phi_link(parameters, y)

### PROBLEM 2 ###


def I_model(parameters, X, y):
    phi = phi_link(parameters, y)
    psi = parameters["psi"]
    return (
        -y * torch.log(psi)
        - (1 - y) * torch.log(1 - psi)
        - torch.sum(X * torch.log(phi) + (1 - X) * torch.log(1 - phi), dim=1)
    )


torch.manual_seed(57702)
theta0 = torch.rand(size=(6,))
theta1 = torch.rand(size=(6,))
psi = torch.rand(size=(1,))
parameters = {"theta0": theta0, "theta1": theta1, "psi": psi}

surprisals = I_model(parameters, X, y)

### SOLUTIONS CLASS ###


class Solutions:
    def __init__(self):
        pass

    def get_solutions(self, prob_num):
        match prob_num:
            case 1:
                return [(phi, "phi")]
            case 2:
                return [(surprisals, "surprisals")]
