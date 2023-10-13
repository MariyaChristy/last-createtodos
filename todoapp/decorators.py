from django.shortcuts import redirect

def signin_required(fn):
    def inner(request,*args,**kwargs):
        if not request.user.is_authenticated:
            return redirect("signin")
        else:
            return fn(request,*args,**kwargs)
    return inner