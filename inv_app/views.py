from django.shortcuts import render,redirect
from django.contrib import messages
from redmail import gmail
from smtplib import SMTPAuthenticationError, SMTPRecipientsRefused, SMTPSenderRefused, SMTPException
import random
import threading
from.models import register_data,new_query,response_queries
from datetime import datetime
from random import randint as ran
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.core.exceptions import ObjectDoesNotExist

# Global variable for OTP
otp = None
demo = []

def generate_otp():
    global otp
    otp = random.randint(100000, 999999)
    
    # Start a timer to clear the OTP after 5 minutes (300 seconds)
    threading.Timer(300, clear_otp).start()

def send_mail(mail):
    gmail.username = "shukk.56@gmail.com"  # Replace with your actual Gmail username
    gmail.password = "gsar enfw yvvp mvty"  # Replace with your Gmail app password

    try:
        gmail.send(
            subject="OTP VERIFICATION",
            receivers=[mail],
            text="Copy the OTP to the clipboard.",
            html=f"<h1>Your OTP is:</h1><p>{otp}</p>"
        )
    except SMTPRecipientsRefused:
        raise ValueError("The recipient email address is invalid.")
    except SMTPSenderRefused:
        raise ValueError("The sender's email credentials are incorrect.")
    except SMTPAuthenticationError:
        raise ValueError("Authentication failed. Check your Gmail credentials.")
    except SMTPException as e:
        raise ValueError(f"Failed to send email: {str(e)}")

def clear_otp():
    global otp
    otp = None
    print("OTP has been cleared.")

# Views
def start(request):
    return render(request, 'register.html')

def reg(request):
    return render(request, 'register.html')

def go_small(request):
    name="small admin"
    context={
        'username':name
        }
    return render(request,"small_admin.html",context)

def temp_otp(request):
    if request.method == "POST":
        global mail, otp, name, passwrd
        name = request.POST.get("username")
        mail = request.POST.get("email")
        passwrd = request.POST.get("password")
        cofrm_pass = request.POST.get("confirm_password")
        if not register_data.objects.filter(reg_mail=mail).exists():

            if len(name) >= 5:
                if passwrd == cofrm_pass:
                    if len(passwrd)>=6:
                        generate_otp()  # Generate OTP
                        print(otp)  # For debugging purposes
                        try:
                            send_mail(mail)
                        except ValueError as e:
                            messages.error(request, str(e))  # Display specific error messages on the registration page
                            return render(request, 'register.html')  # Re-render the registration page with the error message
                        return render(request, "otp.html")  # If email sending is successful, render the OTP page
                    else:
                        messages.error(request, "the minimum password lenght is 6.")
                else:
                    messages.error(request, "Passwords do not match. Please try again.")
            else:
                messages.error(request, "The minimum length of the name should be 5 characters.")
        else:
            messages.error(request, "The Mail already registered..try another mail.")
            
    return render(request, 'register.html')

def log(request):
    return render(request, 'login.html')

def otp_chk(request):
    if request.method == "POST":
        otp_val = request.POST.get("otp_num")
        if otp_val == str(otp):
            type_data="client"
            user=register_data(reg_user=name,reg_mail=mail,reg_type=type_data,reg_pass=passwrd)
            user.save()

            return render(request, 'login.html')
        else:
            messages.error(request, "OTP is incorrect. Please try again.")
            
    return render(request, 'otp.html')

def resend(request):
    global mail  # Use the stored email address for resending

    if len(demo) >= 2: 
        messages.error(request, "Cannot resend the OTP. Too many attempts. Please register again.")
        return render(request, 'otp.html')

    demo.append("1")  # Track an attempt to resend the OTP
    generate_otp()  # Generate a new OTP
    print(otp)  # For debugging purposes
    try:
        send_mail(mail)  # Resend the email to the stored email address
    except ValueError as e:
        messages.error(request, str(e))  # Handle email errors on resending

    return render(request, 'otp.html')


def log_in(request):
    if request.method=="POST":
        global user_id
        log_email=request.POST.get('login_email')
        log_password=request.POST.get('login_password')
        print(log_email)
        print(log_password)
        # check if the user is already registerd or not
        if register_data.objects.filter(reg_mail=log_email,reg_pass=log_password).exists():
            print(log_email)
            print(log_password)
            temp_id=register_data.objects.filter(reg_mail=log_email,reg_pass=log_password)
            for i in temp_id:
                name=i.reg_user
            print(name)
            for i in temp_id:
                user_id=i.id
                type_log=i.reg_type
            print(type_log)
            query1=new_query.objects.filter(id_user_id=user_id)
            print(query1)
            if type_log=="client":
                context={'username':name,'query_dat':query1}
                return render(request,"client.html",context)
            elif type_log=="smalladmin":
                name="small admin"
                context={
                    'username':name
                }
                return render(request,"small_admin.html",context)
            else:
                name="big admin"
                context={
                    'username':name
                }
                return render(request,"big_admin.html",context)

                
        else:
            messages.error(request, "Login details is incorrect please try again..")
        return render(request,"login.html")
    return render(request,"login.html")

