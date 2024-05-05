from django.shortcuts import render,redirect
from django.http import JsonResponse, HttpResponseRedirect
from django.views.decorators.csrf import csrf_exempt
from dcf_form.models import Client,Constants,Industry_Beta 
import requests
import json
from datetime import datetime
import random
# Create your views here.

def index(request):
    return render(request,"dcf_form/home.html")


@csrf_exempt
def form(request):
    industries_option=Industry_Beta.objects.all()
   
    years=[]
    number=7
    valuation_data =  '6/12/2021'
    valuation_data = datetime.strptime(valuation_data, '%d/%m/%Y')
    if request.method=="POST":
        print("///////////",request.POST["provisional_date"])
        valuation_data=datetime.strptime(request.POST["provisional_date"], '%Y-%m-%d')
        print(valuation_data.year)
        if valuation_data.month>3:
            projected_year=valuation_data.year+1
            provisional_months_left=12-valuation_data.month+4
        else:
            projected_year=valuation_data.year
            provisional_months_left=4-valuation_data.month
        years=[]
        for i in range(5):
            years.append(projected_year+i)

        provisional_year=projected_year-1
        long=[1,3,5,7,8,10,12]
        if valuation_data.month in long:
            provisional_days_left=(30-valuation_data.day)/31

        else:
            provisional_days_left=(30-valuation_data.day)/30
        
        r={
            "provisional_year":provisional_year,
            "provisional_months_left":provisional_months_left,
            "provisional_days_left":provisional_days_left,
            "last_year":years[-1],
            "first_year":years[0],
        }
        return JsonResponse(r)
        

    if valuation_data.month>3:
        projected_year=valuation_data.year+1
        provisional_months_left=12-valuation_data.month+4
    else:
        projected_year=valuation_data.year
        provisional_months_left=4-valuation_data.month
    years=[]
    for i in range(5):
        years.append(projected_year+i)

    provisional_year=projected_year-1
    long=[1,3,5,7,8,10,12]
    if valuation_data.month in long:
        provisional_days_left=(30-valuation_data.day)/31

    else:
        provisional_days_left=(30-valuation_data.day)/30

    # print(provisional_year)
    # print(provisional_months_left)
    # print( provisional_days_left)
    # for i in range(2,number):
    #     years.append(20+i)
    # print(years)
    coe_constants=Constants.objects.all().last()
    # print("qgfcdhgvjwsbhxkajnlkzm",float(coe_constants.Risk_free_rate))

    context={
        "last_year":years[-1],
        "first_year":years[0],
        "data":[0,1,2,3,4],
        "coe_rows":[["Risk-Free-Rate",float(coe_constants.Risk_free_rate)],["Market-Premium",float(coe_constants.Market_Premium)],["Beta",float(coe_constants.Beta)],["Effective-tax-rate",float(coe_constants.Effective_tax_Rate)]],
        "provisional_year":provisional_year,
        "provisional_months_left":provisional_months_left,
        "provisional_days_left":provisional_days_left,
        "prov_rows":["Operating-Revenue","Operating-Expenses","Employee-Benefit","Other-Expenses","DepreciationAmortization","Finance-Cost","Other-Income","Equity","Debt","Working-Capital-Asset","Other-liabilities","Cash-bank-balance"],
        "rows":["Operating-Revenue","Operating-Expenses","Employee-Benefit","Other-Expenses","DepreciationAmortization","Finance-Cost","Other-Income","Capital-Expenditure"],
        "funds":["Equity","Debt","Other-liabilities","Tangible-Assets","Investments","Working-Capital-Asset"],
        "ind":industries_option
    }
    return render(request, 'dcf_form/form.html',context)

@csrf_exempt
def get_otp(request):
    if request.method=="POST":
        numbers=[1,2,3,4,5,6,7,8,9,0]
        otp=""
        for i in range(6):
            otp+=str(random.choice(numbers))
        print(otp)
        
        phone=request.POST["phone"]
        print(phone)
        url = "https://www.fast2sms.com/dev/bulk"
        payload = "sender_id=FSTSMS&message=Your 6 digit otp is "+otp+"&language=english&route=p&numbers="+phone
        headers = {
        'authorization': "5i0NbKHPyo6v4tIuJeWFxlhBkjsqmTQALwdC7r1RSUGf2E3MnX9Rt8feA2TGlOj5b3HUsq0rwPKZynVF",
        'Content-Type': "application/x-www-form-urlencoded",
        'Cache-Control': "no-cache",
        }
        response = requests.request("POST", url, data=payload, headers=headers)
        print(response.text)
        r = {
            'generated_otp':otp

        }
        return JsonResponse(r)
    return redirect("/")



