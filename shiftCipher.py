# -*- coding: utf-8 -*-
"""
Created on Sat Mar  5 13:24:08 2022

@author: ilayda
"""

#260201037-İlayda Özel 250201012-Göktay İncekara

import datetime
import sys
alphabet = 'abcdefghijklmnopqrstuvwxyz'  #This is the english alphabet that we use to send our messages.

def arrangeMessage(message):    
    message = message.lower()   #Turning all the message into lowercase characters
    removed =""                 
    for i in range(0,len(message)): 
        if(message[i].islower()):      #If the character is a lowercase character, that means it is not a special character. It is just a character in the alphabets.
            removed+= message[i]       #Put that character into the converted message
            if(message[i] not in alphabet):    #The character can be alphabetic character but it should also be in the alphabet. For example ş is a character but not in the alphabet.
                raise Exception("There is some character which is nonexistent in the alphabet.")   #If it is not defined in the alphabet throw an exception.
    return removed    #Our converted message which contains of the characters of the alphabet.

def checkKey(key):
    for i in range(0,len(key)):
        if(key[i] not in alphabet):    #Key characters should also be in the alphabet.
            return False               #If they are not checkKey is false
    return True                        #If all of the characters in the alphabet checkKey is true

def encrypt(plainText,key):
    
    encrypted = ''   #Encrypted message that will be returned by the function.
    key_index = 0    #To reach each letter in the key we have to traverse the key by that index.
    
    for i in plainText:            #We are taking each letter in plaintext
        startingPoint = ord('a')   #We are assuming all the characters are lowercase letters.
            
        letterNum = ord(i) - startingPoint     #Imagine that our letter is b, ord("b") will yield 98. And the "a" character yields to 97. So with this calculation,98-97=b, b=1 can be found.
        keyNum = ord(key[key_index]) - startingPoint  #This time we are taking the corresponding key letter and calculate its numerical value same as above calculation.
        number = (letterNum +keyNum) % len(alphabet)  #We are encrypting the letter
        encrypted += chr(number + startingPoint)      #Converting that number to it's letter number by adding the starting point again. With chr function, taking the letter value (which is encrypted letter) of that number and adding the encrypted letter into the ciphertext.
        key_index = (key_index +1) % len(key)         #We will reach the next key letter in the key so we are incrementing our key index but when the lenght finishes, we have to start again. So, we are taking it's mode also.
        
    return encrypted    #Our encrypted message will be returned after len(plaintext) iterations.

def decrypt(cipherText, key):
    
    plain = ''            #Decrypted message that will be returned by the function.
    key_index=0           #To reach each letter in the key we have to traverse the key by that index.
    
    for c in cipherText:           #We are taking each letter in ciphertext
        startingPoint = ord('a')   #We are assuming all the characters are lowercase letters.
            
        cip_num = ord(c)-startingPoint     #Imagine that our letter is b, ord("b") will yield 98. And the "a" character yields to 97. So with this calculation,98-97=b, b=1 can be found.
        key_num = ord(key[key_index])- startingPoint     #This time we are taking the corresponding key letter and calculate its numerical value same as above calculation.
        dec_num = (cip_num - key_num)%26     #We are decrypting the letter
        plain += chr(dec_num+startingPoint)  #Converting that number to it's letter number by adding the starting point again. With chr function, taking the letter value (which is decrypted letter) of that number and adding the decrypted letter into the plaintext.
        key_index = (key_index +1) % len(key)   #We will reach the next key letter in the key so we are incrementing our key index but when the lenght finishes, we have to start again. So, we are taking it's mode also.

    return plain                   #Our decrypted message will be returned after len(ciphertext) iterations.


def findKeyChar(str1, str2):
    startingPoint = ord("a")       #Reference point for calculating the numbers for the characters
    return chr(((ord(str1) - ord(str2))%len(alphabet))+startingPoint)      #It takes 2 chars, calculates their numbers, substracts them and converts the ascii number to char.

def breakFunc(plainText,cipherText):
    beginTime = datetime.datetime.now()      #To calculate the time passed while finding the key.
    end = 1                                  #To create possible keys from scratch.
    key_index = 0                            #To reach the key characters one by one.
    key = findKeyChar(cipherText[0], plainText[0])    #Our first key character. For example if the key stream is abcabcabcabc and our key is abc, we are reaching a by subtracting plain text from ciphertext.
    
    for i in range(1,len(cipherText)):
         control = findKeyChar(cipherText[i], plainText[i])      #We are reaching the next key character
         if (control != key[key_index]):                         #We are comparing with the key's next character with the new coming character. If they are different, that means until this character, the key must be updated.
             key = ""
             for j in range(0,end+1):
                 key += findKeyChar(cipherText[j], plainText[j])     #Key is recreating until that point.
             endTime = datetime.datetime.now()                   #In there, we might find the key, so we temporarily assign the endtime in here.
        
         else:                                                   #If new coming character is the same as the key's key_index value, that means 2 options, the key might start repeating itself or another character might come afterwards.
             if (key_index < len(key)):
                 tempKey = ""
                 for j in range(0,end+1):                        #Just in case we have to create a tempkey until that point to assign to the real key in the upcoming characters because if different character comes, we will have to update the key.
                     tempKey += findKeyChar(cipherText[j], plainText[j])    
                 key_index = (key_index +1) % len(key)                   #It is updated to reach and compare the next key character with the new coming character from key stream.
                 
                 if (i+1 != len(cipherText)):                #If we are not at the end of the stream
                     if ((findKeyChar(cipherText[i+1], plainText[i+1])!=key[key_index])):   #We have to check the next keystream character to ensure that we are not in the loop. For example, if the key is abca, abc is a key and abca is the tempKey until that point. Because a is equal to a, we have to understand if the repeating of the key is started or a is in the key. We are checking the next item which is a again in the key stream (abcaabcaabca) and comparing with b (second element of the key). Because they are different, we understood that there is no repetition, a should also be in the key.
                         key = tempKey     #Tempkey becomes the key
                         key_index = 0
                         endTime = datetime.datetime.now()   #In there, we might find the key again, so we temporarily assign the endtime in here.
                    
             if (key_index == len(key)):    #If key_index try to excess the length, it will go back to 0 to check the key indices with key stream.
                 key_index = 0
         end+=1   
    print("Elapsed time while finding the key: " ,endTime-beginTime)
    
    print("Key Length:", len(key))
    return key

