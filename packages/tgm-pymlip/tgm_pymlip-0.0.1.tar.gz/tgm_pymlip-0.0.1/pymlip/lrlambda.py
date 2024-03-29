from cmath import cos
from math import pi
from icecream import ic
import matplotlib.pyplot as plt
import numpy as np
from random import gauss
from scipy import signal


def clip(val, min_, max_):
    return min_ if val < min_ else max_ if val > max_ else val


class nequip_lr_lambda(object):
    def __init__(self, kwargs: dict = {}, verbose: str = False):
        self.verbose: bool = verbose
        self.length: float = kwargs.get("lambda_lr_length", 100)
        self.min_lr_factor: float = float(kwargs.get("lambda_lr_factor", 1e-4))
        self.noise: float = kwargs.get("lambda_lr_noise", 0)
        self.warmup_length: float = kwargs.get("lambda_lr_warm_length", 0)
        self.warmup_factor: float = kwargs.get("lambda_lr_warm_factor", 0.2)
        self.warmup_order: float = kwargs.get("lambda_lr_warm_order", 1)
        self.anneal_type: str = kwargs.get("lambda_lr_anneal", None)
        self.gamma: float = kwargs.get("lambda_lr_gamma", None)
        self.gamma_min: float = kwargs.get(
            "lambda_lr_gamma_min", min(self.min_lr_factor * 10, 1)
        )

    def __call__(self, epoch: float, verbose: bool = None):
        if epoch < self.warmup_length:
            a = 1 - clip(epoch / self.warmup_length, 0, 1)
            return self.interpolate(
                a**self.warmup_order, verbose, min_val=self.warmup_factor
            )
        else:
            epoch -= self.warmup_length
            original_epoch: float = epoch
            epoch += gauss(0, self.noise)
            epoch = max(0, epoch)

            if self.anneal_type is not None:
                forward: bool = self.anneal_type.lower() in ["forward", "both"]
                backward: bool = self.anneal_type.lower() in ["backward", "both"]

                assert forward or backward

                q, mod = divmod(
                    epoch, self.length / 2 if forward and backward else self.length
                )
                if backward and forward:
                    if q % 2 == 1:
                        epoch = ((self.length / 2) - mod) * 2
                    else:
                        epoch = mod * 2
                elif backward and not forward:
                    epoch = self.length - mod
                else:
                    epoch = mod

            retval = self.func(epoch, verbose=verbose)

            if self.gamma is not None:
                retval = retval * max(self.gamma**original_epoch, self.gamma_min)

            return retval

    def plot(self, max_epoch, label=None, show=True):
        epochs = np.arange(0, max_epoch, 1)
        lrs = np.zeros(epochs.shape)
        for index, epoch in enumerate(epochs):
            lrs[index] = self(epoch, verbose=False)
        plt.plot(epochs, lrs, label=label)
        plt.xlabel("epoch")
        plt.ylabel("learning rate scale factor (0 to 1)")
        plt.ylim(0, 1.2)
        if show:
            plt.show()

    def interpolate(self, a, verbose, min_val=None, max_val=1):
        if min_val is None:
            min_val = self.min_lr_factor

        retval = (min_val * a) + (1 - a)

        if verbose is None:
            verbose = self.verbose

        if verbose and float(a).is_integer():
            ic(locals(), self.__dict__)

        return retval


class constant_value(nequip_lr_lambda):
    def __init__(self, kwargs={}, verbose=False):
        super().__init__(kwargs, verbose=verbose)

    def func(self, epoch, verbose=None):
        return 1


class linear_sweep(nequip_lr_lambda):
    def __init__(self, kwargs={}, verbose=False):
        super().__init__(kwargs, verbose=verbose)

    def func(self, epoch, verbose=None):
        a = clip(epoch / self.length, 0, 1)

        return self.interpolate(a, verbose)


class exp_sweep(nequip_lr_lambda):
    def __init__(self, kwargs={}, verbose=False):
        self.order = kwargs.get("lambda_lr_order", 2)
        super().__init__(kwargs, verbose=verbose)

    def func(self, epoch, verbose=None):
        a = clip(epoch / self.length, 0, 1) ** self.order

        return self.interpolate(a, verbose)


class cos_sweep(nequip_lr_lambda):
    def func(self, epoch, verbose=None):
        a = 1 - ((cos(epoch / self.length * 2 * pi).real + 1) / 2)

        return self.interpolate(a, verbose)


class step_down(nequip_lr_lambda):
    def __init__(self, kwargs={}, verbose=False):
        self.step_factor = kwargs.get("lambda_lr_step_factor", 0.9)
        super().__init__(kwargs, verbose=verbose)

    def func(self, epoch, verbose=None):
        current_step = epoch // self.length

        return max(1 * self.step_factor**current_step, self.min_lr_factor)


