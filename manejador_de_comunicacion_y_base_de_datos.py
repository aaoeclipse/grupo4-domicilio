import json
import psycopg2


db_host = "domicilio.cd1xq6ssophg.us-east-1.rds.amazonaws.com"
db_port = 5432
db_name = "postgres"
db_user = "postgres"
db_pass = "pinguilandia"
db_table_pedido = "Pedido"
db_table_user = "Usuario"

salones_disponibles = ['A101', 'A201', 'A301', 'E101', 'E201', 'E301', 'J101', 'J201', 'J301', 'H101', 'H201', 'H301', 'A102', 'A202', 'A302', 'E102', 'E202', 'E302', 'J102', 'J202', 'J302', 'H102', 'H202', 'H302', 'A103', 'A203', 'A303', 'E103', 'E203', 'E303', 'J103', 'J203', 'J303', 'H103', 'H203', 'H303', 'A104', 'A204', 'A304', 'E104', 'E204', 'E304', 'J104', 'J204', 'J304', 'H104', 'H204', 'H304', 'A105', 'A205', 'A305', 'E105', 'E205', 'E305', 'J105', 'J205', 'J305', 'H105', 'H205', 'H305', 'A106', 'A206', 'A306', 'E106', 'E206', 'E306', 'J106', 'J206', 'J306', 'H106', 'H206', 'H306', 'A107', 'A207', 'A307', 'E107', 'E207', 'E307', 'J107', 'J207', 'J307', 'H107', 'H207', 'H307', 'A108', 'A208', 'A308', 'E108', 'E208', 'E308', 'J108', 'J208', 'J308', 'H108', 'H208', 'H308', 'A109', 'A209', 'A309', 'E109', 'E209', 'E309', 'J109', 'J209', 'J309', 'H109', 'H209', 'H309', 'A110', 'A210', 'A310', 'E110', 'E210', 'E310', 'J110', 'J210', 'J310', 'H110', 'H210', 'H310']

def establecer_conexion_a_base_de_datos():
    conn = None
    try:
        conn = psycopg2.connect("dbname='%s' user='%s' host='%s' password='%s'" % (db_name, db_user, db_host, db_pass))
    except:
        print ("I am unable to connect to the database")
    return conn

connection = establecer_conexion_a_base_de_datos()
cursor = connection.cursor()


def crear_pedido_y_guardar_a_la_base_de_datos(event, context):
    """ Crea un pedido con la informacion mandada del bot """
    # Getting info of event (amazon lex)
    amount = event['currentIntent']['slots']['number']
    product = event['currentIntent']['slots']['producto']
    salon = event['currentIntent']['slots']['salon']
    bebida = event['currentIntent']['slots']['bebida']
    tarjeta = event['currentIntent']['slots']['tarjeta']

    # Error Handling
    # Verificacion de salon
    if salon not in salones_disponibles:
        return {
            "dialogAction":{
                "type": "Close",
                "fulfillmentState":"Fulfilled",
                "message": {
                    "contentType": "PlainText",
                    "content": "Lamentablemente el salon que escogio no se es correcto de la Universidad."
                }
            }
        }

    # Verificacion de Tarjeta
    if len(tarjeta) < 5:
        return {
            "dialogAction":{
                "type": "Close",
                "fulfillmentState":"Fulfilled",
                "message": {
                    "contentType": "PlainText",
                    "content": "Lamentablemente no se logro procesar la orden. Favor verificar el numero de tarjeta"
                }
            }
        }   
                

    fin_de_tarjeta = tarjeta[-4:]
    id_user = 1
    x = {
      "id":"1",
      "name": product,
      "price":"5.75",
      "quantity":amount,
      "salon":salon,
      "bebida":bebida
    } 
    json_to_send = json.dumps(x)

    crear_pedido_en_la_base_de_datos(json_to_send, fin_de_tarjeta)

    return {
        "dialogAction":{
            "type": "Close",
            "fulfillmentState":"Fulfilled",
            "message": {
                "contentType": "PlainText",
                "content": "Gracias por su orden de " + amount + " " + product + " al salon " + salon
            }
        }
    }

def crear_pedido_en_la_base_de_datos(json_to_send, fin_de_tarjeta):
    crear_pedido_en_la_base_de_datos = 'INSERT INTO public."Pedido"(id_pedido, pedido, fin_de_tarjeta, fecha, id_user) VALUES(DEFAULT,%s, %s, NOW(), 1)'
    cursor.execute(crear_pedido_en_la_base_de_datos, (json_to_send,fin_de_tarjeta))
    connection.commit()
    count = cursor.rowcount
    print (count, "Record inserted successfully into product table")