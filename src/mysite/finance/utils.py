from .models import *
class Utils(object):
    
    def get_dashboard_info(self):
        
        try:
            total_expense = 0
            total_income = 0
            net_worth = 0
            savings = 0
            expense_details = ExpenseInfo.objects.all()
            for expense in expense_details:
                total_expense = total_expense + int(expense.amount)
                
            income_details = IncomeInfo.objects.all()
            for income in income_details:
                total_income = total_income + int(income.amount)
            
            savings = total_income - total_expense
            
            context_dict = {'total_income':total_income,'total_expense':total_expense,'net_worth':net_worth,'savings':savings }
            return context_dict
        
        except Exception as e:
            raise
        
    def process_expense_info(self):
        
        try:
            expense_details = ExpenseInfo.objects.all()
            expense_list = []
            
            for each_expense in expense_details:
                expense_dict = {}
                expense_dict['trans_type'] = "expense"
                expense_dict['amount'] = str(each_expense.amount)
                expense_dict['date'] = each_expense.date
                expense_dict['description'] = each_expense.description
                expense_list.append(expense_dict)
                    
            return expense_list
        
        except Exception as e:
            raise
    
    def process_income_info(self):
        try:
            income_details = IncomeInfo.objects.all()
            income_list = []
            for each_income in income_details:
                income_dict = {}
                income_dict['trans_type'] = "income"
                income_dict['amount'] = str(each_income.amount)
                income_dict['date'] = each_income.date
                income_dict['description'] = each_income.description
                income_list.append(income_dict)
                
            return income_list
        except Exception as e:
            raise
    
    