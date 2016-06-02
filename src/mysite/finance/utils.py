import logging
log = logging.getLogger(__name__)
from models import IncomeInfo, ExpenseInfo
import config as CONFIG
import decimal


class Utils(object):

    def get_dashboard_info(self, account_id):

        try:
            log.debug("Entering Dashboard Info")
            total_expense = 0
            total_income = 0
            net_worth = 0
            savings = 0
            log.debug("Getting Expense info from table for account_id - {0}".format(account_id))
            expense_details = ExpenseInfo.objects.filter(account_id=account_id)
            log.debug("Expense details - {0}".format(expense_details))
            for expense in expense_details:
                total_expense = total_expense + int(expense.amount)

            income_details = IncomeInfo.objects.filter(account_id=account_id)
            for income in income_details:
                total_income = total_income + int(income.amount)

            savings = total_income - total_expense

            context_dict = {
                'total_income': total_income,
                'total_expense': total_expense,
                'net_worth': net_worth,
                'savings': savings}
            log.debug("Exiting Dashboard Info")
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

    def get_income_info(self, account_id):

        try:
            log.info("Entering get_income_info")
            income_details = IncomeInfo.objects.filter(account_id=account_id)
            log.debug("Income details - {0}".format(income_details))
            context_dict = {}
            sub_types = {}
            chart_description = {}

            total_val = sum(income_info.amount for income_info in income_details)

            for income_info in income_details:
                type = income_info.trans_subtype
                percentage_val = self.percentage(income_info.amount, total_val)
                sub_types.update({type: "{:.0f}".format(percentage_val)})
                chart_description.update({type: "{:.0f}".format(percentage_val) + "%"})

            background_color = []
            background_color_name = []
            hover_background_color_name = []

            for i in range(0, len(sub_types)):
                background_color.append(CONFIG.background_color[i])
                background_color_name.append(CONFIG.background_color_name[i])
                hover_background_color_name.append(CONFIG.hoverBackgroundColor[i])

            context_dict = {
                "type": "income_info",
                "sub_types": sub_types,
                "background_color": background_color,
                "background_color_name": background_color_name,
                "hover_background_color": hover_background_color_name,
                "chart_description": chart_description
            }

            log.debug("Context dict to be returned - {0}".format(context_dict))
            return context_dict

        except Exception as e:
            log.error(e)

    def get_expense_info(self, account_id):

        try:
            log.info("Entering get_expense_info")
            expense_details = ExpenseInfo.objects.filter(account_id=account_id)
            log.debug("Expense details - {0}".format(expense_details))
            context_dict = {}
            sub_types = {}
            chart_description = {}

            total_val = sum(expense_info.amount for expense_info in expense_details)

            for expense_info in expense_details:
                type = expense_info.trans_subtype
                percentage_val = self.percentage(expense_info.amount, total_val)
                sub_types.update({type: "{:.0f}".format(percentage_val)})
                chart_description.update({type: "{:.0f}".format(percentage_val) + "%"})

            background_color = []
            background_color_name = []
            hover_background_color_name = []

            for i in range(0, len(sub_types)):
                background_color.append(CONFIG.background_color[i])
                background_color_name.append(CONFIG.background_color_name[i])
                hover_background_color_name.append(CONFIG.hoverBackgroundColor[i])

            context_dict = {
                "type": "expense_info",
                "sub_types": sub_types,
                "background_color": background_color,
                "background_color_name": background_color_name,
                "hover_background_color": hover_background_color_name,
                "chart_description": chart_description
            }

            log.debug("Context dict to be returned - {0}".format(context_dict))
            return context_dict

        except Exception as e:
            log.error(e)

    def percentage(self, value, total, multiply=True):
        """
        Accepts two integers, a value and a total.

        The value is divided into the total and then multiplied by 100,
        returning its percentage as a float.

        If you don't want the number multiplied by 100, set the 'multiply'
        kwarg to False.

        If one of the numbers is zero, a null value is returned.

        h3. Example usage

            >> import calculate
            >> calculate.percentage(2, 10)
            20.0

        h3. Documentation

            * "percentage":http://en.wikipedia.org/wiki/Percentage

        """
        if not isinstance(value, (int, long, float, decimal.Decimal)):
            return ValueError(
                'Input values should be a number, your first input is a %s' %
                type(value))
        if not isinstance(total, (int, long, float, decimal.Decimal)):
            return ValueError(
                'Input values should be a number, your second input is a %s' %
                type(total))
        try:
            percent = float(value) / float(total)
            if multiply:
                percent = percent * 100
            return percent
        except ZeroDivisionError:
            return None
