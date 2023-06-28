# from django.test import TestCase
# from . import converter_methods
import os
import json

# class TestDecimal(TestCase):
#     def setUp(self):
#         self.converter_object = converter_methods.CurrencyConverter()
#     def test_2_decimal(self):
#         self.assertEqual(self.converter_object.add_2_decimal(.01), '0.01', 'float .01 isn\'t OK')
#         self.assertEqual(self.converter_object.add_2_decimal(0), '0.00', 'int 0 isn\'t OK')
#         self.assertEqual(self.converter_object.add_2_decimal(5555.0), '5555.00', 'float 5555.0 isn\'t OK')
#         self.assertEqual(self.converter_object.add_2_decimal('15'), '15', 'int 15 isn\'t OK')
#         self.assertEqual(self.converter_object.add_2_decimal('1.0'), '1.0', 'float 1.0 isn\'t OK')
#         self.assertEqual(self.converter_object.add_2_decimal(5_555_555), '5555555.00', 'int 5_555_555 isn\'t OK')

def main():
    with open('../backup_rates_from_usd.json') as backup_file:
        backup = json.load(backup_file)
        print(backup)

if __name__ == '__main__':
    main()