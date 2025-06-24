import pytest
from main import where, aggregate, order_by
import csv
from exceptions import *


mock_data: list[dict] = []

with open("test.csv", "r") as file:
    read: csv.DictReader = csv.DictReader(file, delimiter=',', quotechar='|')
    for string in read:
        mock_data.append(string)

def test_filter():
    value: str = "30"
    column: str = "Age"
    
    args: str = f"{column}={value}"    
    assert where(table=mock_data, args=args) == [i for i in mock_data if i[column] == f"{value}"]
    
    args = f"{column}<{value}"    
    assert where(table=mock_data, args=args) == [i for i in mock_data if int(i[column]) < int(f"{value}")]
    
    args = f"{column}>{value}"    
    assert where(table=mock_data, args=args) == [i for i in mock_data if int(i[column]) > int(f"{value}")]
    
    
def test_aggregate():
    min_age: int = 18
    max_age: int = 89
    avg_age: int = 37.5
    
    args: str = "Age=min"    
    assert aggregate(mock_data, args=args) == [{"min" : min_age}]
    
    args = "Age=max"    
    assert aggregate(mock_data, args=args) == [{"max" : max_age}]
    
    args = "Age=avg"    
    assert aggregate(mock_data, args=args) == [{"avg" : avg_age}]
    

def test_empty_value():
    value: str = ""
    column: str = "Age"
    args: str = f"{column}={value}"
    
    with pytest.raises(EmptyValue):
        where(table=mock_data, args=args)
        
    with pytest.raises(EmptyValue):
        aggregate(table=mock_data, args=args)
        

def test_invalid_column_name():
    value: str = "18"
    column: str = "Aage"
    args: str = f"{column}={value}"
    
    with pytest.raises(InvalidColumnName):
        where(table=mock_data, args=args)
    
    with pytest.raises(InvalidColumnName):
        aggregate(table=mock_data, args=args)
        

def test_invalid_format():
    args: str = "Age+18"
    
    with pytest.raises(InvalidFormat):
        where(table=mock_data, args=args)
        
    with pytest.raises(InvalidFormat):
        aggregate(table=mock_data, args=args)
        
        
def test_invalid_aggregate_value():
    args: str = "Age=Moscow"
    
    with pytest.raises(InvalidAggregateValue):
        aggregate(table=mock_data, args=args)
        
        
def test_order_by():
    column: str = "Age"
    args: str = f"{column}=desc"
    
    assert order_by(table=mock_data, args=args) == sorted(mock_data, key = lambda x: x[column], reverse=True)
    
    column: str = "Age"
    args: str = f"{column}=asc"
    
    assert order_by(table=mock_data, args=args) == sorted(mock_data, key = lambda x: x[column])
    
    
def test_invalid_order_by_value():
    column: str = "Age"
    args: str = f"{column}=faker"
    
    with pytest.raises(InvalidOrderByValue):
        order_by(table=mock_data, args=args)