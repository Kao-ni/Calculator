from customtkinter import *
from buttons import *
import darkdetect
from PIL import Image
from settings import *
try:
    from ctypes import *
except:
    pass

class Calculator(CTk):
    def __init__(self, is_dark):
        
        #setup
        super().__init__(fg_color=(WHITE, BLACK))
        
        if is_dark:
            set_appearance_mode('dark')
            self.iconbitmap('images/empty_dark.ico')
        else:
            set_appearance_mode('light')
            self.iconbitmap('images/empty_light.ico')
        
        self.geometry(f'{APP_SIZE[0]}x{APP_SIZE[1]}')
        self.title('')
        self.title_bar_color(is_dark)
        
        #grid layout
        self.rowconfigure(list(range(MAIN_ROWS)), weight = 1, uniform = 'a')
        self.columnconfigure(list(range(MAIN_COLUMNS)), weight = 1, uniform = 'a')
        
        #data
        self.result_string = StringVar(value = '0')
        self.formula_string = StringVar(value='')
        self.display_nums = list()
        self.full_operation = list()
        
        #widgets
        self.create_widgets()
        
        self.mainloop()
        
    def create_widgets(self):
        
        #fonts
        main_font = CTkFont(family = FONT, size = NORMAL_FONT_SIZE)
        result_font = CTkFont(family = FONT, size = OUTPUT_FONT_SIZE)
        
        #output labels
        OutputLabel(self, 0, 'SE', main_font, self.formula_string) #equation
        OutputLabel(self, 1, 'E', result_font, self.result_string) #result
        
        #clear (AC) button
        Button(
            parent = self, 
            func = lambda: (
                self.result_string.set('0'), 
                self.formula_string.set(''),
                self.display_nums.clear(),
                ),
            text = OPERATORS['clear']['text'], 
            col = OPERATORS['clear']['col'], 
            row = OPERATORS['clear']['row'],
            font = main_font)
        
        #percentage (%) button
        Button(
            parent = self, 
            func = self.percent,
            text = OPERATORS['percent']['text'], 
            col = OPERATORS['percent']['col'], 
            row = OPERATORS['percent']['row'],
            font = main_font)
        
        #invert button
        invert_image = CTkImage(
            light_image = Image.open(OPERATORS['invert']['image path']['dark']), 
            dark_image = Image.open(OPERATORS['invert']['image path']['light']))
        Image_button(
            parent = self,
            func = self.invert, 
            col = OPERATORS['invert']['col'],
            row = OPERATORS['invert']['row'],
            image = invert_image)
    
        #number buttons
        for num, data in NUM_POSITIONS.items():
            NumButton(
                parent = self, 
                text = num, 
                func = lambda value=num: (
                    self.display_nums.append(str(value)),
                    self.result_string.set(''.join(self.display_nums))),
                col = data['col'], 
                row = data['row'],
                font = main_font,
                span = data['span'])
            
        #operator buttons
        for operator, data in MATH_POSITIONS.items():
            if data['image path']:
                divide_image = CTkImage(
                    light_image = Image.open(data['image path']['dark']), 
                    dark_image = Image.open(data['image path']['light']))
                MathImageButton(
                    parent = self, 
                    operator = operator, 
                    func = self.math_press,
                    col = data['col'], 
                    row = data['row'], 
                    image = divide_image
                )
            else:
                MathButton(
                    parent = self, 
                    text = data['character'], 
                    operator = operator,
                    func = self.math_press,
                    col = data['col'], 
                    row = data['row'],
                    font = main_font)

    #button functions      
    def percent(self):
        
        if self.display_nums and int(''.join(self.display_nums)) > 0:
            self.result_string.set((float(''.join(self.display_nums))) / 100)
            self.display_nums = [(float(''.join(self.display_nums))) / 100]
            self.display_nums = [(str(self.display_nums[0]))]
        
    def invert(self):
        
            if self.display_nums and self.display_nums[0] != '-':
                self.display_nums.insert(0, '-')
            elif self.display_nums and self.display_nums[0] == '-':
                self.display_nums.pop(0)
            self.result_string.set(''.join(self.display_nums))
        
    def math_press(self, value):
        
        if self.result_string.get() != '0':
            self.full_operation.append(''.join(self.display_nums))
            
            if value != '=':
                
                #update data
                self.full_operation.append(value)
                self.display_nums.clear()
                
                #update output
                self.result_string.set('')
                self.formula_string.set(' '.join(self.full_operation))
                
            else:
                
                #evaluate
                formula = ' '.join(self.full_operation)
                result = eval(formula)
                
                #format result
                if isinstance(result, float):
                    if result.is_integer():
                        result = int(result)
                    else:
                        result = round(result, 6)
                
                #update data
                self.full_operation.clear()
                self.display_nums = [str(result)]
                
                #update output
                self.formula_string.set(formula)
                self.result_string.set(result)
    
    def title_bar_color(self, is_dark):
        
        try:
            HWND = windll.user32.GetParent(self.winfo_id())
            DWMWA_ATTRIBUTE = 35
            COLOR = TITLE_BAR_HEX_COLORS['dark'] if is_dark else TITLE_BAR_HEX_COLORS['light']
            windll.dwmapi.DwmSetWindowAttribute(HWND, DWMWA_ATTRIBUTE, byref(c_int(COLOR)), sizeof(c_int))
        except:
            pass

class OutputLabel(CTkLabel):
    def __init__(self, parent, row, anchor, font, string_var):
        super().__init__(master=parent, font=font, textvariable=string_var)
        self.grid(column = 0, columnspan = 4, row = row, sticky = anchor, padx = 10)

if __name__ == "__main__":
    Calculator(True)