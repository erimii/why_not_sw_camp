# -*- coding: utf-8 -*-
"""
Created on Tue Feb  4 15:54:42 2025

@author: Admin

연락처를 입력받아 txt파일로 저장하고
실행될 때 txt파일의 내용을 자동으로 로딩

선택 메뉴
1. 연락처 입력
2. 연락처 출력
3. 연락처 삭제(이름기준)
4. 종료: txt파일로 저장
"""

class Contact:
    def __init__(self, name, phone_number, e_mail, address):
        self.name = name
        self.phone_number = phone_number
        self.e_mail = e_mail
        self.address = address
    
    def print_info(self):
        print('---------------')
        print(f'name: {self.name}')
        print(f'phone numnber: {self.phone_number}')
        print(f'e_mail: {self.e_mail}')
        print(f'address: {self.address}')
        print('---------------')



# 1번 메뉴 선택 시 입력 받은 내용을 contact 객체에 추가
def set_contact():
    name = input('name: ')
    phone_number = input('phone_number: ')
    e_mail = input('e_mail: ')
    address = input('address: ')
    contact = Contact(name, phone_number, e_mail, address)
    return contact

# 2번 메뉴 선택 시 contact 객체가 갖고 있는 값을 출력
def print_contact(contact_list):
    for contact in contact_list:
        contact.print_info()
        
# 3번 메뉴 선택 시 이름을 통해 삭제
def delete_contact(contact_list, name):
    for i, contact in enumerate(contact_list):
        if contact.name == name:
            del contact_list[i]

# 종료 선택시, 파일로 저장
def store_contact(contact_list):
    f = open('db.txt', 'wt')
    for contact in contact_list:
        f.write(contact.name + '\n')
        f.write(contact.phone_number + '\n')
        f.write(contact.e_mail + '\n')
        f.write(contact.address + '\n')
    f.close()
    
# 프로그램 실행 시 db.txt 자동 로딩
def load_contact(contact_list):
    f = open('db.txt', 'rt')
    lines = f.readline()
    num = len(lines) / 4
    num = int(num)
    
    for i in range(num):
        name = lines[4*i].rstrip('\n')
        phone_number = lines[4*i+1].rstrip('\n')
        e_mail = lines[4*i+2].rstrip('\n')
        address = lines[4*i+3].rstrip('\n')
        contact = Contact(name, phone_number, e_mail, address)
        contact_list.append(contact)
        
    f.close()

def print_menu():
    print('1. input')
    print('2. print')
    print('3. delete')
    print('4. end')
    menu = input('choose the menu: ')
    return int(menu)
    
def run():
    contact_list = []
    load_contact(contact_list)
    while 1:
        menu = print_menu()
        if menu == 1:
            contact = set_contact()
            contact_list.append(contact)
        elif menu == 2:
            print_contact(contact_list)
        elif menu == 3:
            name = input('Enter the name to delete: ')
            delete_contact(contact_list, name)
        elif menu == 4:
            store_contact(contact_list)
        else:
            break

if __name__ == '__main__':  # 파일 자체 실행 여부 확인
    run()



























