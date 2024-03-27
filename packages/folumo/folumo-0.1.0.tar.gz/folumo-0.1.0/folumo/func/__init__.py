from time import time

flipFlop_ = {}
timer_ = {}


def flipFlop(id_):
    if id_ in flipFlop_:
        flipFlop_[id_] = not flipFlop_[id_]
    else:
        flipFlop_[id_] = False

    return flipFlop_[id_]


class Switch:
    def __init__(self, caseNow):
        self.nowArg = caseNow
        self.cases = {}
        self.default_ = None

    def case(self, arg, break_=True):
        def decorator(func):
            self.cases[func] = (arg, break_)

        return decorator

    def default(self, func):
        self.default_ = func

    def run(self):
        case_matched = False
        for func_name in self.cases:
            if self.cases[func_name][0] == self.nowArg:
                func_name()
                if self.cases[func_name][1]:
                    case_matched = True
                    break

        if not case_matched and self.default_:
            self.default_()


class Timer:
    def __init__(self, ID: str, time_: float | int):
        self.ID = ID
        if ID not in timer_:
            timer_[ID] = {
                'func': None,
                "timeNow": time()
            }

        if time() - timer_[ID]["timeNow"] >= time_:
            func = timer_[ID]["func"]
            if func:
                func()
                del timer_[ID]

    def runTask(self):
        def decorator(func):
            if self.ID in timer_:
                timer_[self.ID]["func"] = func

        return decorator


test1_data = {"flipflop": flipFlop("id")}


def test1():
    for _ in range(10):
        print(test1_data["flipflop"])


test2_data = {"switch": Switch(1223)}


def test2():
    @test2_data["switch"].case(123)
    def a():
        print(123)

    @test2_data["switch"].default
    def default_case():
        print("Default case executed")

    test2_data["switch"].run()


test3_data = {"running": True, "count": 0}


def test3():
    while test3_data["running"]:
        oneSec = Timer("oneSec", 1)

        @oneSec.runTask()
        def run():
            print("hihihihihi")
            test3_data["count"] += 1

            if test3_data["count"] >= 10:
                test3_data["running"] = False


if __name__ == "__main__":
    try:
        test1()
        print("TEST 1 EXECUTED WITHOUT ERRORS")

    except Exception as e:
        print(f"TEST 1 EXECUTED WITH AN ERROR: {e}")

    try:
        test2()
        print("TEST 2 EXECUTED WITHOUT ERRORS")

    except Exception as e:
        print(f"TEST 2 EXECUTED WITH AN ERROR: {e}")

    try:
        test3()
        print("TEST 3 EXECUTED WITHOUT ERRORS")

    except Exception as e:
        print(f"TEST 3 EXECUTED WITH AN ERROR: {e}")
