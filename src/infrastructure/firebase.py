import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore
from firebase_admin import messaging
from firebase_admin import db
from firebase_admin import auth
from firebase_admin import storage
from google.cloud.firestore import Query
import datetime as dt
from uuid import uuid4

import os
current_dir = os.path.abspath(os.path.dirname(__file__))

class Firestore():
    """
    Firestore(firebase_cred='service_account.json', name='DEFALUT')

    Estabilish a connection with a firestore database.
    firebase_cred : authentication file.
    name          : established connection's alias.
    """
    def __init__(self, firebase_cred=current_dir+"service_account.json", name='DEFALUT'): 
        cred = credentials.Certificate(firebase_cred)
        try:
            app = firebase_admin.initialize_app(cred)
        except:
            app = firebase_admin.initialize_app(cred, name=name)
        self.db      = firestore.client(app)
        self.storage = storage.bucket('gs://firebase-bucket.com')
        
        
    def read_collection(self, collection_name):
        """
        a list of document generators is returned.
        """
        ref = self.db.collection(collection_name)
        docs = ref.stream() # generator
        return list(docs)

    def read_document(self, collection_name, document_name):
        """
        a document generator is returned.
        document's name    -> {doc.id} 
        document's content -> {doc.to_dict()}
        """
        ref = self.db.collection(collection_name) 
        doc = ref.document(document_name).get()
        return doc
    
    def read_ordered_documents(self, collection_name, key='datetime', order_by = 'desc', limit=1):
        """
        a list of document generators is returned.
        """
        ref = self.db.collection(collection_name)
        if order_by=='desc':
            docs = ref.order_by(key, direction=Query.DESCENDING).limit(limit).stream()
        else:
            docs = ref.order_by(key).limit(limit).stream()
        return list(docs)

    def query_collection(self, collection_name, key, operator, value):
        """
        a list of document generators is returned.
        """
        ref = self.db.collection(collection_name)
        query_ref = ref.where(key, operator, value)
        docs = query_ref.stream()
        return list(docs)
    
    def query_sub_collection(self, collection_name, document_name, sub_collection_name, key, operator, value):
        """
        a list of document generators is returned.
        """
        ref = self.db.collection(collection_name).document(document_name).collection(sub_collection_name)
        query_ref = ref.where(key, operator, value)
        docs = query_ref.stream()
        return list(docs)

    def read_sub_document(self, collection_name, document_name, sub_collection_name, sub_document_name):
        '''
        a list of sub document generators is returned.
        '''
        ref = self.db.collection(collection_name).document(document_name).collection(sub_collection_name)
        docs = ref.document(sub_document_name).get()
        return list(docs)

    def read_ordered_sub_documents(self, collection_name, doccument_name, sub_collection_name, key='datetime', order_by = 'desc', limit=1):
        """
        a list of document generators is returned.
        """
        ref = self.db.collection(collection_name).document(doccument_name).collection(sub_collection_name)
        if order_by=='desc':
            docs = ref.order_by(key, direction=Query.DESCENDING).limit(limit).stream()
        else:
            docs = ref.order_by(key).limit(limit).stream()
        return list(docs)

    def create_document(self, collection_name, document_name, params):
        # Writing on the Firebase Database
        doc_ref = self.db.collection(collection_name).document(document_name)
        response = doc_ref.set(params)
        return response
    
    def update_document(self, collection_name, document_name, params):
        # Writing on the Firebase Database
        doc_ref = self.db.collection(collection_name).document(document_name)
        response = doc_ref.update(params)
        return response

    def update_sub_document(self, collection_name, document_name, sub_collection_name, sub_document_name, params):
        # Writing on th Firebase Database in Sub Collection
        ref = self.db.collection(collection_name).docuemnt_name(document_name).collection(sub_collection_name)
        response = ref.document(sub_document_name).update(params)
        return response
    
    def get_auth_user(self, email):
        user = auth.get_user_by_email(email)
        return user

    def read_sub_collection(self, collection_name, document_name, sub_collection_name):
        ref = self.db.collection(collection_name).document(document_name).collection(sub_collection_name)
        docs = ref.stream()
        return list(docs)

    def query_sub_document_data(self, collection_name, docuemnt_name, sub_collection_name, query_name):
        ref = self.db.collection(collection_name).document(docuemnt_name).collection(sub_collection_name)
        doc = ref.order_by(query_name).stream()
        return doc

    def query_one_sub_document_data(self, collection_name, docuemnt_name, sub_collection_name, query_name):
        ref = self.db.collection(collection_name).document(docuemnt_name).collection(sub_collection_name)
        docs = ref.order_by(query_name, direction=Query.DESCENDING).limit(1).stream()
        return list(docs)
    
    def create_sub_document(self, collection_name, document_name, sub_collection_name, sub_document_name, params):
        ref = self.db.collection(collection_name).document(document_name)
        response = ref.collection(sub_collection_name).document(sub_document_name).set(params)
        return response
        
    def messaging_device(self, message_model):

        response = messaging.send(message_model)

        return response