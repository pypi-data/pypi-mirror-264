import torch
import numpy as np
import matplotlib.pyplot as plt
from dataclasses import dataclass


@dataclass
class GD_output:
    parameters: dict = None
    per_step_objectives: torch.Tensor = None
    per_epoch_objectives: torch.Tensor = None
    epoch_step_nums: torch.Tensor = None
    grad_steps: range = None
    lr: float = None
    num_steps: int = None
    decay_rate: float = None
    beta1: float = None
    beta2: float = None
    batch_size: int = None
    num_epochs: int = None
    max_steps: int = None
    type_flag: str = None

    def __str__(self):
        print_string = ""
        if self.type_flag == "gd":
            print_string += "=" * 30 + " GRADIENT DESCENT OUTPUT " + "=" * 30
            print_string += f"\nlearning rate: {self.lr}, decay rate: {self.decay_rate}, gradient steps: {self.num_steps}"
        elif self.type_flag == "sgd":
            print_string += "=" * 30 + " STOCHASTIC GRADIENT DESCENT OUTPUT " + "=" * 30
            print_string += (
                f"\nlearning rate: {self.lr}, decay rate: {self.decay_rate},"
                f" batch size: {self.batch_size}, number of epochs: {self.num_epochs}, gradient steps: {self.num_steps}"
            )
        elif self.type_flag == "adam":
            print_string += "=" * 30 + " ADAM OUTPUT " + "=" * 30
            print_string += (
                f"\nlearning rate: {self.lr}, batch size: {self.batch_size}, gradient steps: {self.num_steps},"
                f" number of epochs: {self.num_epochs}, beta1: {self.beta1}, beta2: {self.beta2}"
            )
        for key, parameter in self.parameters.items():
            print_string += f"\n\nparameter {key}:\n{parameter}"
        if self.type_flag == "gd":
            print_string += f"\n\nobjectives:\n{self.per_step_objectives}"
        else:
            print_string += f"\n\nper-step objectives:\n{self.per_step_objectives}"
            print_string += (
                f"\n\nper-epoch mean objectives:\n{self.per_epoch_objectives}"
            )
            print_string += f"\n\nepochs began/completed on the follow gradient steps:\n{self.epoch_step_nums}"
        return print_string


def plot_gd(
    gd_output,
    log=False,
    w=5,
    h=4,
    plot_title=True,
    plot_title_string="gradient descent",
    parameter_title=True,
    show_step=True,
    show_epoch=True,
    show_xlabel=True,
    xlabel="gradient steps",
    show_ylabel=True,
    ylabel="objective",
    legend=False,
    per_step_alpha=0.25,
    per_step_color=None,
    per_step_label=None,
    per_epoch_color=None,
    per_epoch_label=None,
    ax=None,
):
    if ax is None:
        ax = plt.axes()
        plt.gcf().set_size_inches(w=w, h=h)

    per_step_objectives = (
        np.log(gd_output.per_step_objectives) if log else gd_output.per_step_objectives
    )

    if show_step:
        ax.plot(
            gd_output.grad_steps,
            per_step_objectives,
            alpha=per_step_alpha,
            color=per_step_color,
            label=per_step_label,
        )

    if gd_output.type_flag != "gd":
        per_epoch_objectives = (
            np.log(gd_output.per_epoch_objectives)
            if log
            else gd_output.per_epoch_objectives
        )
        if show_epoch:
            ax.plot(
                gd_output.epoch_step_nums,
                per_epoch_objectives,
                color=per_epoch_color,
                label=per_epoch_label,
                marker="o",
            )

    if show_xlabel:
        ax.set_xlabel(xlabel)
    if show_ylabel:
        ax.set_ylabel(ylabel)

    if plot_title | parameter_title:
        if gd_output.type_flag == "gd":
            parameter_title_string = (
                f"$\\alpha=${gd_output.lr}, $\\beta=${gd_output.decay_rate}"
            )
        else:
            parameter_title_string = f"$\\alpha=${gd_output.lr}, $\\beta=${gd_output.decay_rate}, $k=${gd_output.batch_size}, $N=${gd_output.num_epochs}"

        if plot_title & parameter_title:
            title_string = plot_title_string + "\n" + parameter_title_string
            ax.set_title(title_string)
        elif plot_title:
            ax.set_title(plot_title_string)
        else:
            ax.set_title(parameter_title_string)

    if legend:
        ax.legend()
