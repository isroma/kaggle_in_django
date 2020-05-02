from django.contrib import admin
from dashboard.models import Ranking, Dashboard

# Register your models here.
admin.site.register(Dashboard)
admin.site.register(Ranking)

class RankingInline(admin.StackedInline):
    model = Ranking

class DashboardAdmin(admin.ModelAdmin):
    inlines = [
        RankingInline,
    ]
