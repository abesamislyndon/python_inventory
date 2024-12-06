from django.shortcuts import render

# Create your views here.
def register_account(request):
    return render(request, 'accounts/register_account.html')
 

def reset_password(request):
    return render(request, 'accounts/reset_password.html')
