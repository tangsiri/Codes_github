# -*- coding: utf-8 -*-
"""
Created on Wed Oct  9 12:07:08 2024

@author: pc22
"""







import pandas as pd
import os
i=1
# # تابع برای حذف سطرهای خالی
def remove_empty_lines(file_path):
    # فایل موقت برای نوشتن داده‌های بدون سطر خالی
    temp_file = file_path + '.tmp'
    
    with open(file_path, 'r') as infile, open(temp_file, 'w') as outfile:
        for line in infile:
            if line.strip():  # بررسی می‌کند که آیا سطر خالی است
                outfile.write(line)
    
    # جایگزینی فایل اصلی با فایل موقت
    os.replace(temp_file, file_path)

# # پوشه‌ی ورودی و خروجی
input_folder = 'D:\\PHD\\PHD\\Code\\GMs_IDA\\PEER'  # مسیر پوشه‌ی ورودی را مشخص کنید
output_folder = 'D:\\PHD\\PHD\\Code\\GMs_IDA\\IDA_Records'  # مسیر پوشه‌ی خروجی را مشخص کنید

# # ایجاد پوشه‌ی خروجی در صورت عدم وجود
os.makedirs(output_folder, exist_ok=True)

# # لیست اعداد برای ضرب
multipliers = [0.1 * i for i in range(1, 11)]  # 0.1, 0.2, ..., 1.0

# # پردازش تمام فایل‌ها در پوشه‌ی ورودی
for input_file in os.listdir(input_folder):
    # فیلتر کردن فایل‌های متنی با پسوند مشخص که حاوی 'UP' نباشند
    if input_file.endswith('.AT2') and '-UP' not in input_file:
        input_path = os.path.join(input_folder, input_file)
        
        # خواندن چهار سطر اول برای کپی کردن
        with open(input_path, 'r') as f:
            header_lines = [next(f) for _ in range(4)]
        
        # خواندن فایل متنی و نادیده گرفتن 4 سطر اول
        data = pd.read_csv(input_path, delim_whitespace=True, header=None, skiprows=4)
        
        # ضرب کردن هر عدد با هر ضریب و ذخیره در فایل‌های متنی جداگانه
        for multiplier in multipliers:
            modified_data = data * multiplier

            # جدا کردن اعداد مثبت و منفی
            positive_numbers = modified_data[modified_data[4] > 0]
            negative_numbers = modified_data[modified_data[4] <= 0]

            # اضافه کردن یک ستون خالی به اعداد مثبت
            positive_numbers = pd.concat([pd.DataFrame([' '] * len(positive_numbers), columns=[None]), positive_numbers], axis=1)

            # ایجاد DataFrame نهایی با اعداد مثبت و منفی
            final_output = pd.concat([negative_numbers, positive_numbers], ignore_index=True)

            # ساخت نام فایل خروجی در پوشه خروجی
            # output_file = os.path.join(output_folder, f'{os.path.splitext(input_file)[0]}_multiplier_{multiplier:.1f}.AT2')
            
            output_file = os.path.join(output_folder, f'{i}.AT2')
            i+=1
            # باز کردن فایل خروجی و نوشتن چهار سطر اول
            with open(output_file, 'w') as f:
                f.writelines(header_lines)  # نوشتن چهار سطر اول
                final_output.to_csv(f, sep='\t', index=False, header=False, float_format='%.7f')  # نوشتن داده‌ها

            # حذف سطرهای خالی از فایل خروجی
            remove_empty_lines(output_file)

            print(f'Operation successfully for {input_file} with multiplier:', multiplier)