##function used to save the query details
@csrf_exempt
def save_data(request):
    current_date = datetime.now()
    formatted_date = current_date.strftime("%Y-%m-%d")
    print(formatted_date)
    if request.method=="POST":

        q_title=request.POST.get('title')
        q_query=request.POST.get('qdata')
        if len(q_query)>=20:
        


            print(q_title)
            print(q_query)

            current_status="new"
            # saving the query
            use=new_query(query_title=q_title,query_data=q_query,query_date=formatted_date,query_status=current_status,id_user_id=user_id)
            use.save()

            #return the updated data to dashboard
            query_datas = list(new_query.objects.filter(id_user_id=user_id).values())

            

            return JsonResponse({"status":"Saved","query_datass":query_datas})
        else:
            return JsonResponse({"status":"nothing"})
    else:
        return JsonResponse({"status":"error"})
    



    # model to view the entered query
@csrf_exempt
def modal(request):
    if request.method == "POST":
        query_id = request.POST.get('query_id')
        # Fetch query data based on the query_id
        try:
            query_instance = new_query.objects.get(id=query_id)
            query_data = query_instance.query_data
            print(query_data)
            return JsonResponse({"status": "Success", "query_datass": query_data})
        except new_query.DoesNotExist:
            return JsonResponse({"status": "Error", "message": "Query not found"})
    else:
        return JsonResponse({"status": "Error", "message": "Invalid request method"})



#function used to return the responsed data from the table
@csrf_exempt
def responses(request): 
    if request.method == "POST":
        query_userid = request.POST.get('query_userdata')
        print(query_userid)
        #try:
        data_change = register_data.objects.filter(id=query_userid)
        for i in data_change:
            temp_retrive=i.reg_type
        
        print(temp_retrive)
        #retrive the data for students 
        if temp_retrive=="client":
            print("poduu")
            query_datas = list(response_queries.objects.filter(res_id_id=user_id).values())
            print(query_datas)
        #retrive the data for admin
        else:
            query_datas = list(response_queries.objects.all().values())
            print("ithan",query_datas) 
            if query_datas: 
                return JsonResponse({"status": "Success", "responsed_datas": query_datas})    
            else:
                return JsonResponse({"status": "Empty", "responsed_datas": []})           
         
    else:
        return JsonResponse({"status": "Error", "message": "Invalid request method"})

#function used to display the modal  
@csrf_exempt
def modal2(request):
    if request.method == "POST":
        print("hhh")
        query_id_ = request.POST.get('query_ids')
        # Fetch query data based on the query_id
        try:
            query_instance = response_queries.objects.get(id=query_id_)
            query_data = query_instance.response_data

            print(query_data)
            return JsonResponse({"status": "Success", "query_datass": query_data})
        except response_queries.DoesNotExist:
            return JsonResponse({"status": "Error", "message": "Query not found"})
    else:
        return JsonResponse({"status": "Error", "message": "Invalid request method"})
    


#function used to display the report data
@csrf_exempt
def report_data(request):
    if request.method == "POST":
        print("helllll")
        # Fetch query data based on the query_id
        try:
            temp_id=register_data.objects.filter(id=user_id)
            print(temp_id)
            for i in temp_id:
                temp_2=i.reg_type
            print(temp_2)
            if temp_2=="client":
                res_query = list(response_queries.objects.filter(res_id_id=user_id).values())
                send_query = list(new_query.objects.filter(id_user_id=user_id).values())
            else:
                
                res_query  = list(response_queries.objects.all().values())
                send_query = list(new_query.objects.all().values())
            print(res_query)
            print(send_query)
         
            print(send_query)

        
            return JsonResponse({"status": "Success", "responsed_queries":res_query,"sended_queries":send_query})
        except response_queries.DoesNotExist:
            return JsonResponse({"status": "Error", "message": "Query not found"})
    else:
        return JsonResponse({"status": "Error", "message": "Invalid request method"})

#function used to display the query question in modal
@csrf_exempt
def get_question(request):
    if request.method == "POST":
        query_id = request.POST.get('res_id_')
        print(query_id)
        # Fetch query data based on the query_id
    
        query_instance = new_query.objects.get(id=query_id)
        query_data=query_instance.query_data

        print(query_data)

        return JsonResponse({"status": "Success", "question_ques": query_data})
        
    else:
        return JsonResponse({"status": "Error", "message": "Invalid request method"})
    


    ##function for fetch the response
