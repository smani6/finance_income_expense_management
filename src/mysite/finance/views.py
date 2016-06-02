from django.shortcuts import render
from django.http import HttpResponse
from django.views.generic import View
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.contrib.auth import authenticate, logout, login
import json
from models import *
from utils import Utils
from models import CustomUser, Account
from django import forms
from django.utils import timezone
from forms import AccountForm
from django.template import RequestContext
import config as CONFIG
from parser_manager import Parser
# Create your views here.
import logging
log = logging.getLogger(__name__)


def index(request):
    return HttpResponse("Hello World")


class Website(View):

    def get(self, request):
        return render(request, 'finance/website1.html')


class SignUp(View):

    def get(self, request):
        return render(request, 'finance/signup.html')

    def post(self, request):
        try:
            log.info("Entering SignUp View")
            log.debug("Signup Customer Request Details - {0}".format(request.POST))

            form = AccountForm(request.POST)
            if form.is_valid():
                log.debug("Form is Valid")
                log.debug(
                    Account.objects.filter(
                        email=request.POST.get('email'),
                        phone_number=request.POST.get('phone_number')))

                is_account_already_exits_with_email = Account.objects.filter(
                    email=request.POST.get('email'))

                if is_account_already_exits_with_email:
                    return render(
                        request, 'finance/signup.html', {
                            'context_dict': 'Account already exists with the email provided'})

                is_account_already_exits_with_phone_number = Account.objects.filter(
                    email=request.POST.get('phone_number'))

                if is_account_already_exits_with_phone_number:
                    return render(request,
                                  'finance/signup.html',
                                  {'context_dict': 'Account already exists with the phone number provided'})

                model_instance = form.save(commit=False)
                model_instance.created_by = 'customer'
                model_instance.created_datetime = timezone.now()
                model_instance.save()
                request.session['account_id'] = model_instance.account_id
                log.debug(
                    "Account Created Successfully and added account_id to session - {0}".format(request.session['account_id']))

                return HttpResponseRedirect(reverse('dashboard'))

            else:
                log.debug("Form is not Valid")
                form = AccountForm()
                extra_context = {}
                extra_context['form'] = form
                return render('finance/signup.html', extra_context,
                              context_instance=RequestContext(request))

        except Exception as e:
            log.error(e)
            log.error(form.errors)


class Login(View):

    def get(self, request):
        return render(request, 'finance/login.html')

    def post(self, request):

        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(username=username, password=password)

        if user is not None:
            login(request, user)
            cu = CustomUser.objects.get(user_id=user.id)
            request.session['account_id'] = cu.Account_id
            return HttpResponseRedirect(reverse('dashboard'))
        else:
            return render(request, 'finance/login.html', {
                'context_dict': 'The username or password were incorrect'})


class Dashboard(View):

    def get(self, request):
        log.info("Entering Dashboard View")
        log.debug("Account id from session - {0}".format(request.session.get('account_id')))
        account_id = request.session.get('account_id')
        util_obj = Utils()
        context_dict = util_obj.get_dashboard_info(account_id)
        log.debug("context_dict values - {0}".format(context_dict))
        log.info("Exiting Dashboard View")
        return render(request, 'finance/index.html', {'dashboard_details': context_dict})


class CharView(View):

    def post(self, request):
        try:
            log.info("Entering ChartView Get Method")
            log.debug("Account id from session - {0}".format(request.session.get('account_id')))
            account_id = request.session.get('account_id')
            input_request = json.loads(request.body)
            log.debug(
                "Incoming Ajax Request - Request for chart info - {0}".format(input_request))

            chart_method_mapper = {
                "income": "get_income_info",
                "expense": "get_expense_info",
                "net_worth": "get_networth_info"
            }

            util_obj = Utils()
            context_dict = getattr(
                util_obj,
                chart_method_mapper[
                    input_request['chart_type']])(account_id)

#             context_dict = {
#                 "type": "income_info",
#                 "sub_types": {
#                     "savings": 15,
#                     "others1": 20,
#                     "others2": 30},
#                 "background_color": CONFIG.background_color,
#                 "background_color_name": CONFIG.background_color_name,
#                 "hover_background_color": CONFIG.hoverBackgroundColor,
#                 "chart_description": {"savings": "15%", "others1": "20%", "others2": "30%"}}

            context_dict = Parser().parse(context_dict, 'OBJECT', 'JSON')

            return HttpResponse(context_dict)
        except Exception as e:
            log.error(e)


class Transaction(View):

    def get(self, request):

        try:
            log.info("Entering Transaction View")
            log.debug("Account id from session - {0}".format(request.session.get('account_id')))
            account_id = request.session.get('account_id')

            expense_details = ExpenseInfo.objects.filter(account_id=account_id)
            transact_list = []

            for each_expense in expense_details:
                expense_dict = {}
                expense_dict['trans_type'] = "expense"
                expense_dict['amount'] = str(each_expense.amount)
                expense_dict['date'] = each_expense.date
                expense_dict['description'] = each_expense.description
                expense_dict['trans_subtype'] = each_expense.trans_subtype
                transact_list.append(expense_dict)

            income_details = IncomeInfo.objects.filter(account_id=account_id)
            for each_income in income_details:
                income_dict = {}
                income_dict['trans_type'] = "income"
                income_dict['amount'] = str(each_income.amount)
                income_dict['date'] = each_income.date
                income_dict['description'] = each_income.description
                income_dict['trans_subtype'] = each_income.trans_subtype
                transact_list.append(income_dict)

            return render(request, 'finance/transactions1.html', {'transact_list': transact_list})
        except Exception as e:
            print e

    def post(self, request):
        try:
            log.info("Entering Transaction View")
            log.debug("Account id from session - {0}".format(request.session.get('account_id')))
            account_id = request.session.get('account_id')
            trans_dict = json.loads(request.body)
            trans_map = {'expense': ExpenseInfo, 'income': IncomeInfo}

            model_name = trans_map[trans_dict['trans_type']]
            log.debug("Model selected - {0}".format(model_name))

            account_obj = Account.objects.get(account_id=account_id)
            log.debug("Calling {0} model to insert into table".format(model_name))
            model_obj = model_name(
                account_id=account_obj,
                trans_subtype=trans_dict.get('trans_sub_type'),
                description=trans_dict.get('description'),
                date=trans_dict.get('date'),
                amount=trans_dict.get('amount'),
                tag=trans_dict.get('tags'))
            model_obj.save()

            return HttpResponse("Transaction Added Successfully")

        except Exception as e:
            print e
