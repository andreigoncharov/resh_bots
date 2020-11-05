'''import datetime

day = datetime.datetime.today().date().day
x = datetime.datetime.now().month
month = x.strftime("%B")
year = datetime.datetime.today().date().year

monthes = {'January': 'Январь', 'February': 'Февраль', 'March': 'Март', 'April': 'Апрель', 'May': 'Май', 'June': 'Июнь',
           'July': 'Июль', 'August': 'Август', 'September': 'Сентябрь', 'October': 'Октябрь', 'November': 'Ноябрь', 'December':'Декабрь'}

month = monthes.get(month)


print(day)
print(month)
print(year)'''
from datetime import datetime, timedelta

'''import re
def detect_numbers(text):
    phone_regex = re.compile(r"(\+380)?\s*?(\d{3})\s*?(\d{3})\s*?(\d{3})")
    groups = phone_regex.findall(text)
    for g in groups:
        print("".join(g))

#detect_numbers("so I need to match +0991302490, +12673042397")
a=''
try:
    a = re.search("(?P<url>t.me?/[^\s]+)", 'andrew').group("url")
except:
    print(len(a))'''

'''date = '24.12.2020'
dot = date.find('.')
if date[int(dot)+1] == '1':
    date = date
else:
    p = date[:-6]
    print(p)
    date_2 = '0' + date[dot+1:]
    print(date_2)
    date = p + date_2
    print(date)
print(date)
import string

tab = str.maketrans(string.punctuation, ' ' * len(string.punctuation))

text = ',Предмет,Предмет,Предмет,Предмет'

res = text.translate(tab).split()

print(res)'''


def bubble_sort(nums):
    # Устанавливаем swapped в True, чтобы цикл запустился хотя бы один раз
    swapped = True
    while swapped:
        swapped = False
        for i in range(len(nums) - 1):
            if nums[i] > nums[i + 1]:
                # Меняем элементы
                nums[i], nums[i + 1] = nums[i + 1], nums[i]
                # Устанавливаем swapped в True для следующей итерации
                swapped = True
        print(nums)

# Проверяем, что оно работает
#random_list_of_nums = [2,8,9,4,1]
#bubble_sort(random_list_of_nums)
#print(random_list_of_nums)

curr_time = datetime.now() - datetime.timedelta(minutes=10)
print(curr_time)