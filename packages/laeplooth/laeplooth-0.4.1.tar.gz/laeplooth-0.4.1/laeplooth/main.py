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
    
    def spoonerism2syl(self, syl):
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
        if syl[posSwap1].startswith(('ลำ', 'ลัว', 'ละ', 'ลา', 'ลั', 'ลู' ,'ลอ')) and not any(char in thai_tonemarks for char in syl[posSwap1]):
                if not (syl[posSwap1].startswith('ลู') and len(syl[posSwap1]) < 3 and len(syl[posSwap2]) < 3):
                    syl[posSwap1] = 'ห' + syl[posSwap1]
        
        # ลินกู ลินกุน
        if syl[posSwap1][-1] in thai_consonants and syl[posSwap1][-1] not in ('ล', 'อ'):
                syl[posSwap2] = (syl[posSwap2] + syl[posSwap1][-1]).replace('ู', 'ุ')

        # ใล่ชู ใล่ชุ่ย, ไลปู ไลปุย
        if syl[posSwap1].startswith(('ใ', 'ไ')):
            syl[posSwap2] = syl[posSwap2].replace('ู', 'ุย')
            
        if any(char in thai_tonemarks for char in syl[posSwap1]):
                tone_mark = next((char for char in syl[posSwap1] if char in thai_tonemarks), '')
                syl[posSwap2] = syl[posSwap2][:1] + tone_mark + syl[posSwap2][1:]

        # ลำขู หลำขุม
        if syl[posSwap1][-1] == 'ำ':
            syl[posSwap2] = syl[posSwap2].replace('ู', 'ุม')
            
        # ลื้อซู ลื้อซู้ว
        if syl[posSwap1].endswith('ื้อ'):
            syl[posSwap2] = syl[posSwap2] + 'ว'
            
        # หละกรู หละกุ
        if syl[posSwap1].startswith('หละ'):
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
        if 'วุย' in syl[posSwap2]: 
            syl[posSwap2] = syl[posSwap2].replace('วุย', 'ุย')

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
        else:
            return "ลู"

    def check_syllable(self):
        # create syllable 
        # ลยามสุม หละสุหลามหยูม
        # ลโมยขุย หละขุโลยมุย
        # ตลาด -> ตะ หลาด
        if len(self.syl[0]) >= 3 and all(char in thai_consonants for char in self.syl[0][:2]) and (self.syl[0][1] != 'ว') and (self.syl[0][2] != 'ะ'):
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
        # if last syllable is 1 character merge it with previous syllable
        if len(self.syl[-1]) == 1:
            self.syl[-2] = self.syl[-2] + self.syl[-1]
            self.syl.pop()
            
    def get_result(self):
        full = ""
        self.check_syllable()
        print(self.syl)
        for inSyl in self.syl:
            inSyl = [self.check_condition(inSyl), inSyl]
            full += "".join(self.spoonerism2syl(inSyl))
        
        return full


def loo(text):
    result = Translator(text).get_result()
    print(result)
    return result









