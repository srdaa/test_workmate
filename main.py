from tabulate import tabulate
import csv
import argparse
from exceptions import *
import re


parser: argparse.ArgumentParser = argparse.ArgumentParser()
parser.add_argument("-f", "--file", help="Путь к файлу")
parser.add_argument("-w", "--where", help="Условие фильтрации в формате column=/</>value")
parser.add_argument("-a", "--aggregate", help="Условие для агрегации в формате column=min/max/avg")
parser.add_argument("-o", "--order-by", help="Условие для сортировки в формате column=desc/asc")
args: argparse.Namespace = parser.parse_args()

def read_csv(file: str) -> list[dict]:
    result_table: list[dict] = []

    with open(args.file, "r") as file:
        read: csv.DictReader = csv.DictReader(file, delimiter=',', quotechar='|')
        for string in read:
            result_table.append(string)
    
    return result_table



def where(table: list[dict], args: str) -> list[dict]:
    column = None
    try:
        column, sep, value = re.split(r'([=<>])', args)
        if value == '':
            raise EmptyValue()
        
        if sep == "=":
            return [i for i in table if i[column] == value]
        
        if sep == "<":
            return [i for i in table if int(i[column]) < int(value)]
        
        if sep == ">":
            return [i for i in table if int(i[column]) > int(value)]
    except KeyError:
        raise InvalidColumnName(column_name=column)
    except ValueError:
        raise InvalidFormat()



def order_by(table: list[dict], args:str) -> list[dict]:
    column = None
    try:
        column, value = args.split("=")
        if value == '':
            raise EmptyValue()
        
        if value == 'asc':
            return sorted(table, key= lambda x: x[column])
        
        if value == 'desc':
            return sorted(table, key= lambda x: x[column], reverse=True)
        
        else:
            raise InvalidOrderByValue(value)
    except KeyError:
        raise InvalidColumnName(column_name=column)
    except ValueError:
        raise InvalidFormat()


def aggregate(table: list[dict], args: str) -> list[dict[str, int]] :
    column, value = None, None
    
    try:
        column, value = args.split("=")
        if value == '':
            raise EmptyValue()
        numbers: list[int] = [int(i[column]) for i in table]
        if value == "min":
            return [{"min": min(numbers)}]
        elif value == "max":
            return [{"max": max(numbers)}]
        elif value == "avg":
            return [{"avg": sum(numbers) / len(numbers)}]
        else:
            raise InvalidAggregateValue(value)
    except KeyError:
        raise InvalidColumnName(column_name=column)
    except ValueError:
        print(column, value)
        raise InvalidFormat()


def main() -> None:
    result_table: list[dict] = read_csv(file=args.file)
    
    if args.where:
        try:
            result_table = where(table=result_table, args=args.where)
        except BaseException as e:
            print(e.message)
            return 

    if args.order_by:
        try:
            if result_table:
                result_table = order_by(table=result_table, args=args.order_by)
        except BaseException as e:
            print(e.message)
            return 

    if args.aggregate:
        try:
            if result_table:
                result_table: list[dict[str, int]] = aggregate(table=result_table, args=args.aggregate)
            else:
                return None
        except BaseException as e:
            print(e.message)
            return 
    
    print(tabulate(result_table, headers="keys"))


if __name__ == "__main__":
    main()