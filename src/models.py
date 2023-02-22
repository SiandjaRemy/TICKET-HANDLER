from django.db import models
from django.contrib.auth.models import User

from io import BytesIO
import qrcode
from django.core.files import File
from PIL import Image, ImageDraw


# Create your models here.

class Profile(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    id_user = models.IntegerField()
    contact = models.IntegerField()
    location = models.CharField(max_length=255, blank=True)
    user_code = models.CharField(max_length=20, blank=True)
    id_card_number = models.IntegerField()
    profile_approuved = models.BooleanField(default=False)

    def __str__(self):
        return self.user.username

class Company(models.Model):
    company = models.ForeignKey(User, on_delete=models.CASCADE)
    contact = models.IntegerField()



class Category(models.Model):
    title = models.CharField(max_length=50, verbose_name="Category Title")
    slug = models.SlugField(max_length=55, verbose_name="Category Slug")
    is_going_on = models.BooleanField(verbose_name="Is Active?")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Created Date")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Updated Date")

    class Meta:
        verbose_name_plural = 'Categories'
        ordering = ('-created_at', )

    def __str__(self):
        return self.title

class Stadium(models.Model):
    name = models.CharField(max_length=45, verbose_name="Stadium name")
    slug = models.SlugField(max_length=55, verbose_name="Stadium Slug")
    location = models.CharField(max_length=255)
    
    def __str__(self):
        return self.name

class Event(models.Model):
    title = models.CharField(max_length=150, verbose_name="Event Title")
    slug = models.SlugField(max_length=160, verbose_name="Event Slug")
    description = models.TextField(blank=True, null=True, verbose_name="Detail Description")
    event_image = models.ImageField(upload_to='events', default="no_image.png", blank=True, null=True, verbose_name="Product Image")
    ticket_price = models.DecimalField(max_digits=8, decimal_places=2)
    available_tickets = models.IntegerField(default=1)
    category = models.ForeignKey(Category, verbose_name="Event Categoy", on_delete=models.CASCADE)
    staduim = models.ForeignKey(Stadium, verbose_name="Event Stadium", on_delete=models.CASCADE)
    is_active = models.BooleanField(verbose_name="Is Active?", default=True)
    event_date_time = models.DateTimeField(auto_now=False, null=True)
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Created Date")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Updated Date")

    class Meta:
        verbose_name_plural = 'Events'
        ordering = ('-created_at', )

    def __str__(self):
        return self.title

class Cart(models.Model):
    user = models.ForeignKey(User, verbose_name="User", on_delete=models.CASCADE)
    event = models.ForeignKey(Event, verbose_name="event", on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1, verbose_name="Quantity")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Created Date")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Updated Date")

    def __str__(self):
        return str(self.user)
    
    # Creating Model Property to calculate Quantity x Price
    @property
    def total_price(self):
        return self.quantity * self.event.ticket_price
    
# Add a boolean field here to be checked if the ordered date passed without the ticket been checked manually
class Order(models.Model):
    user = models.ForeignKey(User, verbose_name="User", on_delete=models.CASCADE)
    event = models.ForeignKey(Event, verbose_name="Event", on_delete=models.CASCADE)
    ordered_event_date_time = models.DateTimeField(auto_now_add=False)
    quantity = models.PositiveIntegerField(verbose_name="Quantity")
    ordered_date = models.DateTimeField(auto_now_add=True, verbose_name="Ordered Date")
    user_code = models.CharField(max_length=20)
    ticket_checked = models.BooleanField(default=False)
    #to be checked if the date of the event passes without the ticket been checked
    date_passed = models.BooleanField(default=False)


# Changed the user code to a foreign key 
class Guest(models.Model):
    user = models.ForeignKey(User, verbose_name="User", on_delete=models.CASCADE)
    user_code = models.CharField(max_length=20)
    name = models.CharField(max_length=25, verbose_name="Guest name")
    age = models.IntegerField(verbose_name="Guest age")
    id_card_number = models.IntegerField()

class GuestOrder(models.Model):
    user = models.ForeignKey(User, verbose_name="User", on_delete=models.CASCADE)
    guest_name = models.CharField(max_length=30)
    id_card_number = models.IntegerField()
    event = models.ForeignKey(Event, verbose_name="Event", on_delete=models.CASCADE)
    guest_order_event_date_time = models.DateTimeField(auto_now_add=False)
    quantity = models.PositiveIntegerField(verbose_name="Quantity")
    ordered_date = models.DateTimeField(auto_now_add=True, verbose_name="Ordered Date")
    user_code = models.CharField(max_length=20)
    ticket_checked = models.BooleanField(default=False)
    #to be checked if the date of the event passes without the ticket been checked
    date_passed = models.BooleanField(default=False)

#Models for the admins

class QrInfo(models.Model):
    code = models.CharField(max_length=25)
    qr_image = models.ImageField(upload_to='qr_images', default="no_image.png", blank=True)
    attributed = models.BooleanField(default=False)
    created_on = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.code
    
    def save(self, *args, **kwargs):
        qrcode_img = qrcode.make(self.code)
        canvas = Image.new("RGB", (330, 330), "white")
        draw = ImageDraw.Draw(canvas)
        canvas.paste(qrcode_img)
        fname = f"qr_code-{self.code}.png"
        buffer = BytesIO()
        canvas.save(buffer, "PNG")
        self.qr_image.save(fname, File(buffer), save=False)
        canvas.close()
        super().save(*args, **kwargs)

