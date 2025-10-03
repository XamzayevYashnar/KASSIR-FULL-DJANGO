from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.utils import timezone
from .models import Barcode

def barcode_list(request):
    barcodes = Barcode.objects.all().order_by('-created_at')
    return render(request, 'home.html', {'barcodes': barcodes})

def kassa(request):
    if request.method == 'POST':
        barcode_value = request.POST.get('barcode')
        if barcode_value:
            # Barcode allaqachon mavjudligini tekshiramiz
            if Barcode.objects.filter(value=barcode_value).exists():
                messages.warning(request, f'Barcode "{barcode_value}" allaqachon mavjud!')
            else:
                Barcode.objects.create(value=barcode_value)
                messages.success(request, f'Barcode "{barcode_value}" muvaffaqiyatli qo\'shildi!')
        return redirect('kassa')
    
    # So'nggi 5 ta barcode'ni olish
    recent_barcodes = Barcode.objects.all().order_by('-created_at')[:5]
    return render(request, 'kass_home.html', {'recent_barcodes': recent_barcodes})

def delete_barcode(request, barcode_id):
    try:
        barcode = Barcode.objects.get(id=barcode_id)
        barcode.delete()
        messages.success(request, f'Barcode "{barcode.value}" muvaffaqiyatli o\'chirildi!')
    except Barcode.DoesNotExist:
        messages.error(request, 'Barcode topilmadi!')
    return redirect('barcode_list')

def toggle_barcode_status(request, barcode_id):
    try:
        barcode = Barcode.objects.get(id=barcode_id)
        barcode.status = not barcode.status
        if barcode.status:
            barcode.completed_at = timezone.now()
        else:
            barcode.completed_at = None
        barcode.save()
        
        status_text = "bajarilgan" if barcode.status else "bajarilmagan"
        messages.success(request, f'Barcode "{barcode.value}" {status_text} holatiga o\'zgartirildi!')
    except Barcode.DoesNotExist:
        messages.error(request, 'Barcode topilmadi!')
    return redirect('barcode_list')

def get_stats(request):
    total_barcodes = Barcode.objects.count()
    completed_barcodes = Barcode.objects.filter(status=True).count()
    pending_barcodes = total_barcodes - completed_barcodes
    
    # Bajarilish foizini hisoblash
    completion_percentage = 0
    if total_barcodes > 0:
        completion_percentage = (completed_barcodes / total_barcodes) * 100
    
    return render(request, 'stats.html', {
        'total_barcodes': total_barcodes,
        'completed_barcodes': completed_barcodes,
        'pending_barcodes': pending_barcodes,
        'completion_percentage': completion_percentage
    })