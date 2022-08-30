from django.shortcuts import render, redirect
from django.views import View
from django.contrib import messages
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.http import HttpResponseRedirect
from django.utils.html import strip_tags

from backend.forms import Seat
from backend.models import Agency, Vehicle
from backend.forms import SeatForm


class SeatListView(View):
    template = "backend/lists/seats.html"

    def get(self, request, *args, **kwargs):
        seats = Seat.objects.all().order_by('-id')
        context = {'seats': seats}
        return render(request, self.template, context)


class CreateUpdateSeat(View):
    template = "backend/create_update_seat.html"

    def get(self, request, *args, **kwargs):
        seat_id = request.GET.get('seat_id')
        vehicle_id = request.GET.get('vehicle_id')

        seat = Seat.objects.filter(id=seat_id).first()
        vehicle = Vehicle.objects.filter(id=vehicle_id).first()

        vehicles = Vehicle.objects.all()
        context = {
            "seat": seat,
            "vehicle": vehicle,
            "vehicles": vehicles,
        }  # noqa
        return render(request, self.template, context)

    def post(self, request, *args, **kwargs):
        seat_id = request.POST.get('seat_id')
        vehicle_id = request.POST.get('vehicle_id')
        vehicle = Vehicle.objects.filter(id=vehicle_id).first()

        if seat_id:
            # seat exists - update seat
            seat = Seat.objects.filter(id=seat_id).first()
            form = SeatForm(request.POST, request.FILES, instance=seat)  # noqa
            if form.is_valid():
                new_seat = form.save(commit=False)
                new_seat.vehicle = vehicle
                new_seat.save()
                messages.success(request, 'Seat Detail Updated Successfully.')  # noqa
                return redirect('backend:seats')
            else:
                for field, error in form.errors.items():
                    message = f"{field.title()}: {strip_tags(error)}"
                    break
                messages.warning(request, message)
                return HttpResponseRedirect(request.META.get("HTTP_REFERER"))
        else:
            # it's a new seat - create seat
            form = SeatForm(request.POST, request.FILES)
            if form.is_valid():
                seat = form.save(commit=False)
                seat.vehicle = vehicle
                seat.save()
                messages.success(request, 'New Seat Created Successfully.')  # noqa
                return redirect('backend:seats')
            else:
                for field, error in form.errors.items():
                    message = f"{field.title()}: {strip_tags(error)}"
                    break
                messages.warning(request, message)
                return HttpResponseRedirect(request.META.get("HTTP_REFERER"))


class DeleteSeat(View):
    def get(self, request, *args, **kwargs):
        return redirect('backend:seats')

    def post(self, request, *args, **kwargs):
        seat_id = request.POST.get('seat_id')
        seat = Seat.objects.filter(id=seat_id).first()
        seat.delete()
        messages.success(request, 'Vehicle Seat Deleted Successfully.')
        return HttpResponseRedirect(request.META.get("HTTP_REFERER"))