def main():
    message="whatismyname"
    plain=arrangeMessage(message)
    key='ababcdababcd'
    isKeyValid = checkKey(key)
    
    if(isKeyValid==False):
        print("Key is not valid!")
        sys.exit()
        

    cipherText = encrypt(plain,key)
    print("Cipher Text: " +cipherText)
    
    print("-------------------------------------")
    plainText = decrypt(cipherText,key)
    print("Plain Text:  " +plainText)
    print("*************************************")
    foundKey = breakFunc(plainText,cipherText)
    print()
    print("Found key: " + foundKey),
    #    message = "I do well in school,and people think I am smart because of it.  But it’s not true. In fact, three years ago I struggled in school. However, two years ago I decided to get serious about school and made a few changes. First, I decided I would become interested in whatever was being taught, regardless of what other people thought. I also decided I would work hard every day and never give up on any assignment. I decided to never, never fall behind. Finally, I decided to make school a priority over friends and fun. After implementing these changes, I became an active participant in classroom discussions. Then my test scores began to rise. I still remember the first time that someone made fun of me because “I was smart.” How exciting! It seems to me that being smart is simply a matter of working hard and being interested. After all, learning a new video game is hard work even when you are interested. Unfortunately, learning a new video game doesn’t help you get into college or get a good job.akslsdhdfytreabbdakgjfdmgfkjdjnntuhghabsgbbdakgjfdmgfkjdjnffmddahahdhfghsjklmnohgjklmsdfghjkklmnbytreuwasojklmnxvcsgdhdkshhdhjskakslsdhdfytreabbdakgjfdmgfkjdjnntuhghabsgbbdakgjfdmgfkjdjnffmddahahdhfghsjklmnohgjklmsdfghjkklmnbytreuwasojklmnxvcsgdhdkshhdhjskakslsdhdfytreabbdakgjfdmgfkjdjnntuhghabsgbbdakgjfdmgfkjdjnffmddahahdhfghsjklmnohgjklmsdfghjkklmnbytreuwasojklmnxvcsgmsdfghjkklmnbytreuwasojklmnxvcsgdhdkshhdhjskakslsdhdfytreabbdakgjfdmgfkjdjnntuhghabsgbbdakgjfdmgfkjdjnffmddahahdhfghsjklmnohgjklmsdfghjkklmnbytreuwasojklmnxvcsgdhdkshhdhjskakslsdhdfytreabbdakgjfdmgfkjdjnntuhghabsgbbdakgjfdmgfkjdjnffmddahahdhfghsjklmnohgjklmsdfghjkklmnbytreuwasojklmnxvcsgdhdkshhdhjskakslsdhdfytreabbdakgjfdmgfkjdjnntuhghabsgbbdakgjfdmgfkjdjnffmddahahdhfghsjklmnohgjklmsdfghjkklmnbytreuwasojklmn"
    #    key='mhmncsgdhdkshhdhjskakslsdhdfythahdjgddshgdshjksdgjfghshajjgjagssgaytewtwyretyerwtuteruywteyueuywteyueewryurtretruyterutrtewyyuerrtyuewrreabbdakgjfdmgfkjdjnntuhghabsgbbdakgjfdmgfkjdjnffmddahahdhfghsjklmnohgjklmsdfghjkklmnbytreuwasojklmnxvcsgdhdkshhdhjskakslsdhdfytreabbdaahdhfghsjklmnohgjklmsdfghjkklmnbytreuwasojklmnxvcsgdhdkshhdhjskakslsdhdfytreabbdakgjfdmgfkjdjnntuhghabsgbbdakgjfdmgfkjdjnffmddahahdhfghsjklmnohgjklmsdfghjkklmnbytreuwasojklmnxvcsgdmgfkjdjnntuhghabsgbbdakgjfdmgfkjdjnffmddahahdhfghsjklmnohgjklmsdfghjkklmnbytreuwasojklmnxvcsgdhdkshhdhjskakslsdhdfytreabbkgmgfkjdjnntuhghabsgbbdakgjfdmgfkjdjnffmddahakslsdhdfytreabbdakgjfdmgfkjdjnntuhghabsgbbdakgjfdmgfkjdjnffmddahahdhfghsjklmnohgjklmsdfghjkklmnbytreuwasojklmnxvcsgdhdkshhdhjskakslsdhdfytreabbdakgjfdmgfkjdjnntuhghabsgbbdakgjfdmgfkjdjnffmddahahdhfghsjklmnohdkshhdhjskakslsdhdfytreabbdakgjfdmgfkjdjnntuhghabsgbbdakgjfdmgfkjdjnffmddahahdhfghsjklmnoh'

main()
      
        
               
        
        