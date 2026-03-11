from typing import Any, Callable


def log(filename: str = "decorators_log") -> Callable:
    """
    декоратор для функций-отчетов, который записывает в файл результат, который возвращает функция, формирующая отчет
    """

    def my_function(func: Callable[[Any], Any]) -> Callable[[Any], Callable]:
        def wrapper(*args: Any, **kwargs: Any) -> Any:
            with open(filename, "a", encoding="utf-8") as file:
                try:
                    result = func(*args, **kwargs)
                    data = result.to_dict(orient="list")
                    file.write(f"{str(data)}\n")
                except Exception as error:
                    file.write(f"{func.__name__} error: {error}\n")
                else:
                    file.write(f"{func.__name__} ok\n")
                    return result

        return wrapper

    return my_function
