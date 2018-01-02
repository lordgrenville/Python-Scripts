#TODO

#1 remove as many end characters as you added null bytes - thats wny there's extra output
#2 python int() won't convert from base85, must do this manually by iterating backwards, multiplying each
# by 85 ^ [position in list]

def solution(choice, text):
    if choice != "e" or "d":
        return "Please select either e for encode or d for decode"
    if choice == "e":
        return convert_to_ascii(text)
    else:
        return convert_from_ascii(text)

def convert_to_ascii(word):
    #padding
    while len(word) % 4 != 0:
        word += '\0'

    packets = [word[i:i + 4] for i in range(0, len(word),4)] 
    new_packets = []
    for p in packets:
        quartet = []
        concat = ""
        for letter in p:
            bin = format(ord(letter), "08b")
            concat += str(bin)
        i = int(concat, 2)
        while i > 85:
            quartet.append(chr(int(i%85) + 33))
            i /= 85
        quartet.append(chr(int(i) + 33))
        quartet.reverse()
        new_packets.append(quartet)
    print(new_packets)

def convert_from_ascii(word):
    while len(word) % 5 != 0:
        word += '\0'

    packets = [word[i:i + 5] for i in range(0, len(word),5)] 
    new_packets = []
    for p in packets:
        quintet = []
        concat = ""
        for letter in p:
            bin = format(int(ord(letter) - 33,85), "08b")
            concat += str(bin) + ","
        concat.split()
        answer = ""
        for l in concat:
         answer += chr(int(l,2))
    print(answer)

convert_from_ascii("87cURD_*#TDfTZ)+T")