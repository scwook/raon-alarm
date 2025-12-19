from datetime import datetime

aaa = datetime.now().replace(hour=15, minute=0, second=0, microsecond=0)
print(aaa)

now = datetime.now()
midnight = now.replace(hour=0, minute=0, second=0, microsecond=0)
sec_now = int((now - midnight).total_seconds())
sec_mg = int((aaa - midnight).total_seconds())

print(sec_now)
print(sec_mg)