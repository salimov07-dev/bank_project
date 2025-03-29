import os
def print_menu():
    os.system("cls" if os.name == "nt" else "clear")  # Terminalni tozalash (Windows/Linux)
    
    print("\033[1;36m")  # **Cyan rang**
    print("–" * 40)
    print(" " * 10 + "💳 BANK PROJECT MENU")
    print("–" * 40)
    print("\033[0m")  # **Rangni tiklash**
    
    print("1️⃣  Foydalanuvchilarni boshqarish 👤")
    print("2️⃣  Tranzaksiya boshqaruvi 💰")
    print("3️⃣  Boshqa funksiyalar 🛠️")
    print("4️⃣  Hisobot va Monitoring 📊") 
    print("5️⃣  Chiqish 🚪")  
 
def print_menu_ManageTransactions():
    print("\n" + "=" * 60)
    print(" 📌 Foydalanuvchilarni boshqarish")
    print("=" * 60)
    print("1️⃣  📤 Kartadan kartaga pul o‘tkazmalar")
    print("2️⃣  📊 Kunlik, haftalik tranzaksiyalarni ko‘rish")
    print("3️⃣  💰 Pul yechish va depozit qilish")
    print("4️⃣  🔙 Ortga qaytish")

def print_menu_ManageTransactions():
    print("\n" + "=" * 60)
    print(" 📌 Tranzaksiya boshqaruvi")
    print("=" * 60)
    print("1️⃣  Kartadan kartaga pul o‘tkazmalar")
    print("2️⃣  📊 Kunlik, haftalik tranzaksiyalarni ko‘rish")
    print("3️⃣  💵 Pul yechish va depozit qilish")
    print("4️⃣  🔙 Ortga qaytish")

def print_menu_other_functions():
    print("\n" + "=" * 60)
    print(" 📌 Boshqa funksiyalar menyusi ")
    print("=" * 60)
    print("1️⃣  📊 Hisobot generatsiyasi (kunlik, haftalik, oylik)")
    print("2️⃣  📝 Ro‘yxatdan o‘tish")
    print("3️⃣  📜 Har bir foydalanuvchining tranzaksiya tarixini ko‘rish")
    print("4️⃣  📈 Balansni tahlil qilish") 
    print("5️⃣ 🔙 Ortga qaytish")
    print("=" * 60)

def forth_menu():
    print("\n" + "=" * 60)
    print(" 📌 Hisobot va Monitoring ")
    print("=" * 60)
    print('1️⃣ 🚫 Bloklangan foydalanuvchilar ro‘yxatini yuritish va ularni monitoring qilish ')
    print('2️⃣ 💳 Kartalarning o‘rtacha foydalanish davomiyligi (foydalanuvchilar kartani qancha muddat ishlatmoqda)')
    print('3️⃣ 👑 Vip users') 
    print('4️⃣ 📅 Rejalashtirilgan to\'lovlar')