@csrf_exempt
def fetch_res(request):
    if request.method=="POST":
        print("koko")
        type_check=request.POST.get('admin_type')
        data_list = list(new_query.objects.all().values())
        return JsonResponse({"status":"Saved","response_query":data_list})
    else:
        return JsonResponse({"status":"error"})
    

#function used to update the current status
@csrf_exempt
def update(request):
    if request.method=="POST":
        q_id=request.POST.get('q_id')
        q_status=request.POST.get('get_status')
        retrive_data=request.POST.get('quer_org')
        print(q_id)
        print(retrive_data)
        data_change = new_query.objects.get(id=q_id)
        data_change.query_status = q_status
        data_change.save()

        try:
            query_datas = list(response_queries.objects.all().values())

            print(query_datas)
            return JsonResponse({"status": "Success", "query_datass": query_datas})
        except new_query.DoesNotExist:
            return JsonResponse({"status": "Error", "message": "Query not found"})
    else:
        return JsonResponse({"status": "Error", "message": "Invalid request method"}) 
@csrf_exempt
def save_res(request):
    if request.method=="POST":
        qid=request.POST.get("res_id")
        r_data=request.POST.get("res_data")
        if len(r_data)>=20:
            print("error")

            res_date = datetime.now()
            responded_date = res_date.strftime("%Y-%m-%d")
            quer_data=new_query.objects.get(id=qid)
            
            
            print("hello")
            temp_id=register_data.objects.filter(id=qid)
            print(temp_id)
            test_id=quer_data.id_user_id

            response_title=quer_data.query_title
        
            query_send_date=quer_data.query_date
        
            response_status="closed"

            use=response_queries(res_title=response_title, query_date=query_send_date, response_data=r_data, resonded_date=responded_date,status=response_status,res_id_id=test_id)
            use.save()

            temp=new_query.objects.get(id=qid)
            temp.delete()

            return JsonResponse({"status":"Saved"})
    
        else:
            return JsonResponse({"status":"nothing"})

    else:
        return JsonResponse({"status":"error"})
    

#function used to return the responsed data from the table
@csrf_exempt
def response_admin(request): 
    if request.method == "POST":
        query_datas = list(response_queries.objects.all().values())
        print("ithan",query_datas) 
        if query_datas: 
            return JsonResponse({"status": "Success", "responsed_datas": query_datas})    
        else:
            return JsonResponse({"status": "Empty", "responsed_datas": []})           
         
    else:
        return JsonResponse({"status": "Error", "message": "Invalid request method"})
    





from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from .models import TaskList

def task_board(request):
    categories = ['upcoming', 'ongoing', 'hold', 'closed']
    
    # Pass both categories and task lists to the template
    task_lists = {category: TaskList.objects.filter(category=category) for category in categories}
    
    context = {
        'categories': [(category, category.capitalize()) for category in categories],  # Pass the categories and their display names
        'task_lists': task_lists  # Pass the task lists for each category
    }
    
    return render(request, 'drag.html', context)


def add_task(request, category):
    if request.method == 'POST':
        current_date = datetime.now()
        formatted_date = current_date.strftime("%Y-%m-%d")
        title = request.POST.get('title')
        TaskList.objects.create(title=title,category=category,task_date=formatted_date)
    return redirect('task_board')

def update_task(request, task_id):
    task = get_object_or_404(TaskList, id=task_id)
    if request.method == 'POST':
        task.title = request.POST.get('title')
        task.save()
    return redirect('task_board')

def delete_task(request, task_id):
    task = get_object_or_404(TaskList, id=task_id)
    task.delete()
    return redirect('task_board')

def update_category(request, task_id):
    if request.method == 'POST':
        task = get_object_or_404(TaskList, id=task_id)
        new_category = request.POST.get('category')
        if new_category in dict(TaskList.CATEGORY_CHOICES):
            task.category = new_category
            task.save()
            return JsonResponse({'success': True})
    return JsonResponse({'success': False})

