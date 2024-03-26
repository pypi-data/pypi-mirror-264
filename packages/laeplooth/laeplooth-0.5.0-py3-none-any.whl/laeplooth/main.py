import re
from pythainlp.tokenize import syllable_tokenize
from pythainlp import thai_consonants, thai_tonemarks




class Translator:
    def __init__(self, inputText):
        self.inputText = inputText
        self.syl = syllable_tokenize(inputText)
        self.remove_special_tokens()
        self.specialCase = re.compile(r'(อย|ห[งญนมยรลว]|กร|คร|ปร|พร|ตร|กล|คล|ปล|พล|กว|คว|[\u0E00-\u0E2E])')
        self.high_consonants = ['ข', 'ฃ', 'ฉ' ,'ฐ' ,'ถ' ,'ผ' ,'ฝ' ,'ศ' ,'ษ' ,'ส', 'ห']
        self.low_consonants = ['ค', 'ฅ', 'ฆ', 'ง', 'ช', 'ซ', 'ฌ', 'ญ', 'ฑ', 'ฒ', 'ณ', 'ท', 'ธ', 'น', 'พ', 'ฟ', 'ภ', 'ม', 'ย', 'ร', 'ล', 'ว', 'ฬ',  'ฮ']
        self.spell_1 = ['ก', 'ข', 'ค', 'ฆ']
        self.spell_2 = ['จ' , 'ด' , 'ต' ,'ถ' ,'ท' , 'ธ' , 'ฎ' , 'ฏ' , 'ฑ' , 'ฒ' , 'ช' , 'ซ' , 'ศ' , 'ษ' , 'ส']
        self.spell_3 = ['บ', 'ป', 'พ', 'ภ', 'ฟ', 'ฝ']
        self.spell_4 = ['ห', 'ฮ']
        self.spell_5 = ['ง']
        self.spell_6 = ['ม']
        self.spell_7 = ['ย']
        self.spell_8 = ['ว']
        self.spell_9 = ['ญ' ,'ณ', 'น', 'ร','ล', 'ฬ']
        self.short_vowel = ['-ะ' , '-ั' , '-ิ' , '-ึ' , '-ุ' , 'เ-ะ' , 'แ-ะ' , 'เ-็' , 'แ-็' , 'โ-ะ' , 'เ-าะ' , 'เ-อะ' , 'เ-ียะ' , 'เ-ือะ' ,'-ัวะ' , 'ฤ' , 'ฦ' , '-ำ' , 'ไ-' , 'ใ-'  , 'เ-า']
        self.long_vowel = ['-า',  '-ี', '-ื', '-ู', 'เ-', 'แ-', 'โ-', '-อ', 'เ-อ', 'เ-ีย', 'เ-ือ', '-ัว', 'ฤๅ', 'ฦๅ']
        
        

    def remove_special_tokens(self):
        if "<s/>" in self.syl:
            self.syl.remove("<s/>")

    def check_swap(self, syl):
        if len(syl) == 2:
            syl[0], syl[1] = syl[1], syl[0]
        elif len(syl) == 3:
            syl[0], syl[2] = syl[2], syl[0]
        return syl

    def word2alpha(self, word):
        match = self.specialCase.search(word)
        if match:
            return match.group(), match.start()
        return None, None
    
    def spoonerism2syl(self, syl, origInSyl):
        syl = self.check_swap(syl)
        if len(syl) == 2:
            posSwap1, posSwap2 = 0, 1
        elif len(syl) == 3:
            posSwap1, posSwap2 = 0, 2
        else:
            raise ValueError('Cannot swap syllables of length other than 2 or 3')

        alpha1, pos1 = self.word2alpha(syl[posSwap1])
        alpha2, pos2 = self.word2alpha(syl[posSwap2])


        s1, s2 = list(syl[posSwap1]), list(syl[posSwap2])

        if len(alpha1) == 1:
            s1[pos1], s2[pos2] = alpha2, alpha1
        else:
            s1[pos1], s1[pos1 + 1], s2[pos2] = 'ห', alpha2, alpha1

        syl[posSwap1], syl[posSwap2] = "".join(s1), "".join(s2)
        
   


        # ลำ ลัว ละ  
        if self.is_h_prefix(origInSyl) and not 'ห' in syl[posSwap1]:
            syl[posSwap1] = 'ห' + syl[posSwap1]
            if syl[posSwap1].startswith('หแ'):
                syl[posSwap1] = syl[posSwap1].replace('หแ', 'แห')
                
        # หมู
        if('หลู' == syl[posSwap1]):
            syl[posSwap1] = syl[posSwap1].replace('หลู', 'ลู')

        # ลินกู ลินกุน
        if self.get_last_con(syl[posSwap1]) in thai_consonants and self.get_last_con(syl[posSwap1]) not in ('ล', 'อ'):
                # มาก
                if  self.is_short_vowel(syl[posSwap1]):
                    syl[posSwap2] = (syl[posSwap2] + syl[posSwap1][-1]).replace('ู', 'ุ')
                else:
                    syl[posSwap2] = (syl[posSwap2] + syl[posSwap1][-1])

        # ใล่ชู ใล่ชุ่ย, ไลปู ไลปุย
        if syl[posSwap1].startswith(('ใ', 'ไ')):
            syl[posSwap2] = syl[posSwap2].replace('ู', 'ุย')

        if any(char in thai_tonemarks for char in syl[posSwap1]):
                tone_mark = next((char for char in syl[posSwap1] if char in thai_tonemarks), '')
                if(alpha1):
                    syl[posSwap2] = syl[posSwap2][:2] + tone_mark + syl[posSwap2][2:]
                else:
                    syl[posSwap2] = syl[posSwap2][:1] + tone_mark + syl[posSwap2][1:]

        # ลำขู หลำขุม
        if syl[posSwap1][-1] == 'ำ':
            syl[posSwap2] = syl[posSwap2].replace('ู', 'ุม')
            
        # ลื้อซู ลื้อซู้ว
        if syl[posSwap1].endswith('ื้อ'):
            syl[posSwap2] = syl[posSwap2] + 'ว'
            
        # หละกรู หละกุ
        if self.is_short_vowel(syl[posSwap1]):
            syl[posSwap2] = syl[posSwap2].replace('ู', 'ุ')
            
        # ลาษดู หลาษดูษ
        if syl[posSwap1].startswith('หลา'):
            syl[posSwap2] = syl[posSwap2].replace('ุ', 'ู')
            
        #  ใหลครุย ใลครุย
        if syl[posSwap1].endswith('หล') and syl[posSwap2][0] in thai_consonants:
            syl[posSwap1] = syl[posSwap1].replace('หล', 'ล')
            
        # เหลือหลู เสือหลุู
        if syl[posSwap1].startswith(('เหลือ')):
            syl[posSwap1] = syl[posSwap1].replace('หล', 'ส')
            
        # ซองลุง ซองลูง
        if 'อ' in syl[posSwap1]:
            syl[posSwap2] = syl[posSwap2].replace('ุ', 'ู')
            
        # ซู้รู้ ซู้รี้ ซูบลุบ ซูบลีบ
        if 'ู' in syl[posSwap1] and ('ู' in syl[posSwap2] or 'ุ' in syl[posSwap2]):
            syl[posSwap2] = syl[posSwap2].replace('ู', 'ี').replace('ุ', 'ี')
            
        # ซุมรุม ซุมริม
        if 'ุ' in syl[posSwap1] and 'ุ' in syl[posSwap2]:
            syl[posSwap2] = syl[posSwap2].replace('ุ', 'ิ')
        
        # หลย ลวย
        if syl[posSwap1] == 'หลย':
            syl[posSwap1] = 'ลวย'
            
        # ลวยควุย ลวยคุย
        if 'วูย' in syl[posSwap2]: 
            syl[posSwap2] = syl[posSwap2].replace('วูย', 'ุย')
            
        if '้ี' in syl[posSwap2]:
            syl[posSwap2] = syl[posSwap2].replace('้ี', 'ี้')
            
        # เหลา แหลง
        syl[posSwap1] = syl[posSwap1].replace('หส', 'ส')
        syl[posSwap2] = syl[posSwap2].replace('ุา', 'ุ').replace('ูา', 'ู')

        return syl

    def check_condition(self, syl):
        alpha_cond, _ = self.word2alpha(syl)
        syl_list_cond = list(syl)

        if alpha_cond in ['ร', 'ล']:
            return 'ซู'
        elif 'ุ' in syl_list_cond or 'ู' in syl_list_cond:
            return 'ลี'
        elif alpha_cond in ['ร', 'ล'] and ('ุ' in syl_list_cond or 'ู' in syl_list_cond):
            return 'ซี'
        elif alpha_cond in ['หล','หร']:
            return 'สู'
        else:
            return "ลู"

    def check_syllable(self):
        #  กรรม 
        if len(self.syl[0]) > 3 and 'รรม' in self.syl[0]:
            self.syl = [self.syl[0][0] + 'ำ']
            
        # ขนม ถนน
        if len(self.syl[0]) == 3 and all(char in thai_consonants for char in self.syl[0]) and self.syl[0][1] != 'อ' and self.syl[0][1] != 'ว':
            self.syl = [self.syl[0][0] + 'ะ', 'ห' + self.syl[0][1:]] + self.syl[1:]
        
        # ลยามสุม หละสุหลามหยูม
        # ลโมยขุย หละขุโลยมุย
        # ตลาด -> ตะ หลาด
        #  prevent อย
        if len(self.syl[0]) > 3 and all(char in thai_consonants for char in self.syl[0][:2]) and (self.syl[0][1] != 'ว') and (self.syl[0][2] != 'ะ') and 'รร' not in self.syl[0] and self.syl[0][:2] != 'อย':
            self.syl = [self.syl[0][:1] + 'ะ', 'ห' + self.syl[0][1:]] + self.syl[1:]
        # เฉลย 
        if len(self.syl[0]) > 3 and self.syl[0].startswith('เ')  and self.syl[0].endswith('ลย'):
            self.syl = [self.syl[0][1] + 'ะ' , self.syl[0][0] + 'ห' + self.syl[0][-2:]]
            
        # แสดง
        if len(self.syl[0]) > 3 and self.syl[0].startswith('แ') and self.syl[0].endswith('ดง'):
            self.syl = [self.syl[0][1] + 'ะ', self.syl[0][0]  + self.syl[0][-2:]]
        # แสลง   
        if len(self.syl[0]) > 3 and self.syl[0].startswith('แส') and self.syl[0].endswith('ลง'):
            self.syl = [self.syl[0][1] + 'ะ', self.syl[0][0] + 'ห'  + self.syl[0][-2:]]
        # ไฉน
        if self.syl[0] == 'ไฉน':
            self.syl = ['ฉะ', 'ไหน']
        # เสมียน เกษียณ เถลิง
        if len(self.syl[0]) > 4 and self.syl[0].startswith('เ') and (self.syl[0].endswith('ียน') or self.syl[0].endswith('ียณ') or self.syl[0].endswith('ลิง')):
            if self.syl[0][1] in self.high_consonants:
                self.syl = [self.syl[0][1] + 'ะ', self.syl[0][:1] + 'ห' + self.syl[0][2:]]
            else:
                self.syl = [self.syl[0][1] + 'ะ', self.syl[0][:1]  + self.syl[0][2:]]
        # เสลา 
        if self.syl[0] == 'เสลา':
            self.syl = ['สะ', 'เหลา']

        # ขโมย -> ขะ โมย 
        if (self.syl[0][0] in thai_consonants and self.syl[0][1] not in thai_consonants) and all(char in thai_consonants for char in self.syl[0][-2:]) and self.syl[0][-2] != 'อ':
            self.syl = [self.syl[0][:1] + 'ะ',  self.syl[0][1:]] + self.syl[1:]
            
            
        # อิดอก
        index = next((i for i, s in enumerate(self.syl) if s.startswith('อิด')), None)
        if index is not None:
            self.syl[index] = self.syl[index][:2]
            self.syl[index + 1] = 'ด' + self.syl[index + 1]

                
        # if last syllable is 1 character merge it with previous syllable
        merged_array = []
        for i, elem in enumerate(self.syl):
            if len(elem) == 1 and i > 0:
                merged_array[-1] += elem
            else:
                merged_array.append(elem)
                
        self.syl = merged_array
            
    def get_first_con(self, syl):
        return next((char for char in syl if char in thai_consonants), '')
    
    def get_last_con(self, syl):   
        return next((char for char in syl[::-1] if char in thai_consonants), '')
    
    def is_short_vowel(self, syl):
        short_matches = re.findall('|'.join(self.short_vowel).replace('-', r'\w*'), syl)
        return len(short_matches) > 0
    
    def is_long_vowel(self, syl):
        long_matches = re.findall('|'.join(self.long_vowel).replace('-', r'\w*'), syl)
        return len(long_matches) > 0
    
    def is_death(self, syl): 
        # สระเสียงสั้น แม่กอกา
        if self.is_short_vowel(syl) and syl[-1] not in thai_consonants:
            return True
        # มีพยัญชนะ ตัวเดียว + ไม่มีสระเสียงยาว
        if len([char for char in syl if char in thai_consonants]) == 1 and not self.is_long_vowel(syl):
            return True
        # แม่ กบ กด กก
        if any( self.get_last_con(syl) in spell for spell in [self.spell_1, self.spell_2, self.spell_3]):
            if len([char for char in syl if char in thai_consonants]) > 1:
                return True
        return False
    
    def is_h_prefix(self, syl):
        # อักษรต่ำ ไม่มี ห
        if self.get_first_con(syl) in self.low_consonants:
            return False
        # อักษรสูง มี ห 
        if self.get_first_con(syl) in self.high_consonants:
            return True
        # กลาง เป็น ไม่มี ห
        if self.get_first_con(syl) not in [self.high_consonants, self.low_consonants] and not self.is_death(syl):
            return False
        # แม่ กอ กา + ไ 
        if len(syl) == 2 and syl[0] == 'ไ':
            return False
        return True

    
    def get_result(self):
        full = ""
        print(self.syl)
        self.check_syllable()
        print(self.syl)
        for inSyl in self.syl:
            origInSyl = inSyl
            inSyl = [self.check_condition(inSyl), inSyl]
            full += "".join(self.spoonerism2syl(inSyl,origInSyl))
        
        return full


def loo(text):
    result = Translator(text).get_result()
    print(result)
    return result









