import csv
from django.core.management.base import BaseCommand, CommandError
from django.contrib.auth.models import User
from newsletters.models import Newsletter
from django.core.mail import send_mail
from optparse import make_option
try:
    from cStringIO import StringIO
except ImportError:
    from StringIO import StringIO
    
class Command(BaseCommand):
    option_list = BaseCommand.option_list + (
        make_option('-e', '--email', action="store_false", dest='email', default=True,
            help='Whether to email the users to datran or not'
        ),
    )
    help = "Reindex user profiles for datran"
    def handle(self, *args, **opts):
        output = StringIO()
        writer = csv.writer(output, quoting=2)
        try:
            users = User.objects.filter(id__in=map(int, args))
        except ValueError:
            if len(args) and args[0] == '*':
                users = User.objects.all()
            else:
                raise CommandError('Args must be a list of User ids')
        # For all users selected
        for user in users:
            # Get their profile (most stuff is stored there)
            row = [
                user.id, # External ID
                user.first_name, # FirstName
                user.last_name, # LastName
                user.email, # Email
            ]
            try:
                prof = user.get_profile()
                row.extend([
                    prof.address1, # Address1
                    prof.address2, # Address2
                    prof.city, # City
                    prof.state, # State
                    prof.zip_code, # PostalCode
                    prof.get_political_view_display(), # Political_View
                    prof.mobile_phone, # WorkPhone,
                    prof.mobile_provider, # Mobile_Provider
                    prof.about_me, # About_Me
                    prof.activities, # Activities
                    prof.interests, # Interests
                    str(prof.update_date).split(' ')[0], # Update_Date YYYY-MM-DD
                    prof.get_gender_display(), # Gender
                    str(prof.date_of_birth).split(' ')[0], # DateOfBirth YYYY-MM-DD
                    prof.get_job_title_display(), # Profession
                    prof.get_job_industry_display(), # Job_Industry
                    prof.get_responsibility_display(), # Job_Responsibility
                    prof.get_company_size_display(), # Company_Size
                    prof.get_income_display(), # HouseHoldIncome
                    str(user.date_joined).split(' ')[0], # SourceSignupDate YYYY-MM-DD
                ])
            except:
                row.extend([None]*19)
            # Add their newsletter subscription info
            for newsletter in Newsletter.objects.all():
                if newsletter in prof.newsletters.all():
                    row.append(1) # subscribed
                else:
                    row.append(None) # unsubscribed
            try:
                writer.writerow(row)
            except (UnicodeDecodeError,UnicodeEncodeError): # Yes we have ugly data
                pass#print row
        if opts.get('email',True): # Send the email to datran if required
            # Subject, Body, From, ToList, ...
            send_mail('twtuserprofiles', output.getvalue(), 'soap@washingtontimes.com',
                ['datran@washingtontimesmail.com'], fail_silently=False)
        else:
            print output.getvalue()

