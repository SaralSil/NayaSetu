from django.contrib import admin
from .models import Department, Scheme, SchemeEligibility, SchemeDocument, CommonRejectionReason

class SchemeDocumentInline(admin.TabularInline):
    model = SchemeDocument
    extra = 1

class SchemeEligibilityInline(admin.StackedInline):
    model = SchemeEligibility
    can_delete = False

class CommonRejectionReasonInline(admin.StackedInline):
    model = CommonRejectionReason
    extra = 1

@admin.register(Department)
class DepartmentAdmin(admin.ModelAdmin):
    list_display = ('name_en', 'code', 'helpline', 'portal_url')
    search_fields = ('name_en', 'name_bn', 'code')

@admin.register(Scheme)
class SchemeAdmin(admin.ModelAdmin):
    list_display = ('name_en', 'name_bn', 'category', 'department', 'benefit_type', 'is_active')
    list_filter = ('category', 'department', 'benefit_type', 'is_active')
    search_fields = ('name_en', 'name_bn', 'description_en')
    prepopulated_fields = {'slug': ('name_en',)}
    inlines = [SchemeEligibilityInline, SchemeDocumentInline, CommonRejectionReasonInline]

@admin.register(CommonRejectionReason)
class CommonRejectionReasonAdmin(admin.ModelAdmin):
    list_display = ('code_or_phrase', 'title_en', 'scheme', 'responsible_authority')
    search_fields = ('code_or_phrase', 'title_en', 'explanation_en')
