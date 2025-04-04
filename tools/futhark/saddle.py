import futhark_utils
import numpy as np


def prepare(server, input):
    server.put_value("start", np.float64(input["start"]))


def entry(server, input, variant):
    (o,), times = futhark_utils.run(
        server,
        variant,
        ("output",),
        ("start",),
        input["min_runs"],
        input["min_seconds"],
    )
    return (o.flatten().tolist(), times)


def rr(server, input):
    return entry(server, input, "rr")


def ff(server, input):
    return entry(server, input, "ff")


def fr(server, input):
    return entry(server, input, "fr")


def rf(server, input):
    return entry(server, input, "rf")
