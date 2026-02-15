from accounts.models import CompanyUser

def user_context(request):

    company_id = request.session.get('company_id')
    user_role = None

    if request.user.is_authenticated and company_id:
        try:
            company_user = CompanyUser.objects.get(user=request.user,company_id=company_id,status='Approved')
            user_role = company_user.role
        except CompanyUser.DoesNotExist:
            user_role = None

    return {'user_role': user_role,'company_id': company_id}
