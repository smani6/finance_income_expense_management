from django.shortcuts import render
from django.http import HttpResponse
from django.views.generic import View
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
import json
from .models import * 
from .utils import Utils
# Create your views here.

def index(request):
	return HttpResponse("Hello World")


class Login(View):

	def get(self,request):
		return render(request,'finance/login.html')

	def post(self,request):
		username = request.POST.get('username')
		password = request.POST.get('password')

		return HttpResponseRedirect(reverse('dashboard'))


class Dashboard(View):

	def get(self,request):
		util_obj = Utils()
		context_dict = util_obj.get_dashboard_info()
		return render(request,'finance/dashboard.html',{'dashboard_details':context_dict})


class Transaction(View):

	def get(self,request):
		
		try:
			expense_details = ExpenseInfo.objects.all()
			transact_list = []
			
			for each_expense in expense_details:
				expense_dict = {}
				expense_dict['trans_type'] = "expense"
				expense_dict['amount'] = str(each_expense.amount)
				expense_dict['date'] = each_expense.date
				expense_dict['description'] = each_expense.description
				transact_list.append(expense_dict)
				
			
			income_details = IncomeInfo.objects.all()
			for each_income in income_details:
				income_dict = {}
				income_dict['trans_type'] = "income"
				income_dict['amount'] = str(each_income.amount)
				income_dict['date'] = each_income.date
				income_dict['description'] = each_income.description
				transact_list.append(income_dict)
			
			return render(request,'finance/transactions.html',{'transact_list':transact_list})
		except Exception as e:
			print e
			
	def post(self,request):
		try:
			
			trans_dict = json.loads(request.body)
			trans_map = {'expense' : ExpenseInfo, 'income': IncomeInfo}
			
			model_name = trans_map[trans_dict['trans_type']]
			
			account_obj = Account.objects.get(account_id=1)
			model_obj = model_name(account_id=account_obj,description=trans_dict.get('description'),date=trans_dict.get('date'),amount=trans_dict.get('amount'),tag=trans_dict.get('tags'))
			model_obj.save()
			
			return HttpResponse("Transaction Added Successfully")
	
		except Exception as e:
			print e
	
	
	
	