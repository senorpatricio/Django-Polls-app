from django.contrib import admin
from .models import Choice, Question

# class QuestionAdmin(admin.ModelAdmin):
# 	fields = ['pub_date', 'question_text']

# admin.site.register(Question, QuestionAdmin)
# admin.site.register(Choice)

class ChoiceInLine(admin.TabularInline):  # can also be StackedInline
	model = Choice
	extra = 3

class QuestionAdmin(admin.ModelAdmin):
	fieldsets = [
		(None,					{'fields': ['question_text']}),
		('Date Information',	{'fields': ['pub_date'], 'classes': ['collapse']}),
	]
	inlines = [ChoiceInLine]
	list_display = ('question_text', 'pub_date', 'was_published_recently')
	list_filter = ['pub_date']  # adds ability to filter by publishing date
	search_fields = ['question_text']  # adds a search box to search through questions

admin.site.register(Question, QuestionAdmin)
# This tells Django: Choice objects are edited on the Question admin page. 
# By default, provide enough fields for 3 choices.