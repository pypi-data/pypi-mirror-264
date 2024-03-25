# FinancialYear
- It calculate financial year related issue
<!-- doc updater -->

### update doc
----------------------------------------
<h3> Major Update in function name and stable version <h3>

### To update
```bash
pip install --upgrade financialyear
```
_______________________________________________________________________________________________________________
### Goal
- Input may be in 2022 or 2022-23 in 
- It Returns the start date and end date of a month for a given financial year and month.
________________________________________________________________________________________________________________
-    get financial_month_start_month
    

-    year = "2023-24" and month as int (e.g., 4 for April)

-    month_start_date returns a date like "01-04-2023"

-    month_end_date returns a date like "30-04-2023"

-    month_list returns all months of the financial year from "04-2023" to "03-2024"

-    get test as 2022-23 from a date

 # Example usage:
 ```bash

financial_year = Finyear("2023-24")

print(financial_year.month_start_date(1))  # Output: 01-04-2023

print(financial_year.month_end_date(1))    # Output: 30-04-

print(financial_year.previous_month_dates(month=1))  # return two date like :: (datetime.date(2023, 12, 1), datetime.date(2023, 12, 31))

print(financial_year.month_list())    # Output: ['04-2023', '05-2023', '06-2023', ..., '03-2024']

print(date_to_finyear(date='2022-10-2')) # output : 2022-23

```