if __name__ == "__main__":
    MARKER_SIZE = 10
    SMALL_SIZE = 12
    MEDIUM_SIZE = 14
    BIGGER_SIZE = 16

    plt.rc("font", size=SMALL_SIZE)  # controls default text sizes
    plt.rc("axes", titlesize=SMALL_SIZE)  # fontsize of the axes title
    plt.rc("axes", labelsize=MEDIUM_SIZE)  # fontsize of the x and y labels
    plt.rc("xtick", labelsize=SMALL_SIZE)  # fontsize of the tick labels
    plt.rc("ytick", labelsize=SMALL_SIZE)  # fontsize of the tick labels
    plt.rc("legend", fontsize=SMALL_SIZE)  # legend fontsize
    plt.rc("figure", titlesize=BIGGER_SIZE)  # fontsize of the figure title
    plt.rc("lines", markersize=MARKER_SIZE)

    for gamma in [1, 0.9999, 0.999, 0.995, 0.99, 0.95, 0.9]:
        lr_lambda = cos_sweep(
            {
                "lambda_lr_warm_length": 10,
                "lambda_lr_gamma": gamma,
                "lambda_lr_noise": 0,
            }
        )
        lr_lambda.plot(500, show=False, label=f"Gamma: {gamma}")
    plt.legend()
    plt.show()

    for order in [0.5, 0.75, 1, 1.25, 1.5, 2]:
        lr_lambda = exp_sweep(
            {
                "lambda_lr_warm_length": 10,
                "lambda_lr_gamma": None,
                "lambda_lr_order": order,
                "lambda_lr_anneal": "forward",
                "lambda_lr_noise": 0,
            }
        )
        lr_lambda.plot(500, show=False, label=f"Order: {order}")
    plt.legend()
    plt.show()

    for step_factor in [0.5, 0.75, 0.9, 0.99]:
        lr_lambda = step_down(
            {
                "lambda_lr_warm_length": 100,
                "lambda_lr_gamma": None,
                "lambda_lr_step_factor": step_factor,
                "lambda_lr_noise": 0,
            }
        )
        lr_lambda.plot(500, show=False, label=f"Step Factor: {step_factor}")
    plt.legend()
    plt.show()

    lr_lambda = linear_sweep(
        {"lambda_lr_warm_length": 50, "lambda_lr_gamma": None, "lambda_lr_noise": 0}
    )
    lr_lambda.plot(1000, show=False, label=f"Simple Linear")

    lr_lambda = linear_sweep(
        {
            "lambda_lr_warm_length": 100,
            "lambda_lr_gamma": None,
            "lambda_lr_noise": 10,
        }
    )
    lr_lambda.plot(1000, show=False, label=f"Noisy Linear")

    lr_lambda = linear_sweep(
        {
            "lambda_lr_warm_length": 200,
            "lambda_lr_gamma": 0.999,
            "lambda_lr_anneal": "forward",
            "lambda_lr_noise": 0,
        }
    )
    lr_lambda.plot(1000, show=False, label=f"Decaying Sawtooth")

    lr_lambda = linear_sweep(
        {
            "lambda_lr_warm_length": 250,
            "lambda_lr_gamma": 0.999,
            "lambda_lr_anneal": "both",
            "lambda_lr_noise": 0,
        }
    )
    lr_lambda.plot(1000, show=False, label=f"Decaying Triangle")

    lr_lambda = cos_sweep(
        {
            "lambda_lr_warm_length": 250,
            "lambda_lr_gamma": 0.999,
            "lambda_lr_noise": 0,
        }
    )
    lr_lambda.plot(1000, show=False, label=f"Decaying Cosine")
    plt.legend()
    plt.show()

    lr_lambda = linear_sweep(
        {
            "lambda_lr_warm_length": 100,
            "lambda_lr_length": 900,
            "lambda_lr_noise": 100,
        }
    )
    lr_lambda.plot(1000, show=False, label=f"Noisiest Linear")

    lr_lambda = linear_sweep(
        {
            "lambda_lr_warm_length": 100,
            "lambda_lr_length": 900,
            "lambda_lr_noise": 25,
        }
    )
    lr_lambda.plot(1000, show=False, label=f"Noisier Linear")

    lr_lambda = linear_sweep(
        {
            "lambda_lr_warm_length": 100,
            "lambda_lr_length": 900,
            "lambda_lr_noise": 5,
        }
    )
    lr_lambda.plot(1000, show=False, label=f"Noisy Linear")

    lr_lambda = cos_sweep(
        {
            "lambda_lr_warm_length": 100,
            "lambda_lr_gamma": None,
            "lambda_lr_gamma": 0.999,
            "lambda_lr_noise": 5,
        }
    )
    lr_lambda.plot(1000, show=False, label=f"Noisy Decaying Cosine")

    plt.legend()
    plt.show()

    lr_lambda = cos_sweep(
        {
            "lambda_lr_warm_length": 100,
            "lambda_lr_gamma": 0.995,
            "lambda_lr_noise": 3,
        }
    )
    lr_lambda.plot(500, show=False)
    plt.ylim(0, 1)
    plt.show()
