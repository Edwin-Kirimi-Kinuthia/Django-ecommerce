from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from userauths.models import User, OTP, UnverifiedUser, Profile

class OTPInline(admin.TabularInline):
    model = OTP
    readonly_fields = ('otpid', 'otp', 'created_at')
    can_delete = False
    extra = 0

    def has_add_permission(self, request, obj=None):
        return False

    def has_change_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return False

class ProfileInline(admin.StackedInline):
    model = Profile
    can_delete = False
    verbose_name_plural = 'Profiles'
    readonly_fields = ['display_profile_image']

    def display_profile_image(self, instance):
        return instance.display_profile_image()
    display_profile_image.short_description = 'Profile Image'

class UserAdmin(BaseUserAdmin):
    inlines = [ProfileInline, OTPInline]
    list_display = ["username", "email", "list_otps"]
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Personal info', {'fields': ('username', 'first_name', 'last_name')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser',
                                    'groups', 'user_permissions')}),
        ('Important dates', {'fields': ('last_login', 'date_joined')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'username', 'password1', 'password2'),
        }),
    )
    search_fields = ('email', 'username')
    ordering = ('email',)
    filter_horizontal = ('groups', 'user_permissions',)

    def list_otps(self, obj):
        return ", ".join([otp.otpid for otp in obj.otp_set.all()])
    list_otps.short_description = 'OTPs'

class UnverifiedUserAdmin(admin.ModelAdmin):
    list_display = ['email', 'username', 'registration_date', 'is_valid']
    search_fields = ['email', 'username']
    readonly_fields = ['verification_token']
    
    def is_valid(self, obj):
        return obj.is_valid()
    is_valid.boolean = True
    is_valid.short_description = 'Is Valid'

admin.site.register(User, UserAdmin)
admin.site.register(UnverifiedUser, UnverifiedUserAdmin)

@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'display_profile_image', 'bio', 'birth_date']
    search_fields = ['user__username', 'user__email', 'bio']
    readonly_fields = ['display_profile_image']

    def display_profile_image(self, obj):
        return obj.display_profile_image()
    display_profile_image.short_description = 'Profile Image'