#dashboard views
"""
# views.py
from django.shortcuts import render
from django.http import JsonResponse
from django.views.generic import TemplateView
from django.db.models import Count
from django.utils import timezone
from datetime import timedelta
from .models import TaskList, Report



def get_task_data(request):
    from_date = request.GET.get('from_date')
    to_date = request.GET.get('to_date')

    tasks = TaskList.objects.all()
    if from_date and to_date:
        tasks = tasks.filter(task_date__range=[from_date, to_date])

    data = tasks.values('category').annotate(count=Count('id'))
    return JsonResponse(list(data), safe=False)

def get_task_details(request):
    category = request.GET.get('category')
    from_date = request.GET.get('from_date')
    to_date = request.GET.get('to_date')

    tasks = TaskList.objects.filter(category=category)
    if from_date and to_date:
        tasks = tasks.filter(task_date__range=[from_date, to_date])

    data = list(tasks.values('title', 'task_date'))
    return JsonResponse(data, safe=False)

def delete_closed_tasks(request):
    two_days_ago = timezone.now() - timedelta(days=2)
    closed_tasks = TaskList.objects.filter(category='closed', task_date__lte=two_days_ago)
    
    for task in closed_tasks:
        Report.objects.create(
            title=task.title,
            category=task.category,
            task_date=task.task_date
        )
        task.delete()

    return JsonResponse({'message': 'Closed tasks older than 48 hours have been moved to reports.'})


# views.py
import os
from django.conf import settings
from django.http import HttpResponse
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter

def generate_report(request):
    # Create a unique filename for the report
    filename = f"report_{timezone.now().strftime('%Y%m%d%H%M%S')}.pdf"
    filepath = os.path.join(settings.MEDIA_ROOT, 'reports', filename)

    # Ensure the reports directory exists
    os.makedirs(os.path.dirname(filepath), exist_ok=True)

    # Create the PDF
    c = canvas.Canvas(filepath, pagesize=letter)
    width, height = letter

    c.drawString(100, height - 100, "Task Report")
    
    # Add report content here
    y = height - 120
    for category in ['upcoming', 'ongoing', 'hold', 'closed']:
        tasks = TaskList.objects.filter(category=category)
        c.drawString(100, y, f"{category.capitalize()} Tasks:")
        y -= 20
        for task in tasks:
            c.drawString(120, y, f"- {task.title} ({task.task_date})")
            y -= 15
        y -= 20

    c.save()

    with open(filepath, 'rb') as f:
        response = HttpResponse(f.read(), content_type='application/pdf')
        response['Content-Disposition'] = f'attachment; filename={filename}'
        return response
"""
from django.shortcuts import render
from django.http import JsonResponse, HttpResponse
from django.views.generic import TemplateView
from django.db.models import Count
from django.utils import timezone
from datetime import timedelta
from .models import TaskList, Report
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from io import BytesIO

class AdminDashboardView(TemplateView):
    template_name = 'big_admin.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = TaskList.CATEGORY_CHOICES
        return context

def get_task_data(request):
    from_date = request.GET.get('from_date')
    to_date = request.GET.get('to_date')

    tasks = TaskList.objects.all()
    if from_date and to_date:
        tasks = tasks.filter(task_date__range=[from_date, to_date])

    data = tasks.values('category').annotate(count=Count('id'))
    return JsonResponse(list(data), safe=False)

def get_task_details(request):
    category = request.GET.get('category')
    from_date = request.GET.get('from_date')
    to_date = request.GET.get('to_date')

    tasks = TaskList.objects.filter(category=category)
    if from_date and to_date:
        tasks = tasks.filter(task_date__range=[from_date, to_date])

    data = list(tasks.values('title', 'task_date'))
    return JsonResponse(data, safe=False)

def delete_closed_tasks(request):
    two_days_ago = timezone.now() - timedelta(days=2)
    closed_tasks = TaskList.objects.filter(category='closed', task_date__lte=two_days_ago)

    for task in closed_tasks:
        Report.objects.create(
            title=task.title,
            category=task.category,
            task_date=task.task_date
        )
        task.delete()

    return JsonResponse({'message': 'Closed tasks older than 48 hours have been moved to reports.'})
from django.http import HttpResponse
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from io import BytesIO
from django.utils import timezone

def generate_report(request):
    # Create a BytesIO buffer
    buffer = BytesIO()

    # Create the PDF object, using the BytesIO object as its "file."
    p = canvas.Canvas(buffer, pagesize=letter)
    width, height = letter

    # Draw things on the PDF. Here's where the PDF generation happens.
    p.drawString(100, height - 100, "Task Report")
    p.drawString(100, height - 115, f"Generated on: {timezone.now().strftime('%Y-%m-%d %H:%M:%S')}")

    y = height - 150
    for category, _ in TaskList.CATEGORY_CHOICES:
        tasks = TaskList.objects.filter(category=category)
        p.drawString(100, y, f"{category.capitalize()} Tasks:")
        y -= 20
        for task in tasks:
            p.drawString(120, y, f"- {task.title} ({task.task_date})")
            y -= 15
        y -= 20

        # Break to a new page if we're running out of space
        if y < 100:
            p.showPage()
            y = height - 100

    # Close the PDF object cleanly, and we're done.
    p.showPage()
    p.save()

    # FileResponse sets the Content-Disposition header so that browsers
    # present the option to save the file.
    buffer.seek(0)
    response = HttpResponse(buffer.getvalue(), content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="task_report.pdf"'

    return response