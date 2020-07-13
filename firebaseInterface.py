import os
import time
import firebase_admin
from firebase_admin import credentials
from firebase_admin.firestore import firestore
from config import USER_ID

os.environ[
    "GOOGLE_APPLICATION_CREDENTIALS"] = "./fridgeio-cbdb1-firebase-adminsdk-nw7ph-5512c75662.json"

firebase_admin.initialize_app(cred)
dbClient = firestore.Client()


def findProductByName(name):
    products = dbClient.collection('products').where(u'Name', u'==', name).get()
    return [x for x in products][0]


def addProductForUser(productName, userId=USER_ID):
    product = findProductByName(productName)
    newDocument = dbClient.collection('users').document(userId).collection('ownedProducts').document()
    productInstance = {
        'productId': product.id,
        'InsertionDate': int(round(time.time() * 1000)),
        'ExpirationDate': int(round(time.time() * 1000)) + product._data['ValidDays'] * 86400000,

    }
    newDocument.set(productInstance)
