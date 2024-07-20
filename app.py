#!/usr/bin/env python
# -*- coding: UTF-8 -*-

__author__ = 'Jose E. Morales Ventura'
__date__ = '01/07/2024'
__description__ = ""
__url__ = "https://softnow-ptv.homes"

import os
import flask_bcrypt
from flask_cors import CORS
from flask import request
from flask import  render_template, Flask
from flask_restful import  Api
import pyautogui
import cv2
from pyzbar import pyzbar
import numpy as np

import time

app = Flask(__name__, template_folder='templates', static_folder='static')
app.config['UPLOAD_EXTENSIONS'] = ['.jpg', '.png']
app.config['MAX_CONTENT_LENGTH'] = 1024 * 1024 * 50
app.config['UPLOAD_PATH'] = 'uploads'
app.config['TEMPLATES_AUTO_RELOAD'] = True

secret = os.urandom(32)
app.config['SECRET_KEY'] = secret
app.secret_key = secret

bcrypt = flask_bcrypt.Bcrypt(app)
CORS(app)
api = Api(app)

PORT_FLASK = 5000

@app.errorhandler(404)
def page_not_found(error):
    '''
    '''
    return render_template('404.html'), 404

@app.errorhandler(Exception)
def handle_exception(e):
    '''
    '''
    return render_template('500.html'), 500

@app.route('/scan', methods=['POST'])
def upload_file():
    '''
    '''

    def read_barcodes(image:object) -> str:
        '''
        '''

        # Convertir la imagen a formato compatible con OpenCV
        image = cv2.imdecode(np.frombuffer(image.read(), np.uint8), cv2.IMREAD_COLOR)

        # Encontrar los códigos de barras en la imagen
        barcodes = pyzbar.decode(image)

        # Lista para almacenar los datos de los códigos de barras
        barcode_data_list = []

        for barcode in barcodes:
            # Extraer la información del código de barras
            barcode_data = barcode.data.decode("utf-8")
            barcode_data_list.append(barcode_data)

        if barcode_data_list:
            return ''.join(barcode_data_list)
        else:
            return '-'

    image_file = request.files['image']
    if not image_file:
        return render_template('message.html', message='File not found')
    else:
        #file_path = app.config['UPLOAD_PATH'] + '/' + image_file.filename
        #image_file.save(file_path)

        barcode = read_barcodes(image_file)
        #print(barcode)
        #barcode = '1234'
        time.sleep(1)
        pyautogui.write(barcode)

        return render_template('main.html')

@app.route('/')
def main() -> object:
    '''
    Vista principal
    '''
    return render_template('main.html')

def set_host(domain_name) -> None:
    '''
    '''

    #C:\Windows\System32\drivers\etc
    # Asigna el nombre de dominio y dirección IP en la red local
    nombre_de_dominio = 'barcode.local'
    direccion_ip = '10.0.0.3'

    # Agrega el nombre de dominio y dirección IP en el archivo hosts
    with open(r"C:\Windows\System32\drivers\etc\hosts", "a") as archivo_hosts:
        archivo_hosts.write(direccion_ip + '\t' + nombre_de_dominio + '\n')
    
if __name__ == '__main__':
    #set_host('qcode.local')
    app.run(debug=True, port=PORT_FLASK, host='0.0.0.0')
