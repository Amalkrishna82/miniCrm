from accounts.models import CompanyUser

def get_user_company(request):
    company_id = request.session.get('company_id')
    if company_id:
        return company_id
    return None

def get_user_role(request, company_id):
    if not company_id:
        return None
    company_user = CompanyUser.objects.filter(user=request.user,company_id=company_id,status='Approved').first()

    if company_user:
        return company_user.role
    return None
