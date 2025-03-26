def print_menu():
    print("\nBank Project:")
    print("1. Foydalanuvchilarni boshqarish")
    print("2. Tranzaksiya boshqaruvi")
    print("3. Other Functions")
    print("4. ")
    print("5. ")
    print("6. Exit")


def print_menu_ManageUsers():
    print("\nFoydalanuvchilarni boshqarish:")
    print("1. Barcha foydalanuvchilarni ko‘rish")
    print("2. So‘nggi 1 oy ichida faol bo‘lgan foydalanuvchilarni ko‘rish")
    print("3. Har bir foydalanuvchining hisob holatini tekshirish")
    print("4. Foydalanuvchi kartalarining limitini nazorat qilish")
    print("5. Ortga qaytish")


def print_menu_ManageTransactions():
    print("\nTranzaksiya boshqaruvi:")
    print("1. Kartadan kartaga pul o‘tkazmalar")
    print("2. Kunlik, haftalik tranzaksiyalarni ko‘rish")
    print("3. Yirik tranzaksiyalarni avtomatik tekshirish (150 mln so‘mdan oshsa)")
    print("4. Pul yechish va depozit qilish")
    print("5. Ortga qaytish")


def print_menu_other_functions():
    print('1. Hisobot generatsiyasi (kunlik, haftalik, oylik)')
    print('2. Bloklangan va tekshirilayotgan kartalarni kuzatish')
    print('3. Har bir foydalanuvchining tranzaksiya tarixini ko‘rish')
    print('4. Balansni tahlil qilish (o‘rtacha balans, eng ko‘p tranzaksiya qilgan foydalanuvchi)')
