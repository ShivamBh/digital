from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.http import Http404

class StaffRequiredmixin():
	@classmethod
	def as_view(self, *args, **kwargs):
		view = super(StaffRequiredmixin, self).as_view(*args, **kwargs)
		return login_required(view)

	@method_decorator(login_required)
	def dispatch(self, request, *args, **kwargs):
		if request.user.is_staff:
			return super(StaffRequiredmixin, self).dispatch(request, *args, **kwargs)
		else:
			raise Http404


class LoginRequiredMixin():
	@classmethod
	def as_view(self, *args, **kwargs):
		view = super(LoginRequiredmixin, self).as_view(*args, **kwargs)
		return staff_member_required(view)

	@method_decorator(login_required)
	def dispatch(self, request, *args, **kwargs):
		return super(LoginRequiredmixin, self).dispatch(request, *args, **kwargs)
	
