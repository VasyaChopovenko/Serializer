import tkinter
from functools import partial
from tkinter import *
import json
import csv
import dicttoxml
import xmltodict

filePath = "D:"


class Model:
    def __init__(self, first_name, second_name, company, x):
        self.first_name = first_name
        self.second_name = second_name
        self.company = company
        self.x = x


class CSVSerDes:
    def serialize(self, obj):
        with open(filePath + "/serialized.csv", "w") as file:
            object_fields = obj.__dict__
            field_names = list(object_fields.keys())

            writer = csv.DictWriter(file, field_names)
            writer.writeheader()
            writer.writerow(object_fields)

    def deserialize(self, obj):
        with open(filePath + "/serialized.csv", "r") as file:
            reader = csv.DictReader(file)
            for field in reader:
                for objField in obj.__dict__:
                    obj.__dict__[objField] = field[objField]
            return obj


class JSONSerDes:
    def serialize(self, obj):
        with open(filePath + "/serialized.json", "w") as file:
            json.dump(obj.__dict__, file)

    def deserialize(self, obj):
        with open(filePath + "/serialized.json", "r") as file:
            obj.__dict__ = json.load(file)
            return obj


class XMLSerDes:
    def serialize(self, obj):
        with open(filePath + "/serialized.xml", "w") as file:
            file.write(str(dicttoxml.dicttoxml(obj.__dict__).decode('utf-8')))

    def deserialize(self, obj):
        with open(filePath + "/serialized.xml", "rb") as file:
            xml_dict = xmltodict.parse(file)['root']
            for field in xml_dict:
                obj.__dict__[field] = xml_dict[field]['#text']
            return obj


class MainWindow:
    def __init__(self, custom_model):
        self.custom_model = custom_model
        self.title = "Serializer"
        self.bound_property_and_entry = dict()
        self.serializers = {"JSON": JSONSerDes(), "XML": XMLSerDes(), "CSV": CSVSerDes()}

    def create(self):
        window = Tk()
        window.title(self.title)
        window.resizable(False, False)

        window.geometry("400x400")
        model_fields = self.custom_model.__dict__

        for field in model_fields:
            label = Label(text=field)
            label.pack()

            field_value = StringVar()
            field_value.set(model_fields[field])
            field_entry = Entry(textvariable=field_value)
            field_entry.pack()

            self.bound_property_and_entry[field] = field_value

        menu_value = StringVar()
        menu_value.set("JSON")
        om = OptionMenu(window, menu_value, "JSON", "XML", "CSV")
        om.config(width=6, height=1, bg='#ecd8c8')

        menu_value.get()
        ser_btn = Button(text="Serialize", command=lambda: self.btn_click_ser(menu_value.get()), width=10, height=1, bg='#f6ce79')
        ser_btn.pack(pady=5)
        des_btn = Button(text="Deserialize", command=lambda: self.btn_click_des(menu_value.get()), width=10, height=1, bg='#c5bffb')
        des_btn.pack()
        om.pack(pady=5)
        om.place()

        window.mainloop()

    def btn_click_ser(self, ser_type):
        model_fields = self.custom_model.__dict__
        for field in model_fields:
            model_fields[field] = self.bound_property_and_entry[field].get()

        self.serialize(ser_type)

    def serialize(self, ser_type):
        self.serializers[ser_type].serialize(self.custom_model)

    def btn_click_des(self, des_type):
        self.deserialize(des_type)

    def deserialize(self, des_type):
        deserialized_object = self.serializers[des_type].deserialize(self.custom_model)
        for field in deserialized_object.__dict__:
            self.bound_property_and_entry[field].set(deserialized_object.__dict__[field])


model = Model("John", "Khon", "Google", "x")

MainWindow(model).create()
