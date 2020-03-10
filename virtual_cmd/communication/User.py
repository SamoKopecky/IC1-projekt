from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes

import os
import sys
import uuid

sys.path.insert(1, "../../")
from virtual_cmd.communication import utils


class User:

    def __init__(self, ca_ip_addr, user_ip_addr):
        """
            Creating variables to store things in later in the code, or initializing them right away
            other_* = variables of the other user we are communicating with
            active_socket = socket to communicate trough
        """
        self.aes_key = bytes()
        self.aes_iv = bytes()
        self.private_key, self.public_key = utils.generate_rsa_keys()
        self.cipher = Cipher
        self.my_certificate = None
        self.other_certificate = None
        self.ca_certificate = None
        self.active_socket = utils.socket.socket()
        self.ca_port = 3333
        self.user_port = 4444
        self.name = str(uuid.uuid1())
        self.ca_ip_addr = ca_ip_addr
        self.user_ip_addr = user_ip_addr
        self.received_messages = []

    def create_certificate_request(self):
        """
            We create certificate request in this function,
            email land common name are derived from the users chosen name,
            sign() functions fill the request with public key that's why we dont use the .public_key() method
            :return: returns created certificate request
        """
        name = utils.x509.Name([
            utils.x509.NameAttribute(utils.NameOID.COUNTRY_NAME, 'CZ'),
            utils.x509.NameAttribute(utils.NameOID.JURISDICTION_STATE_OR_PROVINCE_NAME, 'Czech Republic'),
            utils.x509.NameAttribute(utils.NameOID.LOCALITY_NAME, 'Brno'),
            utils.x509.NameAttribute(utils.NameOID.ORGANIZATION_NAME, 'University of Technology'),
            utils.x509.NameAttribute(utils.NameOID.COMMON_NAME, '{}-vut.cz'.format(self.name)),
            utils.x509.NameAttribute(utils.NameOID.EMAIL_ADDRESS, '{}@vut.cz'.format(self.name)),
        ])
        return utils.x509.CertificateSigningRequestBuilder() \
            .subject_name(name) \
            .sign(self.private_key, utils.hashes.SHA256(), utils.default_backend())

    def send_request_to_ca(self):
        """
            In here we get ready for communication, convert the certificate request to PEM format so
            that it can be sent and then we send it and then we close the connection with CA
            if the verification failed try again
        """
        self.active_socket = utils.start_sending(self.ca_ip_addr, self.ca_port)
        utils.send_data(self.active_socket, b'sending cert request', 'request to start communication')
        data_to_send = self.create_certificate_request().public_bytes(utils.PEM)
        utils.send_data(self.active_socket, data_to_send, 'certificate request')
        received_data = utils.receive_data(self.active_socket, 'certificate or verification failure')
        if received_data == b'verification failed':
            print('verification failed trying again')
            utils.finish_connection(self.active_socket)
            self.send_request_to_ca()
            return
        self.my_certificate = utils.x509.load_pem_x509_certificate(received_data, utils.default_backend())
        utils.finish_connection(self.active_socket)

    def exchange_certificates_and_keys(self, state):
        """
            We decide which user will be sending and receiving and then exchange certificates and AES key
        """
        if state == 'receive':
            self.finish_exchange_of_certificates()
            self.receive_aes_key()
        elif state == 'send':
            self.start_exchange_of_certificates()
            self.generate_and_send_aes_key()
        self._create_aes_cipher()

    def finish_exchange_of_certificates(self):
        """
            first the user receives the certificate and then he sends his certificate
        """
        self.active_socket = utils.start_receiving(self.user_port)
        self.receive_and_verify_certificate()
        self.send_certificate()

    def receive_and_verify_certificate(self):
        """
            certificate is received , if the verification is false an exception is thrown and program exists
        """
        received_data = utils.receive_data(self.active_socket, 'certificate')
        certificate = utils.x509.load_pem_x509_certificate(received_data, utils.default_backend())
        utils.rsa_verify_certificate(self.ca_certificate, certificate)
        self.other_certificate = certificate

    def get_ca_certificate(self):
        """
            requests the CA self singed certificate
        """
        ca_socket = utils.start_sending(self.ca_ip_addr, self.ca_port)
        utils.send_data(ca_socket, b'requesting your self-signed certificate', 'request for self-signed certificate')
        data = utils.receive_data(ca_socket, 'ca certificate')
        self.ca_certificate = utils.x509.load_pem_x509_certificate(data, utils.default_backend())
        utils.rsa_verify_certificate(self.ca_certificate, self.ca_certificate)
        utils.finish_connection(ca_socket)

    def receive_aes_key(self):
        """
            same as function receiving_certificate but this time the user receives AES shared key
            aes is decrypted with RSA
        """
        key = utils.receive_data(self.active_socket, 'encrypted aes key')
        self.aes_iv = utils.receive_data(self.active_socket, 'aes iv')
        self.aes_key = utils.rsa_decrypt(key, self.private_key)

    def start_exchange_of_certificates(self):
        """
            same thing as receive but reverse, user sends then receives the certificate
        """
        self.active_socket = utils.start_sending(self.user_ip_addr, self.user_port)
        self.send_certificate()
        self.receive_and_verify_certificate()

    def send_certificate(self):
        """
            the certificate is sent
        """
        pem_certificate = self.my_certificate.public_bytes(utils.PEM)
        utils.send_data(self.active_socket, pem_certificate, 'certificate')

    def generate_and_send_aes_key(self):
        """
            this method generates the shared AES key and vector which it will then send to the other user
            encrypted with RSA
            key is 32 bytes long
            iv is 16 bytes long and can be sent in plain text
        """
        self.aes_key, self.aes_iv = os.urandom(32), os.urandom(16)
        other_public_key = self.other_certificate.public_key()
        data_to_send = utils.rsa_encrypt(self.aes_key, other_public_key)
        utils.send_data(self.active_socket, data_to_send, 'encrypted aes key')
        utils.send_data(self.active_socket, self.aes_iv, 'aes iv')

    def _create_aes_cipher(self):
        """
            method for just creating aes cipher using CBC mode and AES
        """
        if self.aes_key is None or self.aes_iv is None:
            raise ValueError('null value')
        self.cipher = Cipher(algorithms.AES(self.aes_key),
                             modes.CBC(self.aes_iv),
                             utils.default_backend()
                             )

    def send_data(self, input_data):
        """
            method for sending encrypted data either from a file or from an input
        """
        if input_data[:5] == 'file:':
            input_data = utils.read_file(input_data[5:])
        c_message = utils.aes_encrypt(self.cipher, bytes(input_data, 'utf-8'))
        utils.send_data(self.active_socket, c_message, 'encrypted message')

    def receive_data(self):
        """
            this method is for receiving encrypted data and then decrypting it and storing it
            in list of received message or a file
        """
        c_message = utils.receive_data(self.active_socket, 'encrypted message')
        message = utils.aes_decrypt(self.cipher, c_message)
        return message.decode()

    def use_user(self, state):
        """
            first function that is ran when User.py is ran
        """
        self.send_request_to_ca()
        self.get_ca_certificate()
        utils.rsa_verify_certificate(self.ca_certificate, self.my_certificate)
        self.exchange_certificates_and_keys(state)
