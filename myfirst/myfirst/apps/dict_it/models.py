from django.db import models

class Quest(models.Model):
     id = models.AutoField(primary_key=True)
     quest_level = models.IntegerField('Уровень')
     quest_number = models.IntegerField('Номер')
     quest_text = models.TextField('Вопрос')
     quest_right_answ = models.CharField('Правильный ответ', max_length = 200)
    
     def __str__(self):
         return self.quest_text
         
     class Meta:
         verbose_name = 'Вопрос'
         verbose_name_plural = 'Вопросы'
        
class Answer(models.Model):
     quest_id = models.ForeignKey(Quest, on_delete = models.CASCADE)
     id = models.AutoField(primary_key=True)
     answer_variant = models.IntegerField('Вариант ответа') 
     answer_text = models.CharField('Номер ', max_length = 200)
     quest_id = models.IntegerField('ID') 
     
     def __str__(self):
         return self.answer_text
         
     class Meta:
         verbose_name = 'Ответ'
         verbose_name_plural = 'Ответы'
         
class Users(models.Model):
    id = models.AutoField(primary_key=True)
    userid = models.IntegerField('ID user') 
    last_q = models.IntegerField('Последний вопрос') 
    trys = models.IntegerField('Попытки') 
    r_answ = models.IntegerField('Правильные ответы') 