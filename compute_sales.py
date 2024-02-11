'''Programa que calcula las ventas totales de 2 archivos j'''
import sys
import json


class Sales:
    '''clase genera dictionario de productos'''
    def __init__(self, title: str,  price: str, quantity: str):
        self.title = title
        self.price = price
        self.quantity = quantity
        self.sales_list = []

    def add_sale(self, sales):
        '''agrega elemento a la lista'''
        self.sales_list.append(sales)

    def get_sales(self):
        '''muesta los elemtnos de la lista'''
        return self.sales_list


def exist_product(list_product, product, quantity):
    '''valida si existe uel producto en la lista'''
    res = False
    for prod in list_product:
        if product in prod["title"]:
            if prod["quantity"] > 0 and quantity > 0:
                res = True
            elif prod["quantity"] < 0 and quantity < 0:
                res = True
    return res


def acualiza_cantidad(list_product, value, new_quantity):
    '''actualiza la cantidad de productos vendidos'''
    for lista in list_product:
        if value in lista["title"]:
            if lista["quantity"] > 0 and new_quantity > 0:
                lista["quantity"] += new_quantity
            elif lista["quantity"] < 0 and new_quantity < 0:
                lista["quantity"] += new_quantity


def otener_valores(file_name):
    '''realiza la lectura del archivo'''
    try:
        with open(file_name, encoding='utf-8') as f:
            res = json.load(f)
            return res
    except FileNotFoundError:
        print(f"El archivo {file_name} no existe\n")
        return None
    except PermissionError:
        print(f"acceso denegado al archivo\n{file_name}")
        return None
    except OSError as e:
        print(f"error al consultar archivo: {e}")
        return None


def guardar(resultados, archivo):
    '''guarda e imprime los resultados'''
    with open('resultados.txt', 'a', encoding="utf-8") as f:
        print(f"\nResultados {archivo}\n", file=f)
        for line in resultados:
            print(line)
            f.write(line + '\n')


def main():
    '''Función principal'''
    if len(sys.argv) != 3:
        print("Numero de parametros invalidos.")
        print('python %s parameters_file.param', __file__)
    else:
        dic_products = {}
        dic_sales = {}
        file_name = ""
        for file in sys.argv:
            if file.endswith(".json"):
                jdata = otener_valores(file)
                if jdata is not None:
                    if "title" in jdata[0]:
                        dic_products = jdata
                    elif "SALE_ID" in jdata[0]:
                        dic_sales = jdata
                        file_name = file
        precios = calcular_precios(dic_products, dic_sales)
        resultado = obten_resultados(precios)
        guardar(resultado, file_name)


def calcular_precios(dic_products, dic_sales):
    '''genera lista con los productos, precios y la cantidad total vendida'''
    dic_prod = []
    for prod in dic_products:
        for sal in dic_sales:
            if prod["title"] == sal["Product"]:
                if not exist_product(dic_prod, prod["title"], sal["Quantity"]):
                    newd = Sales(title=prod["title"], price=prod["price"],
                                 quantity=sal["Quantity"])
                    dic_prod.append(newd.__dict__)
                else:
                    acualiza_cantidad(dic_prod, prod["title"], sal["Quantity"])
    return dic_prod


def obten_resultados(dic_sales):
    '''muestra los ventas totales por producto'''
    resume = []
    product = "title"
    price = "price"
    quantity = "quantity"
    total = "total"
    total_sale = 0
    resume.append('Product'.ljust(37) + 'Price'.ljust(7) +
                  "Quantity".ljust(10) + "Subtotal".ljust(6))
    for key in dic_sales:
        subt = key[price] * key[quantity]
        resume.append(f"{key[product]:.<35} $ {key[price]:<7.2f} " +
                      f"{key[quantity]:<6} $ {subt:<10.2f}")
        total_sale += subt
    resume.append(f"\n{total:.<52} $ {total_sale:,.2f}")
    return resume


if __name__ == "__main__":
    main()
