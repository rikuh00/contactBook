import pandas as pd
import os
os.chdir('..')
cwd = os.getcwd()
print(cwd)
#%% Functions
# General Function for Getting the Name of the Record
def getName(action):
    name = input('Please input the name of the contact you want to {}: '.format(action)).title()
    return name
# Enter New Contact
def newContact(book):
    checker = input('Is this a company or an individual? (C for company, I for individual)')
    validInput = ['C', 'c', 'I', 'i']
    while not(checker in validInput):
        print('Invalid input - Please try again.')
        checker = input('Is this a company or an individual? (C for company, I for individual)')
    checker = checker.capitalize()
    print('Please input the following information. Press the enter key to leave fields blank.')
    if checker == 'C':
        contact = {}
        companyName = input('Enter the name of the company: ').title()
        number =  input('Enter the phone number of the company: ')
        number = number.replace('-', '').replace('(', '').replace(')', '')
        if number != '':
            number = '({0}){1}-{2}'.format(number[:3], number[3:6], number[6:])
        email = input('Enter the email of the company: ')
        contact['firstName'] = [companyName]
        contact['lastName'] = companyName
        contact['number'] = number
        contact['email'] = email
        contact['type'] = 'Company'
    elif checker == 'I':
        contact = {}
        firstName = input('Enter the first name of the individual: ').title()
        lastName = input('Enter the last name of the individual: ').title()
        number =  input('Enter the phone number of the individual: ')
        number = number.replace('-', '').replace('(', '').replace(')', '')
        if number != '':
            number = '({0}){1}-{2}'.format(number[:3], number[3:6], number[6:])
        email = input('Enter the email of the individual: ')
        contact['firstName'] = [firstName]
        contact['lastName'] = lastName
        contact['number'] = number
        contact['email'] = email
        contact['type'] = 'Individual'
    contact = pd.DataFrame(contact)
    book = pd.concat([book, contact]).reset_index(drop = True)
    return book

# Searching for a Record (by name, assuming no duplicates)
def search(name, book):
    temp = book.reset_index(drop = False)
    temp = temp[(temp.firstName == name) | (temp.lastName == name)].reset_index(drop = True)
    try:
        index = (temp['index'][0])
    except Exception:
        print('Record not found.')
        index = -1
    return index

# View a Record
def searchRecord(name, book):
    indexNum = search(name, book)
    if indexNum < 0:
        return None
    print(book.iloc[indexNum])
    return None

# View Entire Contact Book
def viewBook(book):
    temp = book.sort_values(by = 'firstName').reset_index(drop = True)
    for num in range(len(temp)):
        print(temp.iloc[num])
    return None

# Edit a Record
def edit(name, book):
    indexNum = search(name, book)
    if indexNum < 0:
        return book
    searchRecord(name, book)
    checker = input('Proceed with editing? [Y/N]: ').capitalize()
    if checker == 'N':
        return book
    elif checker == 'Y':
        book = book.drop(book.index[indexNum])
        book = newContact(book)
        return book
    else:
        print('Invalid input.')
        return book

# Delete a Record
def delete(name, book):
    indexNum = search(name, book)
    if indexNum < 0:
        return book
    searchRecord(name, book)
    checker = input('Are you sure you want to delete this contact? [Y/N]: ').capitalize()
    if checker == 'N':
        return book
    elif checker == 'Y':
        book = book.drop(book.index[indexNum]).reset_index(drop = True)
        return book
    else:
        print('Invalid input.')
        return book

#%% Main
if __name__ == '__main__':
    try:
        book = pd.read_csv(cwd + r'Data/contactBook.csv')
    except pd.errors.EmptyDataError:
        book = pd.DataFrame()
    except FileNotFoundError:
        book = pd.DataFrame()
    print(book.head(10))

    actionList = ['N', 'V', 'E', 'D']
    action = 'N'
    while action in actionList:
        print('Choose from the following options:')
        print('[N]ew Contact, [S]earch for Contact, [V]iew Book, [E]dit Contact, [D]elete Contact')
        action = input('Plase indicate your choice now: ').capitalize()

        if action == 'N':
            book = newContact(book)
        elif action == 'S':
            name = getName('searchRecord')
            searchRecord(name, book)
        elif action == 'V':
            viewBook(book)
        elif action == 'E':
            name = getName('edit')
            book = edit(name, book)
        elif action == 'D':
            name = getName('delete')
            book = delete(name, book)
        else:
            book.to_csv(cwd + r'/Data/contactBook.csv', index = False)
            print('Exiting the application...')