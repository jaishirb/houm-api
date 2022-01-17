from apps.houmers.models import Houmer, CompanyAgent
from apps.utils.forms import BaseUserCreationForm


class HoumerForm(BaseUserCreationForm):
    """
    usage of forms for improving the User experience in admin.
    """
    class Meta(BaseUserCreationForm.Meta):
        model = Houmer


class CompanyAgentForm(BaseUserCreationForm):
    class Meta(BaseUserCreationForm.Meta):
        model = CompanyAgent
