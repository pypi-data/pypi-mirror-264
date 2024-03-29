import typing as t
def yes_or_no(
    question: str,
    assume_return_is_yes: bool = False) -> bool:
    while True:
        answer = input(f"{question} (y/n):")
        ans = answer.strip()
        if ans in ["y", "Y"] or (assume_return_is_yes and ans== ""):
            return True
        elif ans in ["n", "N"]:
            return False
        else:
            print("invalid input, try again")
            continue


def get_positive_integer_input(
    question: str,
    valid_options: t.List[int] = None,
) -> int:
    print(question)
    answer = None
    while answer is None:
        answer = input("Enter a number:")
        answer = answer.strip()
        try:
            answer = int(answer)
        except:
            answer = None
        else:
            answer = answer if answer >= 1 else None
        finally:
            if answer is None:
                print("Not a valid answer")
            else:
                return answer

def get_select_input(
    question: str,
    options: t.List[t.Any],
    option_formatter: t.Callable = lambda option: str(option),
) -> t.Any:
    option_strings = [
        f"{index}) {option_formatter(option)}"
        for index, option in enumerate(options, 1)
    ]
    valid_choices = [f"{index}" for index in range(1, 1 + len(options))]
    print(
        "------------",
        question,
        *option_strings,
        "------------",
        sep="\n"
    )
    answer = None
    while answer is None:
        answer = input("Enter a number:")
        answer = answer.strip()
        if answer not in valid_choices:
            print("Not a valid answer")
            answer = None
            continue
    answer_index = int(answer) - 1
    return options[answer_index]