@csrf_exempt
def save(request):
    if request.method == "POST":
        name = request.POST["name"]
        email = request.POST["email"]
        phone = request.POST["phone"]
        print("name is steve", request.POST["name"])
        new_user = Client.objects.create(
            email=email, name=name, phone=phone)
        new_user.save()
        print("------")
        new_id=Client.objects.all().last().id
        response={
            'final_id':new_id
        }
        print('new user created')
        return JsonResponse(response)
        
    return redirect("/")


@csrf_exempt
def valuate(request):
    if request.method=="POST":
        coe_constants=Constants.objects.all().last()
        provisional_year=float(request.POST.get("provisional_year"))
        
        provisional_months_left=float(request.POST.get("provisional_months_left"))
        provisional_days_left=float(request.POST.get("provisional_days_left"))
        firstyear=int(request.POST.get("firstyear"))
        
        lastyear=int(request.POST.get("lastyear"))

        years=[i for i in range(firstyear,lastyear+1)]
        print(years)
        provisional_inputs=request.POST.get("provisional_arr").split(',')

        for i in range(len(provisional_inputs)):
            provisional_inputs[i]=float(provisional_inputs[i])
        # print(provisional_inputs)

        coe_rows=request.POST.get("coe_rows").split(",")
        for i in range(len(coe_rows)):
            coe_rows[i]=float(coe_rows[i])
        print("!!!!!!!!!",coe_rows)
        ind_type=Industry_Beta.objects.get(id=int(coe_rows[-5]))
        

        opr=request.POST.get("Operating-Revenue").split(',')
        cogs=request.POST.get("Operating-Expenses").split(',')
        eb=request.POST.get("Employee-Benefit").split(',')
        oe=request.POST.get("Other-Expenses").split(',')
        d_a=request.POST.get("DepreciationAmortization").split(',')
        fc=request.POST.get("Finance-Cost").split(',')
        oi=request.POST.get("Other-Income").split(',')
        ta=request.POST.get("Tangible-Assets").split(',')
        inv=request.POST.get("Investments").split(',')
        wca=request.POST.get("Working-Capital-Asset").split(',')
        ol=request.POST.get("Other-liabilities").split(',')
        eq=request.POST.get("Equity").split(',')
        d=request.POST.get("Debt").split(',')
        ce=request.POST.get("Capital-Expenditure").split(",")

        provisional_inputs=[0,0,5.32,500.11,0,0,0,-4.42,4.55,0,0,0.13]
        opr=[0,0,356.69,696.77,1234.24]
        cogs=[0,0,17.83,34.84,61.71]
        oe=[5,7.5,9.45,18.46,32.71]
        eb=[6.65,240,360,432,518.4]
        d_a=[0,1.61,16.82,41.06,71.38,110.73]
        fc=[0,0,0,0,0]
        oi=[0,0,0,0,0]
        eq=[47.32,283.01,511.35,751.43,1187.59]
        d=[4.55,4.55,4.55,4.55,0]
        ol=[0,0,0.74,1.45,2.57]
        ta=[11.25,50.45,123.18,214.15,332.19]
        inv=[0,0,0,0,0]
        wca=[0,10.5,40.67,67.68,109.21]
        ce=[1285797,5601203,11379800,16235390,22876194]

     
        # provisional_inputs=[1000,300,200,100,50,75,25,0,0]
        # opr=[98.11,6703.2,704.53,764.32,824.6]
        # cogs=[51.16,342.03,372.58,396.60,412.30]
        # eb=[9.85,43.35,47.68,52.45,57.69]
        # oe=[37.49,237.03,257.82,26.63,292.36]
        # d_a=[0.13,1.42,1.43,1.45,1.46]
        # fc=[0,0,0,0,0]
        # oi=[0,0,0,0,0]
        # eq=[100.2,100.12,200.44,200.55,300.12]
        # d=[100.11,181.2,100.75,120.44,100.2]
        # ol=[100.1,100.1,100.1,100.1,100.1]
        # ta=[101.22,101.22,101.22,101.22,101.22]
        # inv=[120.3,120.3,120.3,120.3,120.3]
        # wca=[21.7,41.7,31.7,22.7,21.7]
        for i in range(len(opr)):
            opr[i]=float(opr[i])
            cogs[i]=float(cogs[i])
            eb[i]=float(eb[i])
            oe[i]=float(oe[i])
            d_a[i]=float(d_a[i])
            fc[i]=float(fc[i])
            oi[i]=float(oi[i])
            ta[i]=float(ta[i])
            inv[i]=float(inv[i])
            wca[i]=float(wca[i])
            ol[i]=float(ol[i])
            eq[i]=float(eq[i])
            d[i]=float(d[i])
            ce[i]=float(ce[i])
           
          
        
        for i in range(len(provisional_inputs)):
            provisional_inputs[i]=float(provisional_inputs[i])


        ########COE########

        coe = {}
        
        coe['Risk_Free_Rate'] = float(coe_rows[6])/100
        coe['Market_Premium'] = float(coe_rows[7])/100
        coe['Market_Return'] = coe['Risk_Free_Rate'] + coe['Market_Premium']
        if provisional_inputs[8]:
                    coe['Beta'] = ind_type.unlevered_beta
        else:
                    coe['Beta'] = ind_type.beta
        coe['Cost_of_Equity_temp'] = coe['Risk_Free_Rate'] + (coe['Beta'] * coe['Market_Premium'])
        coe['Risk_Premium'] = float(coe_rows[0])/100
        coe['Cost_of_Equity'] = coe['Cost_of_Equity_temp'] + coe['Risk_Premium']
        coe['Cost_of_Debt'] = float(coe_rows[1])
        coe['Effective_tax_rate'] = 25.17/100
        coe['Cost_of_debt_after_tax'] = coe['Cost_of_Debt'] * (1 - coe['Effective_tax_rate'])
        coe['Target_Debt_as_total_capitalisation'] = float(coe_rows[2])
        coe['Target_Market_cap_as_of_Total_Capitalisation'] = 1 - coe['Cost_of_debt_after_tax']
        coe['WACC'] = coe['Cost_of_debt_after_tax'] * coe['Target_Debt_as_total_capitalisation'] + coe['Cost_of_Equity'] * coe['Target_Market_cap_as_of_Total_Capitalisation']
        coe['growth_rate'] = float(coe_rows[3])/100
        coe['no_of_equity_shares']=float(coe_rows[4])
       
        
        #######################################     Projected Financials     ###################################################
        Projected_Financials = {}
        Projected_Financials['Particulars_for_year']={}

        Projected_Financials["provisional_values"] = {}
        Projected_Financials["provisional_values"]["Operating_revenue"] = {}
        Projected_Financials["provisional_values"]["Operating_expenses"] = {}
        Projected_Financials['provisional_values']['Employee_benefit']={}
        Projected_Financials['provisional_values']['Other_expenses']={}
        Projected_Financials["provisional_values"]["Depreciation_&_Amortization"] = {}
        Projected_Financials['provisional_values']['Finance_cost']={}
        Projected_Financials['provisional_values']['Other_income']={}
        Projected_Financials['provisional_values']['Taxes']={}
        Projected_Financials['provisional_values']['Equity']={}
        Projected_Financials['provisional_values']['Debt']={}

        print(Projected_Financials)
        
        fields=["Operating_revenue","Operating_expenses","Employee_benefit","Other_expenses","Depreciation_&_Amortization","Finance_cost","Other_income","Equity","Debt","Other-liabilities","Working-Capital-Asset","Cash-bank-balance"]
        for i in range(len(fields)):
            
            Projected_Financials['provisional_values'][fields[i]]=float(provisional_inputs[i])
        print( Projected_Financials['provisional_values'])


        Projected_Financials['provisional_values']['EBITDA']=Projected_Financials["provisional_values"]["Operating_revenue"]-(Projected_Financials["provisional_values"]["Operating_expenses"]+Projected_Financials['provisional_values']['Employee_benefit']+Projected_Financials['provisional_values']['Other_expenses'])


        Projected_Financials['provisional_values']['EBIT']=Projected_Financials['provisional_values']['EBITDA']-Projected_Financials["provisional_values"]["Depreciation_&_Amortization"]


        Projected_Financials['provisional_values']['EBT']=Projected_Financials['provisional_values']['EBIT']-Projected_Financials['provisional_values']['Finance_cost']+Projected_Financials['provisional_values']['Other_income']
        if Projected_Financials['provisional_values']['EBT']<0:
            Projected_Financials['provisional_values']['Taxes']=0
        else:
            Projected_Financials['provisional_values']['Taxes']=Projected_Financials['provisional_values']['EBT']*coe['Effective_tax_rate'] 
        Projected_Financials['provisional_values']['EAT']=Projected_Financials['provisional_values']['EBT']-Projected_Financials['provisional_values']['Taxes']


        


      
        
    
        Projected_Financials["Particulars_for_year"]["Operating_revenue"] = {}
        Projected_Financials["Particulars_for_year"]["Operating_expenses"] = {}
        Projected_Financials['Particulars_for_year']['Employee_benefit']={}
        Projected_Financials['Particulars_for_year']['Other_expenses']={}
        Projected_Financials["Particulars_for_year"]["Depreciation_&_Amortization"] = {}
        Projected_Financials['Particulars_for_year']['Finance_cost']={}
        Projected_Financials['Particulars_for_year']['Other_income']={}


        

        


        for i in range(len(years)):
            Projected_Financials['Particulars_for_year']['Operating_revenue'][years[i]]=opr[i]
            Projected_Financials["Particulars_for_year"]["Operating_expenses"][years[i]]=cogs[i]
            Projected_Financials['Particulars_for_year']['Employee_benefit'][years[i]]=eb[i]
            Projected_Financials['Particulars_for_year']['Other_expenses'][years[i]]=oe[i]
            Projected_Financials["Particulars_for_year"]["Depreciation_&_Amortization"][years[i]]=d_a[i]
            Projected_Financials['Particulars_for_year']['Finance_cost'][years[i]]=fc[i]
            Projected_Financials['Particulars_for_year']['Other_income'][years[i]]=oi[i]
        Projected_Financials['Particulars_for_year']['EBITDA']={}

        Projected_Financials['Particulars_for_year']['EBIT']={}

        Projected_Financials['Particulars_for_year']['EBT']={}
        Projected_Financials['Particulars_for_year']['Taxes']={}
        Projected_Financials['Particulars_for_year']['EAT']={}

        taxes_sum=Projected_Financials['provisional_values']['EAT']


        for year in years:
            Projected_Financials['Particulars_for_year']['EBITDA'][year]= Projected_Financials["Particulars_for_year"]["Operating_revenue"][year]-(Projected_Financials["Particulars_for_year"]["Operating_expenses"][year]+Projected_Financials['Particulars_for_year']['Employee_benefit'][year]+Projected_Financials['Particulars_for_year']['Other_expenses'][year])

        
            Projected_Financials['Particulars_for_year']['EBIT'][year]=Projected_Financials['Particulars_for_year']['EBITDA'][year]- Projected_Financials["Particulars_for_year"]["Depreciation_&_Amortization"][year]
            
            Projected_Financials['Particulars_for_year']['EBT'][year]=Projected_Financials['Particulars_for_year']['EBIT'][year]-Projected_Financials['Particulars_for_year']['Finance_cost'][year]+ Projected_Financials['Particulars_for_year']['Other_income'][year]

        
            if Projected_Financials['Particulars_for_year']['EBT'][year]<0:
                Projected_Financials['Particulars_for_year']['Taxes'][year]=0
                taxes_sum+=Projected_Financials['Particulars_for_year']['EBT'][year]
            elif taxes_sum:
                
                taxes_sum+=Projected_Financials['Particulars_for_year']['EBT'][year]

                if taxes_sum>0:
                    Projected_Financials['Particulars_for_year']['Taxes'][year]=Projected_Financials['Particulars_for_year']['EBT'][year]*coe['Effective_tax_rate'] 
                    print(year)
                    taxes_sum=0
                else:
                    Projected_Financials['Particulars_for_year']['Taxes'][year]=0
            else:

                Projected_Financials['Particulars_for_year']['Taxes'][year]=Projected_Financials['Particulars_for_year']['EBT'][year]*coe['Effective_tax_rate']

            
            Projected_Financials['Particulars_for_year']['EAT'][year]=Projected_Financials['Particulars_for_year']['EBT'][year]-Projected_Financials['Particulars_for_year']['Taxes'][year]
                
       
        Projected_Financials['Sources_of_application_funds']={}
        Projected_Financials['Sources_of_application_funds']['Equity']={}
        Projected_Financials['Sources_of_application_funds']['Debt']={}
        Projected_Financials['Sources_of_application_funds']['Other_Liabilities']={}
        Projected_Financials['Sources_of_application_funds']['Equity_liabilities']={}

        

        for i in range(len(years)):
            Projected_Financials['Sources_of_application_funds']['Equity'][years[i]]=eq[i]
            Projected_Financials['Sources_of_application_funds']['Debt'][years[i]]=d[i]
            Projected_Financials['Sources_of_application_funds']['Other_Liabilities'][years[i]]=ol[i]
            Projected_Financials['Sources_of_application_funds']['Equity_liabilities'][years[i]]=Projected_Financials['Sources_of_application_funds']['Equity'][years[i]]+Projected_Financials['Sources_of_application_funds']['Debt'][years[i]]+  Projected_Financials['Sources_of_application_funds']['Other_Liabilities'][years[i]]
                
        Projected_Financials['Sources_of_application_funds']['Tangible_Assets']={}
        Projected_Financials['Sources_of_application_funds']['Investments']={}
        Projected_Financials['Sources_of_application_funds']['working_capital_asset']={}
        Projected_Financials['Sources_of_application_funds']['Cash_bank_balance']={}
        Projected_Financials['Sources_of_application_funds']['Funds_applied']={}

        

        for i in range(len(years)):
            Projected_Financials['Sources_of_application_funds']['Tangible_Assets'][years[i]]=ta[i]
            Projected_Financials['Sources_of_application_funds']['Investments'][years[i]]=inv[i]
            Projected_Financials['Sources_of_application_funds']['working_capital_asset'][years[i]]=wca[i]
            Projected_Financials['Sources_of_application_funds']['Cash_bank_balance'][years[i]]=Projected_Financials['Sources_of_application_funds']['Equity_liabilities'][years[i]]-Projected_Financials['Sources_of_application_funds']['Tangible_Assets'][years[i]]-Projected_Financials['Sources_of_application_funds']['Investments'][years[i]]-Projected_Financials['Sources_of_application_funds']['working_capital_asset'][years[i]]
            Projected_Financials['Sources_of_application_funds']['Funds_applied'][years[i]]=Projected_Financials['Sources_of_application_funds']['Cash_bank_balance'][years[i]]+Projected_Financials['Sources_of_application_funds']['working_capital_asset'][years[i]]+Projected_Financials['Sources_of_application_funds']['Tangible_Assets'][years[i]]+ Projected_Financials['Sources_of_application_funds']['Investments'][years[i]]
                                                                                

        Projected_Financials['Sources_of_application_funds']['Net_current_assets']={}
        Projected_Financials['Sources_of_application_funds']['Change_in_working_capital']={}
        for year in years:

            Projected_Financials['Sources_of_application_funds']['Net_current_assets'][year]=Projected_Financials['Sources_of_application_funds']['working_capital_asset'][year]-Projected_Financials['Sources_of_application_funds']['Other_Liabilities'][year]
        
        for i in range(len(years)):
            if i==0:
                Projected_Financials['Sources_of_application_funds']['Change_in_working_capital'][years[i]]= Projected_Financials['provisional_values']["Working-Capital-Asset"]- Projected_Financials['provisional_values']["Other-liabilities"]-Projected_Financials['Sources_of_application_funds']['Net_current_assets'][years[i]]
            else:
                Projected_Financials['Sources_of_application_funds']['Change_in_working_capital'][years[i]]=Projected_Financials['Sources_of_application_funds']['Net_current_assets'][years[i-1]]-Projected_Financials['Sources_of_application_funds']['Net_current_assets'][years[i]]

        #############################                 Valuation Summary         #######################################

        Valuation_summary={}
        # Valuation_summary["Growth_rate"]=coe_rows[7]/100
        Valuation_summary["Number_of_months"]={}
        for i in range(len(years)):
            if i==0:
                Valuation_summary["Number_of_months"][years[i]]=provisional_months_left-1+provisional_days_left
            else:
                Valuation_summary["Number_of_months"][years[i]]= Valuation_summary["Number_of_months"][years[i-1]]+12


        Valuation_summary["Free_cash_flows_to_equity"]={}
        Valuation_summary["Discount_Factor"]={}
        Valuation_summary["Present_value"]={}


        for i in range(len(years)):
            if i==0:
                Valuation_summary["Free_cash_flows_to_equity"][years[i]]=Projected_Financials['Particulars_for_year']['EAT'][years[i]]+ Projected_Financials["Particulars_for_year"]["Depreciation_&_Amortization"][years[i]]+Projected_Financials['Sources_of_application_funds']['Debt'][years[i]]-Projected_Financials["provisional_values"]["Debt"]-ce[i]/(10**5)+Projected_Financials['Sources_of_application_funds']['Change_in_working_capital'][years[i]]
            else:
                Valuation_summary["Free_cash_flows_to_equity"][years[i]]=Projected_Financials['Particulars_for_year']['EAT'][years[i]]+ Projected_Financials["Particulars_for_year"]["Depreciation_&_Amortization"][years[i]]+Projected_Financials["Sources_of_application_funds"]['Debt'][years[i]]-Projected_Financials['Sources_of_application_funds']['Debt'][years[i-1]]-Projected_Financials["Particulars_for_year"]["Operating_revenue"][years[i]]/(10**5)+Projected_Financials['Sources_of_application_funds']['Change_in_working_capital'][years[i]]
            Valuation_summary["Discount_Factor"][years[i]]=1/(1+coe['Cost_of_Equity'])**(Valuation_summary["Number_of_months"][years[i]]/12)
            Valuation_summary["Present_value"][years[i]]=Valuation_summary["Free_cash_flows_to_equity"][years[i]]*Valuation_summary["Discount_Factor"][years[i]]
        Valuation_summary["Terminal_cash_flow"]=Valuation_summary["Free_cash_flows_to_equity"][list(Valuation_summary["Free_cash_flows_to_equity"].keys())[-1]]
        # Valuation_summary["Post_tax_terminal_value"]=(Valuation_summary["Terminal_cash_flow"]*(1+Valuation_summary["Growth_rate"]))/(coe['WACC']-Valuation_summary["Growth_rate"])
        Valuation_summary["NPV_of_explicit_period"]=0
        for year in years:
            Valuation_summary["NPV_of_explicit_period"]+=Valuation_summary["Present_value"][year]
        final_valuation=[]

        count=0
        for growthrate in [0.02,coe_rows[3]/100,0.1]:
            count+=1
            Valuation_summary["Growth_rate"]=growthrate
            Valuation_summary["Post_tax_terminal_value"]=(Valuation_summary["Terminal_cash_flow"]*(1+Valuation_summary["Growth_rate"]))/(coe['WACC']-Valuation_summary["Growth_rate"])
            Valuation_summary["present_value_perpetuity"]=Valuation_summary["Post_tax_terminal_value"]*Valuation_summary["Discount_Factor"][list(Valuation_summary["Discount_Factor"].keys())[-1]]
            # Valuation_summary["cash_bank_balance"]=0.65
            Valuation_summary["cash_bank_balance"]=Projected_Financials['provisional_values']["Cash-bank-balance"]
            Valuation_summary["Implied_premoney_equity_value"]=Valuation_summary["NPV_of_explicit_period"]+Valuation_summary["present_value_perpetuity"]+Valuation_summary["cash_bank_balance"]+float(request.POST.get("Market_value_invetment")) + float(request.POST.get("Contigent_liability"))
            Valuation_summary["Number_of_equity_shares"]=coe['no_of_equity_shares']
            Valuation_summary["Value_per_equity"]=Valuation_summary["Implied_premoney_equity_value"]*(10**5)/Valuation_summary["Number_of_equity_shares"]
            final_valuation.append(Valuation_summary["Value_per_equity"])
            if count==2:
                premoney_equity_value=Valuation_summary["Implied_premoney_equity_value"]
            print("final anser",Valuation_summary["Value_per_equity"])
        response={
            "two_percent":final_valuation[0],
            "input_percent":final_valuation[1],
            "ten_percent":final_valuation[2],
            "equity_shares":coe['no_of_equity_shares'],
            "premoney_equity_value":premoney_equity_value
        }
      
        print("-------",request.POST.get("final_id"))
        # item=Client.objects.get(id=request.POST.get("final_id"))
        # item.valuation=final_valuation[1]
        # item.save()
        return JsonResponse(response)
        
    return redirect("/")